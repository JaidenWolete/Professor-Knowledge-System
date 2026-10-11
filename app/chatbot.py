
from pathlib import Path
import re

from pyswip import Prolog


# ==================================================
# 1. INITIALIZE PROLOG
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent
PROLOG_DIR = BASE_DIR / "prolog"

prolog = Prolog()

for filename in (
    "professors.pl",
    "schedule.pl",
    "syllabus.pl",
    "rules.pl",
):
    filepath = PROLOG_DIR / filename

    if filepath.exists():
        prolog.consult(str(filepath))
    else:
        print(f"Warning: Missing Prolog file: {filepath}")


# ==================================================
# 2. GENERAL HELPERS
# ==================================================

def clean(value):
    if value is None:
        return ""

    if isinstance(value, bytes):
        value = value.decode("utf-8", errors="replace")

    return str(value).strip()


def normalize(value):
    return re.sub(r"\s+", " ", clean(value)).strip().lower()


def normalize_person(value):
    value = normalize(value)

    return re.sub(
        r"^(dr|prof|professor)\.?\s+",
        "",
        value,
    ).strip()


def course_key(value):
    """
    Compare course codes while ignoring spaces and letter case.

    Examples:
        CTEC 350.170 -> CTEC350.170
        CTEC350.170  -> CTEC350.170

    The original spelling from Prolog is preserved separately.
    """
    return re.sub(r"\s+", "", clean(value)).upper()


def quote_prolog(value):
    value = clean(value)
    value = value.replace("\\", "\\\\")
    value = value.replace('"', '\\"')
    return f'"{value}"'


def run_query(query):
    try:
        return list(prolog.query(query))
    except Exception as error:
        print(f"Prolog query error: {error}")
        return []


# ==================================================
# 3. PROFESSOR LOOKUPS
# ==================================================

def get_all_professors():
    professors = set()

    for result in run_query("professor(P)"):
        name = clean(result.get("P"))

        if name:
            professors.add(name)

    return sorted(professors)


def canonical_name(name):
    target = normalize_person(name)

    for professor in get_all_professors():
        if normalize_person(professor) == target:
            return professor

    return name.strip()


def find_professor_matches(question):
    question_text = normalize(question)
    matches = []

    for professor in get_all_professors():
        name = normalize(professor)
        short_name = normalize_person(professor)

        if name and name in question_text:
            matches.append(professor)
            continue

        if short_name and short_name in question_text:
            matches.append(professor)
            continue

        # Also allow a distinctive last name.
        parts = short_name.split()

        if parts:
            last_name = parts[-1]

            if (
                len(last_name) > 3
                and re.search(
                    rf"\b{re.escape(last_name)}\b",
                    question_text,
                )
            ):
                matches.append(professor)

    # Prefer the longest matched name if multiple names overlap.
    return sorted(
        set(matches),
        key=len,
        reverse=True,
    )


def get_professor_detail(professor, predicate):
    professor = canonical_name(professor)
    quoted_name = quote_prolog(professor)

    results = run_query(
        f"{predicate}({quoted_name}, Value)"
    )

    return sorted({
        clean(result.get("Value"))
        for result in results
        if clean(result.get("Value"))
    })


def get_courses_by_professor(professor):
    professor = canonical_name(professor)
    target = normalize_person(professor)
    courses = set()

    # teaches(Professor, Course)
    for result in run_query("teaches(P, C)"):
        name = clean(result.get("P"))
        code = clean(result.get("C"))

        if code and normalize_person(name) == target:
            courses.add(code)

    # instructor(Course, Instructor)
    for result in run_query("instructor(C, I)"):
        name = clean(result.get("I"))
        code = clean(result.get("C"))

        if code and normalize_person(name) == target:
            courses.add(code)

    return sorted(courses, key=course_key)


# ==================================================
# 4. COURSE LOOKUPS
# ==================================================

def get_course_codes():
    courses = set()

    # teaches(Professor, Course): Course is the second argument.
    for result in run_query("teaches(_, C)"):
        code = clean(result.get("C"))

        if code:
            courses.add(code)

    # These predicates store Course in their first argument.
    for predicate in ("course", "days", "room", "instructor"):
        for result in run_query(f"{predicate}(C, _)"):
            code = clean(result.get("C"))

            if code:
                courses.add(code)

    # time(Course, Start, End) is a three-argument predicate.
    for result in run_query("time(C, _, _)"):
        code = clean(result.get("C"))

        if code:
            courses.add(code)

    return sorted(courses, key=course_key)


def find_course_code(question):
    """
    Find a course code in the question and return its exact
    spelling from the Prolog database whenever it is available.
    """
    pattern = r"\b[A-Z]{3,5}\s*\d{3}(?:\.\d{3})?\b"

    match = re.search(pattern, question, re.IGNORECASE)

    if not match:
        return None

    candidate = match.group(0)
    candidate_key = course_key(candidate)

    # IMPORTANT: return the exact stored course code.
    for stored_code in get_course_codes():
        if course_key(stored_code) == candidate_key:
            return stored_code

    # No matching fact exists. Keep a consistently formatted
    # candidate so the chatbot can report missing information.
    return re.sub(r"\s+", "", candidate).upper()


def get_course_property(course_code, predicate):
    quoted_code = quote_prolog(course_code)

    results = run_query(
        f"{predicate}({quoted_code}, Value)"
    )

    return sorted({
        clean(result.get("Value"))
        for result in results
        if clean(result.get("Value"))
    })


def get_course_title(course_code):
    titles = get_course_property(course_code, "course")

    return titles[0] if titles else ""


def get_course_times(course_code):
    quoted_code = quote_prolog(course_code)

    # Correct arity: time/3, never time/2.
    results = run_query(
        f"time({quoted_code}, Start, End)"
    )

    times = set()

    for result in results:
        start = clean(result.get("Start"))
        end = clean(result.get("End"))

        if start and end:
            times.add((start, end))

    return sorted(times)


def get_course_instructors(course_code):
    target = course_key(course_code)
    instructors = set()

    # Use instructor(Course, Instructor) facts.
    for result in run_query("instructor(C, I)"):
        code = clean(result.get("C"))
        name = clean(result.get("I"))

        if code and name and course_key(code) == target:
            instructors.add(name)

    # Also use teaches(Professor, Course) facts.
    for result in run_query("teaches(P, C)"):
        name = clean(result.get("P"))
        code = clean(result.get("C"))

        if code and name and course_key(code) == target:
            instructors.add(name)

    return sorted(instructors)


# ==================================================
# 5. FORMATTING HELPERS
# ==================================================

def format_days(value):
    day_codes = {
        "M": "Monday",
        "T": "Tuesday",
        "W": "Wednesday",
        "R": "Thursday",
        "F": "Friday",
        "S": "Saturday",
        "U": "Sunday",
    }

    value = clean(value).upper()

    if re.fullmatch(r"[MTWRFSU]+", value):
        return ", ".join(
            day_codes[letter]
            for letter in value
        )

    return clean(value)


def format_time(value):
    value = clean(value)

    try:
        parts = value.split(":")
        hour = int(parts[0])
        minute = int(parts[1])

        suffix = "AM" if hour < 12 else "PM"
        display_hour = hour % 12 or 12

        return f"{display_hour}:{minute:02d} {suffix}"

    except (ValueError, IndexError):
        return value


# ==================================================
# 6. QUESTION ANSWERING
# ==================================================

def answer_question(question):
    normalized = normalize(question)

    if not normalized:
        return "Please enter a question."

    if normalized in {"quit", "exit"}:
        return None

    # --------------------------------------------------
    # List professors
    # --------------------------------------------------

    if (
        "list professors" in normalized
        or "which professors" in normalized
        or "who are the professors" in normalized
        or "all professors" in normalized
    ):
        professors = get_all_professors()

        if professors:
            return (
                "Professors:\n"
                + "\n".join(f"- {p}" for p in professors)
            )

        return "No professors found."

    # Detect professors and course codes independently.
    professors = find_professor_matches(question)
    course_code = find_course_code(question)

    # --------------------------------------------------
    # Professor questions
    # --------------------------------------------------

    if professors and not course_code:
        professor = professors[0]

        if re.search(
            r"\b(courses|classes|teach|teaches|teaching)\b",
            normalized,
        ):
            courses = get_courses_by_professor(professor)

            if courses:
                return (
                    f"Courses taught by {professor}:\n"
                    + "\n".join(f"- {c}" for c in courses)
                )

            return f"No courses found for {professor}."

        if re.search(
            r"\b(email|e-mail|contact)\b",
            normalized,
        ):
            values = get_professor_detail(professor, "email")

            if values:
                return (
                    f"{professor}'s email: "
                    + ", ".join(values)
                )

            return f"No email found for {professor}."

        if re.search(
            r"\b(office|office room)\b",
            normalized,
        ):
            values = get_professor_detail(professor, "office")

            if values:
                return (
                    f"{professor}'s office: "
                    + ", ".join(values)
                )

            return f"No office found for {professor}."

        if re.search(
            r"\b(department|faculty)\b",
            normalized,
        ):
            values = get_professor_detail(
                professor, "department"
            )

            if values:
                return (
                    f"{professor}'s department: "
                    + ", ".join(values)
                )

            return f"No department found for {professor}."

        if re.search(
            r"\b(specialty|specialties|expertise|expert)\b",
            normalized,
        ):
            values = get_professor_detail(
                professor, "specialty"
            )

            if values:
                return (
                    f"{professor}'s specialties:\n"
                    + "\n".join(f"- {v}" for v in values)
                )

            return f"No specialties found for {professor}."

        # A professor-only question defaults to their courses.
        courses = get_courses_by_professor(professor)

        if courses:
            return (
                f"Courses taught by {professor}:\n"
                + "\n".join(f"- {c}" for c in courses)
            )

        return f"I found {professor}, but no courses are listed."

    # --------------------------------------------------
    # Course questions
    # --------------------------------------------------

    if course_code:
        # Instructor questions.
        if re.search(
            r"\b(who|instructor|professor|teacher|teaches|teaching)\b",
            normalized,
        ):
            instructors = get_course_instructors(course_code)

            if instructors:
                return (
                    f"{course_code} is taught by "
                    + ", ".join(instructors)
                    + "."
                )

            return f"No instructor found for {course_code}."

        # Meeting time questions.
        if re.search(
            r"\b(time|times|start|starts|end|ends|begin|begins|"
            r"finish|finishes|hour|hours|when)\b",
            normalized,
        ):
            times = get_course_times(course_code)

            if times:
                return "\n".join(
                    f"{course_code} meets from "
                    f"{format_time(start)} to {format_time(end)}."
                    for start, end in times
                )

            return f"No meeting time found for {course_code}."

        # Meeting days questions.
        if re.search(
            r"\b(days|day|weekday|weekdays)\b",
            normalized,
        ):
            days = get_course_property(course_code, "days")

            if days:
                return (
                    f"{course_code} meets on "
                    + "; ".join(format_days(d) for d in days)
                    + "."
                )

            return f"No meeting days found for {course_code}."

        # Classroom questions.
        if re.search(
            r"\b(room|classroom|location|where)\b",
            normalized,
        ):
            rooms = get_course_property(course_code, "room")

            if rooms:
                return (
                    f"{course_code} meets in room "
                    + ", ".join(rooms)
                    + "."
                )

            return f"No room found for {course_code}."

        # Course title questions.
        if re.search(
            r"\b(title|name|called|description)\b",
            normalized,
        ):
            title = get_course_title(course_code)

            if title:
                return f"{course_code} is {title}."

            return f"No course title found for {course_code}."

        # General course summary.
        details = [f"Course: {course_code}"]

        title = get_course_title(course_code)
        days = get_course_property(course_code, "days")
        rooms = get_course_property(course_code, "room")
        times = get_course_times(course_code)
        instructors = get_course_instructors(course_code)

        if title:
            details.append(f"Title: {title}")

        if instructors:
            details.append(
                "Instructor: " + ", ".join(instructors)
            )

        if days:
            details.append(
                "Days: "
                + ", ".join(format_days(d) for d in days)
            )

        if times:
            start, end = times[0]
            details.append(
                f"Time: {format_time(start)} to {format_time(end)}"
            )

        if rooms:
            details.append("Room: " + ", ".join(rooms))

        return "\n".join(details)

    return (
        "Sorry, I could not understand that question. "
        "Try asking about a professor, or include a course code "
        "such as CTEC 350.170 or COSC369."
    )


# ==================================================
# 7. MAIN CHAT LOOP
# ==================================================

def main():
    print("Professor Knowledge Expert System")
    print("Ask about professors, courses, meeting times, days, or rooms.")
    print("Type 'quit' to exit.\n")

    while True:
        try:
            question = input("Ask a question (or type quit): ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        answer = answer_question(question)

        if answer is None:
            print("Goodbye!")
            break

        print(answer)
        print()


if __name__ == "__main__":
    main()



from pathlib import Path
import re
from pyswip import Prolog

# Find the project directories
BASE_DIR = Path(__file__).resolve().parent.parent
PROLOG_DIR = BASE_DIR / "prolog"

# Initialize Prolog
prolog = Prolog()

# Load the knowledge base files
for filename in [
    "professors.pl",
    "schedule.pl",
    "syllabus.pl",
    "rules.pl"
]:
    file_path = PROLOG_DIR / filename
    prolog.consult(str(file_path))


def clean(value):
    """Convert Prolog values into readable Python strings."""
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return str(value)


def normalize(text):
    """Normalize text for easier comparison."""
    return re.sub(r"\s+", " ", text.strip()).lower()


def canonical_name(name):
    """Remove titles so professor names can be matched consistently."""
    name = clean(name)
    name = re.sub(
        r"\b(dr|doctor|prof|professor)\.?\s*",
        "",
        name,
        flags=re.IGNORECASE
    )
    return normalize(name)


def run_query(query):
    """Run a Prolog query and return all results."""
    try:
        return list(prolog.query(query))
    except Exception as error:
        print(f"Query error: {error}")
        return []


def get_all_professors():
    """Collect professors from professor and teaching facts."""
    names = set()

    for result in run_query("professor(P)"):
        names.add(clean(result["P"]))

    for result in run_query("teaches(P, C)"):
        names.add(clean(result["P"]))

    for result in run_query("instructor(C, P)"):
        names.add(clean(result["P"]))

    return sorted(names)


def get_all_teaching_facts():
    """Collect course and professor relationships."""
    facts = set()

    for result in run_query("teaches(P, C)"):
        facts.add((clean(result["P"]), clean(result["C"])))

    for result in run_query("instructor(C, P)"):
        facts.add((clean(result["P"]), clean(result["C"])))

    return facts


def get_course_titles():
    """Collect course codes and titles."""
    titles = {}

    for result in run_query("course(C, T)"):
        code = clean(result["C"]).upper()
        title = clean(result["T"])
        titles[code] = title

    return titles


def find_professor_matches(name):
    """Find professors by full name or partial name."""
    requested = canonical_name(name)
    requested_words = requested.split()

    matches = {}

    for professor in get_all_professors():
        normalized_professor = canonical_name(professor)
        professor_words = normalized_professor.split()

        exact_match = normalized_professor == requested
        partial_match = (
            requested in normalized_professor
            or all(word in professor_words for word in requested_words)
        )

        if exact_match or partial_match:
            matches[normalized_professor] = professor

    return list(matches.values())


def get_courses_by_professor(professor_name):
    """Find courses taught under all variants of a professor's name."""
    target = canonical_name(professor_name)
    courses = set()

    for professor, course_code in get_all_teaching_facts():
        if canonical_name(professor) == target:
            courses.add(course_code.upper())

    return sorted(courses)


def find_course_instructors(course_code):
    """Find instructors for a course."""
    target = normalize(course_code).upper()
    instructors = set()

    for professor, code in get_all_teaching_facts():
        if normalize(code).upper() == target:
            instructors.add(professor)

    return sorted(instructors)


def find_course_code(text):
    """Extract a course code such as CTEC 350.170."""
    match = re.search(
        r"\b([A-Z]{2,}\s*\d{3}\.\d{3})\b",
        text,
        re.IGNORECASE
    )

    if match:
        return re.sub(r"\s+", " ", match.group(1)).upper()

    return None


def get_course_property(course_code, predicate):
    """Look up a course property, such as its days or room."""
    course_code = course_code.upper()

    # Escape quotation marks in case a code contains them.
    safe_code = course_code.replace("\\", "\\\\").replace('"', '\\"')
    query = f'{predicate}("{safe_code}", Value)'

    results = run_query(query)

    if results:
        return clean(results[0]["Value"])

    return None


def format_days(days):
    """Translate schedule abbreviations into readable day names."""
    day_names = {
        "M": "Monday",
        "T": "Tuesday",
        "W": "Wednesday",
        "R": "Thursday",
        "F": "Friday",
        "S": "Saturday",
        "U": "Sunday"
    }

    readable = [day_names[letter] for letter in days if letter in day_names]

    if readable:
        return ", ".join(readable)

    return days


def get_professor_details(professor_name, predicate):
    """Retrieve details such as department, office, or email."""
    matches = find_professor_matches(professor_name)

    if not matches:
        return None, None

    if len(matches) > 1:
        return "multiple", matches

    target = canonical_name(matches[0])

    # Search facts using the actual professor name in the knowledge base.
    for professor in matches:
        safe_name = professor.replace("\\", "\\\\").replace('"', '\\"')
        query = f'{predicate}("{safe_name}", Value)'
        results = run_query(query)

        if results:
            return professor, clean(results[0]["Value"])

    # If no exact fact was found, report that the detail is unavailable.
    return matches[0], None


def answer_question(question):
    """Understand the question and return an answer."""
    question = question.strip()
    normalized = normalize(question)

    # List professors
    if re.search(r"\b(list|show)\s+(all\s+)?professors\b", normalized):
        professors = get_all_professors()

        if not professors:
            return "No professors found in the knowledge base."

        unique_names = {}
        for professor in professors:
            unique_names[canonical_name(professor)] = professor

        return "Professors:\n" + "\n".join(
            f"- {name}" for name in sorted(unique_names.values())
        )

    # Questions about course meeting days
    if re.search(r"\b(what|which)\s+days\b|\bwhen\b", normalized):
        course_code = find_course_code(question)

        if course_code:
            days = get_course_property(course_code, "days")

            if days:
                return f"{course_code} meets on {format_days(days)}."

            return f"I could not find meeting days for {course_code}."

    # Questions about course room numbers
    if re.search(r"\b(room|where)\b", normalized):
        course_code = find_course_code(question)

        if course_code:
            room = get_course_property(course_code, "room")

            if room:
                return f"{course_code} meets in room {room}."

            return f"I could not find a room for {course_code}."

    # Questions about course meeting times
    if re.search(r"\b(time|what time|when)\b", normalized):
        course_code = find_course_code(question)

        if course_code:
            start = get_course_property(course_code, "time_start")
            end = get_course_property(course_code, "time_end")

            if start and end:
                return f"{course_code} meets from {start} to {end}."

            # The schedule may store both times in one time/3 predicate.
            results = run_query(
                f'time("{course_code}", Start, End)'
            )

            if results:
                start = clean(results[0]["Start"])
                end = clean(results[0]["End"])
                return f"{course_code} meets from {start} to {end}."

            return f"I could not find meeting times for {course_code}."

    # Questions asking who teaches a course
    if re.search(r"\b(who|which professor|which instructor)\b", normalized):
        course_code = find_course_code(question)

        if course_code:
            instructors = find_course_instructors(course_code)

            if instructors:
                return (
                    f"Instructor(s) for {course_code}:\n"
                    + "\n".join(f"- {name}" for name in instructors)
                )

            return f"I could not find an instructor for {course_code}."

    # Questions asking which courses a professor teaches
    match = re.search(
        r"(?:which|what)\s+courses\s+(?:does|do)\s+(.+?)\s+teach\??$",
        question,
        re.IGNORECASE
    )

    if match:
        requested_name = match.group(1).strip()
        professors = find_professor_matches(requested_name)

        if not professors:
            return f"I could not find a professor matching '{requested_name}'."

        if len(professors) > 1:
            return (
                "Multiple professors matched:\n"
                + "\n".join(f"- {name}" for name in professors)
                + "\nPlease enter a more specific name."
            )

        courses = get_courses_by_professor(professors[0])

        if not courses:
            return f"No courses found for {professors[0]}."

        titles = get_course_titles()
        lines = []

        for code in courses:
            title = titles.get(code, "")
            if title:
                lines.append(f"- {code}: {title}")
            else:
                lines.append(f"- {code}")

        return f"Courses taught by {professors[0]}:\n" + "\n".join(lines)

    # Professor email
    match = re.search(
        r"(?:what\s+is\s+)?(?:the\s+)?email\s+(?:for|of)\s+(.+?)\??$",
        question,
        re.IGNORECASE
    )

    if match:
        name = match.group(1).strip()
        professor, value = get_professor_details(name, "email")

        if professor == "multiple":
            return (
                "Multiple professors matched:\n"
                + "\n".join(f"- {p}" for p in value)
            )

        if not professor:
            return f"I could not find a professor matching '{name}'."

        if value:
            return f"Email for {professor}: {value}"

        return f"No email information found for {professor}."

    # Professor office
    match = re.search(
        r"(?:what\s+is\s+)?(?:the\s+)?office\s+(?:for|of)\s+(.+?)\??$",
        question,
        re.IGNORECASE
    )

    if match:
        name = match.group(1).strip()
        professor, value = get_professor_details(name, "office")

        if professor == "multiple":
            return (
                "Multiple professors matched:\n"
                + "\n".join(f"- {p}" for p in value)
            )

        if not professor:
            return f"I could not find a professor matching '{name}'."

        if value:
            return f"Office for {professor}: {value}"

        return f"No office information found for {professor}."

    # General professor name lookup
    professors = find_professor_matches(question)

    if len(professors) == 1:
        courses = get_courses_by_professor(professors[0])

        if courses:
            return (
                f"{professors[0]} teaches:\n"
                + "\n".join(f"- {course}" for course in courses)
            )

        return f"I found {professors[0]}, but no courses are listed."

    if len(professors) > 1:
        return (
            "Multiple professors matched:\n"
            + "\n".join(f"- {name}" for name in professors)
            + "\nPlease enter a more specific name."
        )

    return (
        "Sorry, I could not understand that question.\n"
        "Try questions such as:\n"
        "- Which courses does Anthony Adedoyin teach?\n"
        "- Which courses does Appolo Tankeh teach?\n"
        "- Who teaches CTEC 350.170?\n"
        "- What days does CTEC 345.170 meet?\n"
        "- What room is CTEC 435.170 in?\n"
        "- What time does CTEC 435.170 meet?\n"
        "- What is the email for Anthony Adedoyin?\n"
        "- What is Anthony Adedoyin's office?\n"
        "- List professors"
    )


# Main chatbot loop
print("Professor Knowledge Expert System")
print("Ask a question, or type 'quit' to exit.")

while True:
    try:
        question = input("\nAsk a question (or type quit): ").strip()

        if question.lower() in {"quit", "exit"}:
            print("Goodbye!")
            break

        if not question:
            continue

        print("\n" + answer_question(question))

    except KeyboardInterrupt:
        print("\nGoodbye!")
        break


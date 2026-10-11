
from docx import Document
from pathlib import Path
import re


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

SYLLABUS_FILE = (
    BASE_DIR
    / "data"
    / "Sept1_28_Syllabus_COSC 369-Software Engineering- - Dr. Tankeh updated.docx"
)

OUTPUT_FILE = BASE_DIR / "prolog" / "syllabus.pl"


def prolog_string(value):
    """Escape text for a Prolog double-quoted string."""
    value = str(value)
    value = value.replace("\\", "\\\\")
    value = value.replace('"', '\\"')
    value = value.replace("\n", "\\n")
    value = value.replace("\r", "\\r")
    return f'"{value}"'


def main():
    doc = Document(SYLLABUS_FILE)

    # Read all paragraphs from the syllabus.
    paragraphs = [
        paragraph.text.strip()
        for paragraph in doc.paragraphs
        if paragraph.text.strip()
    ]

    # Also read text from tables, since syllabus details
    # may be stored inside tables.
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                text = cell.text.strip()
                if text:
                    paragraphs.append(text)

    syllabus_text = "\n".join(paragraphs)

    # Defaults based on the known COSC 369 syllabus.
    course_code = "COSC369"
    course_title = "Software Engineering I"
    instructor_name = "Dr. Appolo Tankeh"

    # Attempt to identify the course code in the document.
    code_match = re.search(
        r"\b(COSC)\s*[- ]?\s*(369)\b",
        syllabus_text,
        re.IGNORECASE,
    )

    if code_match:
        course_code = f"{code_match.group(1).upper()}{code_match.group(2)}"

    # Look for an instructor name in the document.
    instructor_match = re.search(
        r"(?:instructor|professor)\s*:\s*"
        r"(Dr\.?\s+[A-Z][A-Za-z.'-]+"
        r"(?:\s+[A-Z][A-Za-z.'-]+)*)",
        syllabus_text,
        re.IGNORECASE,
    )

    if instructor_match:
        instructor_name = instructor_match.group(1).strip()

    # Write Prolog facts.
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as output:
        output.write(":- multifile course/2.\n")
        output.write(":- multifile instructor/2.\n")
        output.write(":- multifile teaches/2.\n\n")

        output.write(
            f"course({prolog_string(course_code)}, "
            f"{prolog_string(course_title)}).\n"
        )

        output.write(
            f"instructor({prolog_string(course_code)}, "
            f"{prolog_string(instructor_name)}).\n"
        )

        output.write(
            f"teaches({prolog_string(instructor_name)}, "
            f"{prolog_string(course_code)}).\n"
        )

    print(f"Generated {OUTPUT_FILE}")
    print(f"Course: {course_code} - {course_title}")
    print(f"Instructor: {instructor_name}")


if __name__ == "__main__":
    main()


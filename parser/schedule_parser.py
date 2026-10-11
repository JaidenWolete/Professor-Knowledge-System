
import pandas as pd
import yaml
from pathlib import Path
from datetime import datetime, date, time

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
EXCEL_FILE = BASE_DIR / "data" / "CTEC Fall 2026 Schedule - Share (2).xlsx"
YAML_FILE = BASE_DIR / "data" / "professors.yaml"
OUTPUT_FILE = BASE_DIR / "prolog" / "schedule.pl"


def clean_value(value):
    """Convert Excel values to clean strings."""
    if pd.isna(value):
        return ""

    if isinstance(value, (datetime, date, time)):
        return value.strftime("%H:%M:%S")

    return str(value).strip()


def prolog_string(value):
    """Escape a value for a Prolog double-quoted string."""
    value = str(value)
    value = value.replace("\\", "\\\\")
    value = value.replace('"', '\\"')
    value = value.replace("\n", "\\n")
    value = value.replace("\r", "\\r")
    return f'"{value}"'


def convert_instructor_name(name):
    """Convert 'Last, First' to 'First Last'."""
    name = name.strip()

    if "," in name:
        parts = [part.strip() for part in name.split(",", 1)]
        if len(parts) == 2 and parts[0] and parts[1]:
            return f"{parts[1]} {parts[0]}"

    return name


def main():
    # Read the Excel schedule.
    df = pd.read_excel(EXCEL_FILE)

    # Remove accidental spaces from column names.
    df.columns = [str(column).strip() for column in df.columns]

    required_columns = [
        "ID", "Course Title", "Instructor 2025",
        "Days", "Room", "Begin", "End"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing Excel columns: {missing_columns}. "
            f"Available columns: {list(df.columns)}"
        )

    # Load additional professor names from YAML.
    with open(YAML_FILE, "r", encoding="utf-8") as yaml_file:
        yaml_data = yaml.safe_load(yaml_file) or {}

    professors = set()

    for professor in yaml_data.get("professors", []):
        name = str(professor.get("name", "")).strip()
        if name and name.lower() != "nan":
            professors.add(name)

    facts = []

    # Declare predicates that can also be defined in other files.
    facts.extend([
        ":- multifile course/2.",
        ":- multifile teaches/2.",
        ":- multifile days/2.",
        ":- multifile room/2.",
        ":- multifile time/3.",
        ":- multifile professor/1.",
        ""
    ])

    # Generate course facts.
    for _, row in df.iterrows():
        course = clean_value(row["ID"])
        title = clean_value(row["Course Title"])
        instructor = convert_instructor_name(
            clean_value(row["Instructor 2025"])
        )
        days = clean_value(row["Days"])
        room = clean_value(row["Room"])
        begin_time = clean_value(row["Begin"])
        end_time = clean_value(row["End"])

        # Skip rows without a course identifier.
        if not course:
            continue

        facts.append(
            f"course({prolog_string(course)}, "
            f"{prolog_string(title)})."
        )

        # Don't create a teaching fact for missing instructors.
        if instructor and instructor.lower() != "nan":
            facts.append(
                f"teaches({prolog_string(instructor)}, "
                f"{prolog_string(course)})."
            )
            professors.add(instructor)

        # Missing values are represented as empty strings,
        # not the literal text "nan".
        if days.lower() == "nan":
            days = ""
        if room.lower() == "nan":
            room = ""
        if begin_time.lower() == "nan":
            begin_time = ""
        if end_time.lower() == "nan":
            end_time = ""

        facts.append(
            f"days({prolog_string(course)}, "
            f"{prolog_string(days)})."
        )
        facts.append(
            f"room({prolog_string(course)}, "
            f"{prolog_string(room)})."
        )
        facts.append(
            f"time({prolog_string(course)}, "
            f"{prolog_string(begin_time)}, "
            f"{prolog_string(end_time)})."
        )

    # Add the professor list.
    facts.append("")
    facts.append("% Professors")

    for professor in sorted(professors):
        facts.append(
            f"professor({prolog_string(professor)})."
        )

    # Write the generated Prolog file.
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        "\n".join(facts) + "\n",
        encoding="utf-8"
    )

    print(f"Generated {OUTPUT_FILE}")
    print(f"Found {len(professors)} distinct professor names.")
    print(f"Processed {len(df)} spreadsheet rows.")


if __name__ == "__main__":
    main()


from pathlib import Path
import yaml


# Get the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Define file paths
yaml_path = PROJECT_ROOT / "data" / "professors.yaml"
prolog_path = PROJECT_ROOT / "prolog" / "professors.pl"


def prolog_string(value):
    """Convert a Python value into a safely quoted Prolog string."""
    if value is None:
        value = ""

    value = str(value)
    value = value.replace("\\", "\\\\").replace('"', '\\"')
    value = value.replace("\n", "\\n").replace("\r", "\\r")

    return f'"{value}"'


# Load professor information
with open(yaml_path, "r", encoding="utf-8") as file:
    data = yaml.safe_load(file) or {}

professors = data.get("professors", [])

# Generate professors.pl
with open(prolog_path, "w", encoding="utf-8") as output:
    output.write(":- multifile professor/1.\n")
    output.write(":- multifile department/2.\n")
    output.write(":- multifile office/2.\n")
    output.write(":- multifile email/2.\n")
    output.write(":- multifile specialty/2.\n\n")

    for professor in professors:
        name = prolog_string(professor.get("name"))
        department = prolog_string(professor.get("department"))
        office = prolog_string(professor.get("office"))
        email = prolog_string(professor.get("email"))

        output.write(f"professor({name}).\n")
        output.write(f"department({name},{department}).\n")
        output.write(f"office({name},{office}).\n")
        output.write(f"email({name},{email}).\n")

        for specialty in professor.get("specialty", []):
            output.write(
                f"specialty({name},{prolog_string(specialty)}).\n"
            )

        output.write("\n")

print(f"Generated {prolog_path}")
print(f"Processed {len(professors)} professors.")

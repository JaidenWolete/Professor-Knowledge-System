import pandas as pd
import yaml

file_path = "data/CTEC Fall 2026 Schedule - Share (2).xlsx"

# Read schedule
df = pd.read_excel(file_path)

# Store all professors in a set (prevents duplicates)
professors = set()

with open("prolog/schedule.pl", "w") as output:

    # Process schedule rows
    for _, row in df.iterrows():

        course = str(row["ID"]).strip()
        title = str(row["Course Title"]).strip()
        instructor = str(row["Instructor 2025"]).strip()
        days = str(row["Days"]).strip()
        room = str(row["Room"]).strip()
        begin_time = str(row["Begin"]).strip()
        end_time = str(row["End "]).strip()

        # Save instructor from Excel
        if instructor and instructor.lower() != "nan":
            professors.add(instructor)

        output.write(
            f'course("{course}","{title}").\n'
        )

        output.write(
            f'teaches("{instructor}","{course}").\n'
        )

        output.write(
            f'days("{course}","{days}").\n'
        )

        output.write(
            f'room("{course}","{room}").\n'
        )

        output.write(
            f'time("{course}","{begin_time}","{end_time}").\n'
        )

    # Read professors from YAML
    with open("data/professors.yaml", "r") as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)

    for prof in yaml_data["professors"]:
        professors.add(prof["name"])

    # Write professor facts
    output.write("\n% Professors\n")

    for professor in sorted(professors):
        output.write(
            f'professor("{professor}").\n'
        )

print(f"Generated schedule.pl with {len(professors)} professors")

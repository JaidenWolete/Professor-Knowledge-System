import yaml

# Load YAML file
with open("data/professors.yaml", "r") as file:
    data = yaml.safe_load(file)

# Create professors.pl
with open("prolog/professors.pl", "w") as output:

    for professor in data["professors"]:

        name = professor["name"]

        output.write(
            f'professor("{name}").\n'
        )

        output.write(
            f'department("{name}","{professor["department"]}").\n'
        )

        output.write(
            f'office("{name}","{professor["office"]}").\n'
        )

        output.write(
            f'email("{name}","{professor["email"]}").\n'
        )

        for specialty in professor["specialty"]:

            output.write(
                f'specialty("{name}","{specialty}").\n'
            )

print("Generated prolog/professors.pl")

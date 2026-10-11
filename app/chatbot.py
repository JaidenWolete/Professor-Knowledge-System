from pyswip import Prolog

prolog = Prolog()

# Load knowledge base
prolog.consult("prolog/professors.pl")
prolog.consult("prolog/schedule.pl")
prolog.consult("prolog/syllabus.pl")
prolog.consult("prolog/rules.pl")

print("Professor Knowledge Expert System")

while True:

    question = input("\nAsk a question (or type quit): ").strip()

    if question.lower() == "quit":
        print("Goodbye!")
        break

    elif question.lower() == "list professors":

        print("\nProfessors:")
        for result in prolog.query("professor(X)"):
            print("-", result["X"])

    elif question.lower().startswith("who teaches"):

        course = (
            question.replace("Who teaches", "")
                    .replace("?", "")
                    .strip()
        )

        found = False

        for result in prolog.query(
            f'course_professor("{course}", X)'
        ):
            print("Professor:", result["X"])
            found = True

        if not found:
            print("Course not found.")

    elif question.lower().startswith("what room is"):

        course = (
            question.replace("What room is", "")
                    .replace("in?", "")
                    .replace("?", "")
                    .strip()
        )

        found = False

        for result in prolog.query(
            f'course_room("{course}", X)'
        ):
            print("Room:", result["X"])
            found = True

        if not found:
            print("Room not found.")

    elif question.lower().startswith("what days does"):

        course = (
            question.replace("What days does", "")
                    .replace("meet?", "")
                    .replace("?", "")
                    .strip()
        )

        found = False

        for result in prolog.query(
            f'course_days("{course}", X)'
        ):
            print("Days:", result["X"])
            found = True

        if not found:
            print("Days not found.")

    elif "email" in question.lower():

        professor = (
            question.replace("What is", "")
                    .replace("'s email", "")
                    .replace("email", "")
                    .replace("?", "")
                    .strip()
        )

        found = False

        for result in prolog.query(
            f'professor_email("{professor}", X)'
        ):
            print("Email:", result["X"])
            found = True

        if not found:
            print("Email not found.")

    elif "office" in question.lower():

        professor = (
            question.replace("What is", "")
                    .replace("'s office", "")
                    .replace("office", "")
                    .replace("?", "")
                    .strip()
        )

        found = False

        for result in prolog.query(
            f'professor_office("{professor}", X)'
        ):
            print("Office:", result["X"])
            found = True

        if not found:
            print("Office not found.")

    elif "specialty" in question.lower():

        professor = (
            question.replace("What is", "")
                    .replace("'s specialty", "")
                    .replace("specialty", "")
                    .replace("?", "")
                    .strip()
        )

        found = False

        for result in prolog.query(
            f'professor_specialty("{professor}", X)'
        ):
            print("Specialty:", result["X"])
            found = True

        if not found:
            print("Specialty not found.")

    else:
        print("Question not recognized.")

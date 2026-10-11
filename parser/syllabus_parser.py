from docx import Document

file_path = "data/Sept1_28_Syllabus_COSC 369-Software Engineering- - Dr. Tankeh updated.docx"

doc = Document(file_path)

with open("prolog/syllabus.pl", "w") as output:

    output.write(
        'course("COSC369","Software Engineering I").\n'
    )

    output.write(
        'instructor("COSC369","Dr. Appolo Tankeh").\n'
    )

    output.write(
        'teaches("Dr. Appolo Tankeh","COSC369").\n'
    )

print("Generated prolog/syllabus.pl")



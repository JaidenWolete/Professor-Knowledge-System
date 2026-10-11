course_professor(Course, Professor) :-
    teaches(Professor, Course).

professor_course(Professor, Course) :-
    teaches(Professor, Course).

course_room(Course, Room) :-
    room(Course, Room).

course_days(Course, Days) :-
    days(Course, Days).

course_instructor(Course, Instructor) :-
    instructor(Course, Instructor).

professor_specialty(Professor, Specialty) :-
    specialty(Professor, Specialty).

professor_email(Professor, Email) :-
    email(Professor, Email).

professor_office(Professor, Office) :-
    office(Professor, Office).

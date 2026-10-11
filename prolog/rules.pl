
% Find the professor teaching a course.
course_professor(Course, Professor) :-
    teaches(Professor, Course).

% Find courses taught by a professor.
professor_course(Professor, Course) :-
    teaches(Professor, Course).

% Find a course's room.
course_room(Course, Room) :-
    room(Course, Room).

% Find a course's meeting days.
course_days(Course, Days) :-
    days(Course, Days).

% Find a course's meeting times.
course_time(Course, Start, End) :-
    time(Course, Start, End).

% Find a course instructor from syllabus information.
course_instructor(Course, Instructor) :-
    instructor(Course, Instructor).

% Find a professor's specialty.
professor_specialty(Professor, Specialty) :-
    specialty(Professor, Specialty).

% Find a professor's email.
professor_email(Professor, Email) :-
    email(Professor, Email).

% Find a professor's office.
professor_office(Professor, Office) :-
    office(Professor, Office).

% Find a professor's department.
professor_department(Professor, Department) :-
    department(Professor, Department).


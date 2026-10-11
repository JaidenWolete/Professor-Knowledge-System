# Professor Knowledge Expert System

**COSC 369 — Midterm Project**

## Project Description

The Professor Knowledge Expert System is a knowledge-based application that uses Python and SWI-Prolog to organize and retrieve information about professors, courses, schedules, and syllabi.

The system collects information from multiple data sources, converts the information into Prolog facts, and allows users to ask questions through an interactive Python chatbot.

## Technologies Used

- **Python**
- **SWI-Prolog** 
- **PySwip** 
- **YAML** 
- **Excel** 
- **DOCX** 
- **GitLab** 

## Features

The system is designed to support questions about:

- Professors and their information
- Courses taught by professors
- Instructors assigned to courses
- Course meeting days and times
- Classroom locations
- Professor office hours, when available in the knowledge base
- Course information and weekly topics, when available in the knowledge base

The answers depend on the information extracted from the source files and loaded into the Prolog knowledge base.

## Data Sources

### 1. Professor Information (YAML)

The professor data file stores information such as:

- Professor names
- Office locations
- Email addresses
- Areas of specialty

### 2. Course Schedule (Excel)

The course schedule contains information such as:

- Course IDs
- Course titles
- Assigned professors
- Classroom locations
- Meeting days
- Meeting times

### 3. Course Syllabus (DOCX)

The syllabus documents may contain:

- Instructor information
- Office hours
- Course descriptions and information
- Weekly topics

## Project Structure

```text
professor-knowledge-system/
├── app/
│   └── chatbot.py
├── data/
│   ├── professors.yaml
│   ├── CTEC Fall 2026 Schedule - Share (2).xlsx
│   └── syllabus documents
├── parser/
│   ├── schedule_parser.py
│   ├── syllabus_parser.py
│   └── yaml_parser.py
├── prolog/
│   ├── professors.pl
│   ├── schedule.pl
│   ├── syllabus.pl
│   └── rules.pl
├── test_prolog.py
├── requirements.txt
├── .gitignore
├── .gitlab-ci.yml
└── README.md
```

## Requirements

The project requires:

- Python 3
- SWI-Prolog
- PySwip
- The Python packages listed in `requirements.txt`

## Installation

### 1. Install SWI-Prolog

Install SWI-Prolog for your operating system. PySwip requires a compatible SWI-Prolog installation.

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Running the Application

From the root directory of the project, run:

```bash
python3 app/chatbot.py
```

The chatbot will load the Prolog knowledge base and prompt the user to enter a question.

Type `quit` or `exit` to close the application.

## Example Questions

Users can try questions such as:

- Which courses does Anthony Adedoyin teach?
- Which courses does Appolo Tankeh teach?
- Who teaches CTEC 350.170?
- What days does CTEC 345.170 meet?
- What room is CTEC 435.170 in?
- What time does CTEC 435.170 meet?
- What is the email for Anthony Adedoyin?
- What is Anthony Adedoyin's office?
- List professors

Available questions depend on the facts and rules loaded into the knowledge base.

## Testing

Run the Prolog test script from the project root:

```bash
python3 test_prolog.py
```

Check that the expected professors, courses, and schedule information are returned.

## Project Goal

The goal of this project is to demonstrate how structured data, logic-based knowledge representation, and a Python interface can work together to build an expert system that answers questions about professors and academic courses.


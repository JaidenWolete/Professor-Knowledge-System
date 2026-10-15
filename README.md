# Professor Knowledge Expert System

## Project Overview

The Professor Knowledge Expert System is a Python and Prolog-based application developed for COSC 369 — Software Engineering. It allows users to ask questions about professors, courses, and class schedules through an interactive command-line chatbot.

Python handles user interaction and data processing, while SWI-Prolog stores academic facts and applies logical rules to retrieve relevant information.

## Features

- Retrieve professor names, departments, office locations, email addresses, and specialties.
- Identify courses taught by professors.
- Look up course titles, instructors, meeting days, times, and rooms.
- Generate Prolog facts from YAML, Excel spreadsheets, and Word documents.
- Query academic information through a Python chatbot.
- Run automated Python checks through GitLab CI/CD.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.11 | Application logic and data processing |
| SWI-Prolog | Knowledge representation and logical reasoning |
| PySwip | Python–Prolog integration |
| PyYAML | Reading professor information from YAML |
| pandas | Processing Excel schedule data |
| openpyxl | Reading Excel files |
| python-docx | Reading Word documents |
| GitLab CI/CD | Automated project checks |

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
├── requirements.txt
├── test_prolog.py
├── .gitlab-ci.yml
└── README.md
```

## Prerequisites

Install the following software:

- Python 3.11 or a compatible version
- Git
- SWI-Prolog

On macOS, install SWI-Prolog using Homebrew:

```bash
brew install swi-prolog
```

Verify the installation:

```bash
swipl --version
```

## Installation

Clone the repository:

```bash
git clone https://gitlab.com/JaidenWolete/professor-knowledge-system.git
cd professor-knowledge-system
```

Create and activate a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the project dependencies:

```bash
python3 -m pip install -r requirements.txt
```

## Preparing the Knowledge Base

The source data is stored in the `data/` directory. The parser scripts generate Prolog facts in the `prolog/` directory.

Run the parsers from the project root:

```bash
python3 parser/yaml_parser.py
python3 parser/schedule_parser.py
python3 parser/syllabus_parser.py
```

The scripts generate the following files:

- `prolog/professors.pl` — professor details from YAML.
- `prolog/schedule.pl` — course and scheduling information from Excel.
- `prolog/syllabus.pl` — course and instructor information from syllabus documents.

Ensure the expected source files are present in `data/` before running the parsers.

## Running the Chatbot

Activate the virtual environment if it is not already active:

```bash
source venv/bin/activate
```

Start the application:

```bash
python3 app/chatbot.py
```

Enter a question when prompted by the chatbot.

### Example Questions

- Which courses does Anthony Adedoyin teach?
- Which courses does Appolo Tankeh teach?
- Who teaches CTEC 350.170?
- What room is CTEC 350.170 in?
- What days does CTEC 350.170 meet?
- What time does CTEC 350.170 meet?
- What is the email address of Appolo Tankeh?
- What department does Anthony Adedoyin belong to?
- What are Appolo Tankeh's specialties?

Responses depend on the information available in the knowledge base.

## Testing

### Test the Python–Prolog Connection

Run:

```bash
python3 test_prolog.py
```

This test checks whether PySwip can be imported and a Prolog interface object can be created.

### Check Prolog Files

Run these commands from the project root:

```bash
swipl -q -t halt -s prolog/professors.pl
swipl -q -t halt -s prolog/schedule.pl
swipl -q -t halt -s prolog/syllabus.pl
swipl -q -t halt -s prolog/rules.pl
```

These commands check whether each file loads without reporting a Prolog error. They do not verify the correctness of every query.

### GitLab CI/CD

The `.gitlab-ci.yml` configuration runs automated checks in a Python 3.11 environment. It installs dependencies from `requirements.txt`, checks Python imports, and compiles project scripts to identify syntax errors.

The current configuration does not run full end-to-end Prolog integration tests.

## Knowledge Representation

The system represents academic information using Prolog facts and rules.

| Predicate | Description |
|---|---|
| `professor/1` | Identifies a professor |
| `department/2` | Associates a professor with a department |
| `office/2` | Stores a professor's office |
| `email/2` | Stores a professor's email address |
| `specialty/2` | Records a professor's specialty |
| `course/2` | Associates a course code with its title |
| `teaches/2` | Connects a professor to a course |
| `days/2` | Stores course meeting days |
| `room/2` | Stores the course room |
| `time/3` | Stores the course start and end times |

Rules defined in `prolog/rules.pl` provide reusable queries over these facts.

## Data Sources

The system uses academic information from:

- `data/professors.yaml`
- The Fall 2026 CTEC course schedule spreadsheet
- Course syllabus documents in the `data/` directory

The generated knowledge base depends on the accuracy and completeness of these source files.

## Author

Jaiden Wolete & Reuben Odedairo

## Repository

[Professor Knowledge Expert System on GitLab](https://gitlab.com/JaidenWolete/professor-knowledge-system)


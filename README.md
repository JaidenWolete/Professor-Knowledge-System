# Professor Knowledge Expert System

## Project Overview

The Professor Knowledge Expert System is a Python and Prolog-based question-answering application developed for COSC 369. It allows users to ask questions about professors and courses using an interactive command-line chatbot.

The system uses Prolog facts and rules to retrieve information from the project's professor, course schedule, and syllabus data.

## Features

- List professors in the knowledge base.
- Find courses taught by a professor.
- Identify the instructor of a course.
- Retrieve course meeting days and times.
- Find classroom locations.
- Look up professor email addresses and office locations.
- Retrieve professor specialties.
- Answer questions using an interactive command-line interface.

## Technologies

- Python
- SWI-Prolog
- PySwip
- YAML, Excel, and DOCX processing tools, where used by the project

## Running the Application

From the root of the project, run:

```bash
python3 app/chatbot.py
```

Ask questions at the command-line prompt. For example:

- `Which courses does Anthony Adedoyin teach?`
- `Who teaches CTEC 350.170?`
- `What room is CTEC 350.170 in?`
- `What days does CTEC 350.170 meet?`
- `What time does CTEC 350.170 meet?`
- `What is Appolo Tankeh's email?`

Type `quit` to exit the chatbot.

## Project Structure

- `app/` — Chatbot application.
- `data/` — Source files containing professor, schedule, and syllabus information.
- `parser/` — Scripts for processing source data.
- `prolog/` — Prolog facts and rules used by the knowledge system.
- `requirements.txt` — Python dependencies.
- `test_prolog.py` — Prolog-related tests, if applicable.
- `.gitlab-ci.yml` — GitLab CI/CD configuration.

## Data and Knowledge Base

The application loads Prolog knowledge from the files in `prolog/`, including professor information, course schedules, syllabus information, and inference rules. The available answers depend on the facts loaded into the knowledge base.

## Testing

Run the project's Prolog test script from the project root:

```bash
python3 test_prolog.py
```

Ensure that SWI-Prolog and the required Python dependencies are installed before running the application or tests.

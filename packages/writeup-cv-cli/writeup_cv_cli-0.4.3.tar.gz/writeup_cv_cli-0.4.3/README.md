![image](https://github.com/user-attachments/assets/fbd23f54-9491-45b0-b75d-804f871342c7)

# Writeup - Software Engineering Project - 22916 2025A

Command-line interface (CLI) tool designed to analyze CVs (curriculum vitae) in PDF format. It allows users, particularly HR professionals, to evaluate CVs against specific job descriptions. The tool provides a match score, highlights relevant skills, and generates a summary of the candidate's suitability for the role. The analysis can be performed for individual CVs or in batch mode for multiple CVs in a directory. The project leverages Gemini APIs for advanced text analysis and supports output in JSON or PDF format or displaying in terminal.

## Authors

| Contributor                                      | GitHub Profile                              |
| ------------------------------------------------ | ------------------------------------------- |
| [@dolev146](https://www.github.com/dolev146)     | [GitHub](https://www.github.com/dolev146)   |
| [@shimshon21](https://www.github.com/shimshon21) | [GitHub](https://www.github.com/shimshon21) |
| [@yakov103](https://www.github.com/yakov103)     | [GitHub](https://www.github.com/yakov103)   |

## Phase 1: Requirements Engineering

[llm_link_to_chat_phase_1](./chats/phase1.txt)

###

 Consult with an LLM to define ONE significant and interesting CV analysis feature.

prompt : "I am a software developer developing a terminal Python app that gets a CV (curriculum vitae) PDF file as input and a text prompt from the user, for example, "Does this CV match the iOS developer?" I want to consult with you about what could be a significant and interesting analysis feature I can implement in my software. Document the feature's requirements clearly. Include acceptance criteria.
The users of our software will be Human resources trying to find the best job applicant by role, seniority and relevent skills."

### Document the feature's requirements clearly.

### Feature Overview

#### Feature Name

Role Matching & Competency Analysis

#### Description:

The Role Matching & Competency Analysis feature takes a PDF CV and a text prompt describing the job role (e.g., “iOS Developer” or specific requirement job post. It then analyzes the CV content for skills, experiences, and qualifications relevant to that role. The outcome are:

- Numerical score between 0 - 10
- Years of Experience
- Summary
- Relevent skills
- Other skills
- Pros
- Cons

### User Stories

As an HR professional, I want to input a CV and a prompt describing the job position so that I can receive a quick assessment of how well the CV matches the role.
As an HR professional, I want to see a breakdown of relevant skills and experiences extracted from the CV so that I can understand the candidate's strengths and areas where they might fall short.
As an HR professional, I want a confidence or match score that summarizes the overall fit so that I can compare multiple applicants easily.

### Functional Requirements

1. File Parsing & Text Extraction
   Accept PDF input via command line, extract text reliably (up to ~10 pages).

2. Scoring Mechanism
   Generate a 0-10 score based on keyword frequency, critical experience, and years of experience.

3. Skills
   Generate Relevant skills which most likley will be required for the position.
   And other skill which might be less relvevant for the position.

4. Pros and Cons
   Generate all positive aspects and negative points as well.

#### Non-Functional Requirements

1. Performance

The system should provide results for a typical 2–5 page CV within a few seconds.
Larger CVs (up to ~10 pages) should be processed within an acceptable time (under 30 seconds, for example).

2. Reliability

The system should reliably parse PDFs with standard text. If the PDF is scanned or image-based, the system may return an error or a warning unless Optical Character Recognition (OCR) is implemented.

3. Maintainability

The code should be modular, with separate functions for PDF parsing, text analysis, scoring, and summarization, allowing for easy updates or improvements to each component.

4. Scalability

The feature should be designed so that new skills or roles can be added easily to the matching algorithm (e.g., by adding or updating a skills dictionary or training an NLP model).

### Include acceptance criteria

### Acceptance Criteria

#### 1. CV Input & Prompt Capture

Given a valid PDF file path and a relevant prompt,
when the user runs the software in the terminal,
then the software extracts text from the PDF and processes the prompt without error.\*\*

#### 2. Analysis & Scoring

**Acceptence Criteria 1:**
Given a valid PDF that includes role (e.g:“iOS developer”) and seniority(e.g: Junior) ,
when the user runs the analysis,
then the system outputs:
A match score between 0 and 10,
A Years of Experience,
A short textual summary describing the candidate’s suitability,
A list of detected relevant skills (e.g., “Swift,” “Objective-C,” “UIKit”),
A list of other relevant skills (e.g., “Java,” “Kotlin,” “Android”),
A list of Pros,
A list of Cons.

**Acceptence Criteria 2:** Given a valid PDF that lacks any relevant skills for the prompt,
when the user runs the analysis,
then the system outputs a low match score (e.g., near 0) and indicates no relevant skills found.
Invalid CV or Prompt

**Acceptence Criteria 3(not implemented):** Given an invalid or non-existent PDF file path,
when the user runs the software,
then the system provides an error message and does not crash.
Given an empty or nonsensical prompt (e.g., “asdfghjk”),
when the user runs the software,
then the system warns the user that the role could not be identified and proceeds with minimal or no matching.
Performance

**Acceptence Criteria 4:** Given a CV of ~5 pages,
when the user runs the analysis,
then the system should return results within a few seconds (e.g., under 20 seconds).

- Document LLM interactions (link).
  [chat](https://chatgpt.com/share/67c1dfc9-f7a8-8011-8a50-cec0dd751f5f)

## Phase 2: Architecture

### Define Command-Line Interface Specification (Inline)

#### CLI Commands

##### `writeup evaluate`

Evaluates a single CV PDF against a specific position and seniority level, optionally overriding the default API key. Generates a structured report in either JSON or PDF format.

#### Usage

```zsh
writeup evaluate [OPTIONS] FILE
```

#### Description

- **FILE** (Positional Argument, Required)  
  Path to the CV PDF file that you want to evaluate.

#### Options

- **`--position, -p (TEXT, Required)`**  
  The name/title of the position you are evaluating for (e.g., "Software Engineer").

- **`--seniority, -s (TEXT, Required)`**  
  The seniority level of the position (e.g., "Mid-Level," "Senior," etc.).

- **`--output, -o (TEXT)`**  
  The output file name for the generated report.  
  If omitted, a default name is used:

  - **`evaluation_report.json`** if `--format json`
  - **`evaluation_report.pdf`** if `--format pdf`

- **`--format, -f (TEXT, default: json)`**  
  The report format. Choose **json** or **pdf**.

- **`--api-key, -t (TEXT)`**  
  An optional override for the `GEMINI_API_KEY` environment variable.  
  Use this if you do not want to rely on the API key from `.env`.

- **`--help`**  
  Displays usage information and exits.

#### Example

```
writeup evaluate resume.pdf -p "Data Scientist" -s "Senior" --format pdf
```

This command evaluates `resume.pdf` for a **Senior Data Scientist** role, then creates and saves a PDF report (by default, named `evaluation_report.pdf`).

### Plan file system interactions, i.e., input/output (inline).

### Inputs

- The system accepts **PDF files** as input.
- Input files can be specified using a **file path** or directory path.
- When evaluating multiple files in a batch, the system will scan the specified directory for files matching the `.pdf` extension.
- The input file(s) must be accessible and readable by the system.

### Outputs:

- Output files are generated in **JSON** or **PDF** format.
- The default output file name follows this pattern:

  - **`evaluation_report.json`** – for single-file JSON reports
  - **`evaluation_report.pdf`** – for single-file PDF reports
  - **`batch_evaluation_report.json`** – for batch JSON reports
  - **`batch_evaluation_report.pdf`** – for batch PDF reports

- If an output filename is specified using the `--output` option, the system will override the default name.

### Your feature may use additional files for input and output.

**A .env file** or config file could store default API_KEY and other environment variables.

**A logs** directory could store logs if needed for debugging or usage reporting.

### Identify relevant third-party libraries.

**Typer**

For easy and intuitive CLI creation.

**Poetry**

Dependency management and project packaging.

**Curl**

For requests

**Google-Genai**
For Pdf analysis

### Define team member responsibilities.

| User                                             | Responsibilitiy                                           |
| ------------------------------------------------ | --------------------------------------------------------- |
| [@dolev146](https://www.github.com/dolev146)     | Reasearch & Communication with Google api                 |
| [@shimshon21](https://www.github.com/shimshon21) | Export to pdf & Third libraries managment & Documentation |
| [@yakov103](https://www.github.com/yakov103)     | Infrastucture & Data flow                                 |

**_LLM Interactions:_**
[chat](https://chatgpt.com/share/67c30550-6034-800a-be83-a438dda7406d)

## Phase 3: Design
### 🧠 CRC: Classes, Responsibilities, and Collaborations

A structured overview of the main classes, their core responsibilities, and their collaborators in the system.

---

#### 🧑‍💻 CLI Interface

| 🔧 Class | 📌 Responsibilities | 🤝 Collaborations |
|---------|---------------------|-------------------|
| **CLIHandler**<br/>([cli.py](./writeup/cli.py)) | - Parse command-line arguments (file path, position, seniority, output format).<br/>- Orchestrate the application's flow.<br/>- Handle user interaction and terminal output. | - Calls [Analyzer](./writeup/core/evaluator.py)<br/>- Uses [JsonExporter](./writeup/reports/json_report.py) and [PDFExporter](./writeup/reports/pdf_report.py)<br/>- Interacts with [Feedback](./writeup/core/models.py) |

---

#### 🧰 Core Logic

| 🔧 Class | 📌 Responsibilities | 🤝 Collaborations |
|---------|---------------------|-------------------|
| **Analyzer**<br/>([evaluator.py](./writeup/core/evaluator.py)) | - Evaluate CVs using the Gemini API.<br/>- Generate structured feedback (score, skills, pros, cons).<br/>- Support batch evaluations. | - Uses [Feedback](./writeup/core/models.py)<br/>- Interacts with [TextPreprocessor](#textpreprocessor)<br/>- Uses Gemini API |
---

#### 📦 Data Models

| 🔧 Class | 📌 Responsibilities | 🤝 Collaborations |
|---------|---------------------|-------------------|
| **Feedback**<br/>([models.py](./writeup/core/models.py)) | - Represent the structured output from the LLM (e.g., score, summary, skills).<br/>- Serve as a data model for reports. | - Used by [Analyzer](./writeup/core/evaluator.py)<br/>- Passed to [JsonExporter](./writeup/reports/json_report.py) and [PDFExporter](./writeup/reports/pdf_report.py) |

---

#### 📤 Reporting / Exporters

| 🔧 Class | 📌 Responsibilities | 🤝 Collaborations |
|---------|---------------------|-------------------|
| **JsonExporter**<br/>([json_report.py](./writeup/reports/json_report.py)) | - Generate and save evaluation results as JSON.<br/>- Support single and batch exports. | - Receives [Feedback](./writeup/core/models.py)<br/>- Called by [CLIHandler](./writeup/cli.py) |
| **PDFExporter**<br/>([pdf_report.py](./writeup/reports/pdf_report.py)) | - Generate a PDF report using LLM output. | - Called by [CLIHandler](./writeup/cli.py)<br/>- Receives [Feedback](./writeup/core/models.py) |

---

## Phase 4: Coding & Testing

### Files table:

| Directory          | File Name                                                | Description                                                                   |
| ------------------ | -------------------------------------------------------- | ----------------------------------------------------------------------------- |
| writeup            | [cli.py](./writeup/cli.py)                               | Get user input and return output in Json/PDF/Console format                   |
| writeup -> core    | [evaluator.py](./writeup/core/evaluator.py)              | Fetch response from LLM by given prompt of user required experience seniority |
|                    | [models.py](./writeup/core/models.py)                    | Store models fetched from the LLM                                             |
| writeup -> reports | [json_report.py](./writeup/reports/json_report.py)       | Export LLM response into Json file format                                     |
|                    | [pdf_report.py](./writeup/reports/pdf_report.py)         | Export LLM response into PDF file format                                      |
| writeup -> utils   | [text_utils.py](./writeup/utils/text_utils.py)           | UI text utils for drawing break lines                                         |
| writeup -> tests   | [conftest.py](./tests/conftest.py)                       | Tests configuration file                                                      |
|                    | [test_batch_evaluate.py](./tests/test_batch_evaluate.py) | Batch evaluate tests                                                          |
|                    | [test_evaluate.py](./tests/test_evaluate.py)             | Evaluate tests for multiple mock pdf files                                    |

### Testing

We use `pytest` as our testing framework. Below are the details of the tests implemented:

#### Test Configuration ([conftest.py](./tests/conftest.py))

- **gemini_api_key**: A fixture that retrieves the `GEMINI_API_KEY` environment variable. If the key is not provided, it skips tests that require a real API call.
- **cv_dir**: A fixture that provides the path to the `cv` directory, which is assumed to be located one level above the `tests` directory.

#### Batch Evaluate Tests ([test_batch_evaluate.py](./tests/test_evaluate.py))

These tests are designed to evaluate the functionality of batch processing multiple CV PDFs in a directory.

- **test_batch_evaluate_success**: Tests the successful evaluation of multiple CV PDFs in a directory and checks if the batch report is generated correctly.
- **test_batch_evaluate_no_files**: Tests the scenario where no PDF files are found in the specified directory and ensures the appropriate error message is displayed.
- **test_batch_evaluate_invalid_api_key**: Tests the scenario where an invalid API key is provided and ensures the appropriate error message is displayed.

#### Evaluate Tests (`test_evaluate.py`)

These tests are designed to evaluate the functionality of processing a single CV PDF.

- **test_evaluate_success**: Tests the successful evaluation of a single CV PDF and checks if the report is generated correctly.
- **test_evaluate_file_not_found**: Tests the scenario where the specified CV PDF file is not found and ensures the appropriate error message is displayed.
- **test_evaluate_invalid_api_key**: Tests the scenario where an invalid API key is provided and ensures the appropriate error message is displayed.
- **test_evaluate_invalid_format**: Tests the scenario where an invalid report format is specified and ensures the appropriate error message is displayed.

### Running Tests

To run the tests, use the following command:

```bash
poetry run pytest
```

This command will execute all the tests in the `tests` directory and provide a summary of the test results.

## Phase 5: Documentation

### Project Overview

The Writeup project is a CLI tool designed for HR professionals to analyze CVs in PDF format. It evaluates CVs against job descriptions, providing a match score, relevant skills, years of experience, and a summary of the candidate's suitability. The tool supports batch processing, JSON/PDF output, and leverages Gemini APIs for advanced text analysis. It is modular, scalable, and optimized for performance.

#### Project Structure

```bash
.
├── README.md
├── evaluation_report.json
├── poetry.lock
├── pyproject.toml
├── tests
│   ├── conftest.py
│   ├── test_batch_evaluate.py
│   └── test_evaluate.py
└── writeup
    ├── cli.py
    ├── core
    │   ├── evaluator.py
    │   └── models.py
    ├── reports
    │   ├── json_report.py
    │   └── pdf_report.py
    └── utils
        └── text_utils.py

6 directories, 13 files

```

## Demo
Evaluate feature demo:

https://github.com/user-attachments/assets/1fef6e6f-c038-4f56-b554-e2a75cb2e037

## Installation

```zsh

  pipx install writeup-cv-cli

```

## Usage

After installing, you can run the CLI command as follows:

```bash
writeup evaluate --pdf-path path/to/cv.pdf -t <gemini_token>
```

This command scans and analyzes the provided CV PDF file and outputs an analysis report.

## Development

- **Run Tests:**

  ```bash

  poetry run pytest

  ```

- **LLM Interactions:** Save all LLM chats in the [chats/](./chats/) directory.

## Screenshots
PDF Example:

![alt text](/screenshots/cv-example.png)

Analyzer Output: 

![Analyzer output](/screenshots/output_example.png)

Analyzer JSON Output:

![alt text](/screenshots/json_output.png)

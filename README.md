# Schedule Converter

## Description
The Schedule Converter is a Python application that converts textual schedule descriptions into AIXM 5.1.1 XML format for aeronautical information systems. It reads schedules from a text file, validates their format, processes them using the Gemini API (or a mock response for testing), and outputs formatted XML to a file.

## Features
- Reads schedule text from `input.txt` with strict format validation.
- Generates formatted AIXM XML and writes it to `output.xml`.
- Configurable via `.env` for API key and file paths.
- Robust error handling and logging.
- Supports mock API responses for debugging.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/semahkadri/Schedule-Converter.git
   cd Schedule-Converter

2. Create a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

4. Create a `.env` file with:
GEMINI_API_KEY=your_api_key
INPUT_FILE=input.txt
OUTPUT_FILE=output.xml

5. Add schedule text to `input.txt` (e.g., `MON-FRI: 0800-1800, SAT: 0800-1200`).

## Usage
Run the script:
`python main.py`

- Output: Formatted AIXM XML in output.xml.
- Logs: Check app.log for execution details.

## Overview
The Schedule Converter is a Python application designed to convert textual schedule descriptions used in aeronautical information systems into AIXM 5.1.1 XML format. It reads strictly formatted schedules from a text file, validates their format, processes them using the Gemini API (or a mock response for testing), and outputs formatted XML to a file, facilitating automation for the Service de l'Information Aéronautique (SIA).

**Repository**: [https://github.com/semahkadri/Schedule-Converter](https://github.com/semahkadri/Schedule-Converter)

## Solution Description
- **Purpose**: Automate the conversion of human-readable schedules (e.g., "MON-FRI: 0800-1800, SAT: 0800-1200") into AIXM XML, ensuring only valid inputs are processed.
- **Components**:
  - **Input**: Schedule text read from a file specified in `.env` (e.g., `input.txt`). Input must follow a strict format (e.g., `DAY: HHMM-HHMM`, with valid days and times).
  - **Validation**: A regex-based validator checks that the input matches expected patterns (e.g., valid days like `MON-FRI`, `SAT`, `Every day` and times like `0800-1800`).
  - **Processing**: The `ScheduleConverter` class:
    1. **Parsing**: Converts validated text into JSON dictionaries using the Gemini API (or mock).
    2. **Validation**: Ensures JSON includes required fields (`timeReference`, `startDate`, `endDate`, `day`, `startTime`, `endTime`).
    3. **XML Generation**: Produces formatted AIXM XML with proper indentation using `xml.etree.ElementTree` and `xml.dom.minidom`.
  - **Output**: Formatted AIXM XML written to a file specified in `.env` (e.g., `output.xml`) and logged.

## Project Structure
- `config/config.py`: Loads API key and file paths from `.env`.
- `utils/logging_config.py`: Configures logging to console and `app.log`.
- `models/schedule_converter.py`: Contains the `ScheduleConverter` class for parsing and XML generation.
- `main.py`: Reads input file, validates schedule text, runs conversion, and writes output file.
- `input.txt`: Contains the schedule text (e.g., "MON-FRI: 0800-1800, SAT: 0800-1200").
- `.env`: Stores `GEMINI_API_KEY`, `INPUT_FILE`, and `OUTPUT_FILE`.
- `requirements.txt`: Lists dependencies (`google-generativeai`, `python-dotenv`).
- `.gitignore`: Excludes `.env`, `app.log`, `output.xml`, and `__pycache__`.
- `README.md`: Project overview and instructions.

## Execution Flow
1. **Initialization**:
   - Load API key and file paths from `.env`.
   - Set up logging.
2. **Input**:
   - Read schedule text from the input file (e.g., `input.txt`).
3. **Validation**:
   - Check that the schedule text matches the required format using regex and time validation.
   - Reject invalid inputs with an error message guiding the user.
4. **Conversion**:
   - Create a `ScheduleConverter` instance.
   - Parse validated text into JSON (mock or real API).
   - Generate formatted AIXM XML.
5. **Output**:
   - Write formatted XML to the output file (e.g., `output.xml`).
   - Log all steps and errors.

## Diagram
[Input File] → [Read Text] → [Validate Format] → [Gemini API/Mock] → [JSON Parsing] → [Validation] → [XML Generation] → [Formatted Output File]
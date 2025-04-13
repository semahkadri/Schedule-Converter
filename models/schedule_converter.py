import json
import xml.etree.ElementTree as ET
from typing import List, Dict
import google.generativeai as genai
import logging
import xml.dom.minidom

class ScheduleConverter:
    """A class to convert textual schedule descriptions into AIXM 5.1.1 XML format using the Gemini API."""

    def __init__(self, api_key: str) -> None:
        """Initialize the ScheduleConverter with a Gemini API key.

        Args:
            api_key (str): The API key for accessing the Gemini API.
        """
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.logger = logging.getLogger(__name__)

    def parse_schedule_text(self, text: str) -> List[Dict[str, str]]:
        """Parse a textual schedule description into a structured list of schedule dictionaries.

        Args:
            text (str): The textual schedule description.

        Returns:
            List[Dict[str, str]]: A list of dictionaries, each containing schedule details.

        Raises:
            ValueError: If the parsing fails.
        """
        USE_MOCK = True 
        if USE_MOCK:
            self.logger.info("Using mock response for debugging")
            mock_response = """
            [
                {"timeReference": "UTC", "startDate": "01-01", "endDate": "31-12", "day": "WORK DAY", "startTime": "08:00", "endTime": "18:00"},
                {"timeReference": "UTC", "startDate": "01-01", "endDate": "31-12", "day": "SAT", "startTime": "08:00", "endTime": "12:00"}
            ]
            """
            return json.loads(mock_response)
        else:
            prompt = self._create_prompt(text)
            try:
                response = self.model.generate_content(prompt)
                self.logger.info(f"Raw API response: {response.text}")
                schedules = json.loads(response.text)
                if not isinstance(schedules, list):
                    raise ValueError("Expected a JSON list from LLM response")
                
                required_keys = {'timeReference', 'startDate', 'endDate', 'day', 'startTime', 'endTime'}
                for i, sched in enumerate(schedules):
                    if not isinstance(sched, dict):
                        raise ValueError(f"Schedule {i} is not a dictionary")
                    missing = required_keys - set(sched.keys())
                    if missing:
                        raise ValueError(f"Schedule {i} is missing keys: {missing}")
                
                return schedules
            except json.JSONDecodeError as e:
                self.logger.error(f"JSON decode error: {e}")
                raise ValueError("Failed to parse LLM response as JSON")
            except Exception as e:
                self.logger.error(f"Error parsing schedule text: {e}")
                raise

    def generate_aixm_xml(self, schedules: List[Dict[str, str]]) -> str:
        """Generate a formatted AIXM 5.1.1 XML string from a list of schedule dictionaries.

        Args:
            schedules (List[Dict[str, str]]): List of schedule periods.

        Returns:
            str: The formatted AIXM XML string with indentation.
        """
        try:
            root = ET.Element('PropertiesWithSchedule')
            for sched in schedules:
                time_interval = ET.SubElement(root, 'timeInterval')
                timesheet = ET.SubElement(time_interval, 'Timesheet')
                ET.SubElement(timesheet, 'timeReference').text = sched.get('timeReference', 'UTC')
                ET.SubElement(timesheet, 'startDate').text = sched.get('startDate', '01-01')
                ET.SubElement(timesheet, 'endDate').text = sched.get('endDate', '31-12')
                ET.SubElement(timesheet, 'day').text = sched.get('day', 'EVERY DAY')
                ET.SubElement(timesheet, 'startTime').text = sched.get('startTime', '00:00')
                ET.SubElement(timesheet, 'endTime').text = sched.get('endTime', '23:59')
            
            rough_string = ET.tostring(root, encoding='unicode')
            parsed = xml.dom.minidom.parseString(rough_string)
            pretty_xml = parsed.toprettyxml(indent="  ", encoding=None)
            pretty_xml = '\n'.join(line for line in pretty_xml.split('\n') if line.strip() and not line.startswith('<?xml'))
            return pretty_xml.strip()
        except KeyError as e:
            self.logger.error(f"Missing key in schedule dictionary: {e}")
            raise ValueError(f"Invalid schedule data: missing key {e}")
        except Exception as e:
            self.logger.error(f"Error generating AIXM XML: {e}")
            raise

    def convert_text_to_aixm(self, text: str) -> str:
        """Convert a textual schedule description directly into an AIXM 5.1.1 XML string.

        Args:
            text (str): The textual schedule description.

        Returns:
            str: The AIXM XML string.

        Raises:
            ValueError: If parsing the schedule text fails.
        """
        try:
            schedules = self.parse_schedule_text(text)
            return self.generate_aixm_xml(schedules)
        except Exception as e:
            self.logger.error(f"Error converting text to AIXM: {e}")
            raise

    def _create_prompt(self, text: str) -> str:
        """Create a prompt for the Gemini API to parse the schedule text into JSON.

        Args:
            text (str): The textual schedule description.

        Returns:
            str: A formatted prompt string with examples and the input text.
        """
        prompt_template = """
You are an assistant that converts textual schedule descriptions into a structured JSON format 
for AIXM 5.1.1 Timesheets. Each schedule period must include the following keys:
- timeReference: always "UTC"
- startDate: "01-01" (unless specified otherwise)
- endDate: "31-12" (unless specified otherwise)
- day: a string representing the day or day group (e.g., "WORK DAY" for Monday to Friday, "SAT" for Saturday, "EVERY DAY" for all days)
- startTime: time in "HH:MM" format (e.g., "08:00")
- endTime: time in "HH:MM" format (e.g., "18:00")

Examples:
Text: "MON-FRI: 0800-1800, SAT: 0800-1200"
Output:
[
    {"timeReference": "UTC", "startDate": "01-01", "endDate": "31-12", "day": "WORK DAY", "startTime": "08:00", "endTime": "18:00"},
    {"timeReference": "UTC", "startDate": "01-01", "endDate": "31-12", "day": "SAT", "startTime": "08:00", "endTime": "12:00"}
]

Text: "Every day from 0900 to 1700"
Output:
[
    {"timeReference": "UTC", "startDate": "01-01", "endDate": "31-12", "day": "EVERY DAY", "startTime": "09:00", "endTime": "17:00"}
]

Now, convert the following text into a JSON list of dictionaries:
{}
"""
        return prompt_template.format(text)
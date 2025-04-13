from config.config import Config
from utils.logging_config import setup_logging
from models.schedule_converter import ScheduleConverter
import logging
import os
import re

def validate_schedule_text(text: str) -> bool:
    """Validate the schedule text format.

    Args:
        text (str): The schedule text to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    if not text.strip():
        return False
    
    pattern = r'^\s*(?:(?:MON-FRI|SUN-FRI|MON-SAT|SUN-SAT|MON|TUE|WED|THU|FRI|SAT|SUN|Every day)\s*:\s*\d{4}-\d{4})\s*(?:,\s*(?:(?:MON-FRI|SUN-FRI|MON-SAT|SUN-SAT|MON|TUE|WED|THU|FRI|SAT|SUN|Every day)\s*:\s*\d{4}-\d{4})\s*)*$'
    
    if not re.match(pattern, text):
        return False
    
    schedules = [s.strip() for s in text.split(',')]
    for sched in schedules:
        try:
            day_part, time_part = [p.strip() for p in sched.split(':')]
            start_time, end_time = [t.strip() for t in time_part.split('-')]
            if not (len(start_time) == 4 and len(end_time) == 4 and start_time.isdigit() and end_time.isdigit()):
                return False
            start_hour, start_min = int(start_time[:2]), int(start_time[2:])
            end_hour, end_min = int(end_time[:2]), int(end_time[2:])
            if not (0 <= start_hour <= 23 and 0 <= start_min <= 59 and 0 <= end_hour <= 23 and 0 <= end_min <= 59):
                return False
        except ValueError:
            return False
    
    return True

def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    api_key = Config.GEMINI_API_KEY
    input_file = Config.INPUT_FILE
    output_file = Config.OUTPUT_FILE

    if not api_key:
        logger.error("GEMINI_API_KEY is not set in the .env file.")
        return

    if not os.path.exists(input_file):
        logger.error(f"Input file {input_file} does not exist.")
        return

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            schedule_text = f.read().strip()
        logger.info(f"Read schedule text from {input_file}: {schedule_text}")
    except Exception as e:
        logger.error(f"Failed to read input file {input_file}: {e}")
        return

    if not validate_schedule_text(schedule_text):
        logger.error(
            f"Invalid schedule format in {input_file}. Expected format: "
            "'MON-FRI: HHMM-HHMM, SAT: HHMM-HHMM' or 'Every day: HHMM-HHMM', "
            "e.g., 'MON-FRI: 0800-1800, SAT: 0800-1200'"
        )
        return

    converter = ScheduleConverter(api_key)
    try:
        xml_output = converter.convert_text_to_aixm(schedule_text)
        logger.info("Generated AIXM XML successfully")
    except ValueError as e:
        logger.error(f"Conversion error: {e}")
        return
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(xml_output)
        logger.info(f"Wrote AIXM XML to {output_file}")
    except Exception as e:
        logger.error(f"Failed to write output file {output_file}: {e}")
        return

if __name__ == "__main__":
    main()
from config.config import Config
from utils.logging_config import setup_logging
from models.schedule_converter import ScheduleConverter
import logging
import os

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
from config.config import Config
from utils.logging_config import setup_logging
from models.schedule_converter import ScheduleConverter
import logging

def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    api_key = Config.GEMINI_API_KEY
    if not api_key:
        logger.error("GEMINI_API_KEY is not set in the .env file.")
        return

    converter = ScheduleConverter(api_key)
    schedule_text = "MON-FRI: 0800-1800, SAT: 0800-1200"

    try:
        xml_output = converter.convert_text_to_aixm(schedule_text)
        logger.info("Generated AIXM XML:\n%s", xml_output)
    except ValueError as e:
        logger.error("Conversion error: %s", e)
    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)

if __name__ == "__main__":
    main()
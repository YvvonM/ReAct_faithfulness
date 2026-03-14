import wikipedia
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

class Wikipedia:
    def run(self, search_term: str) -> str:
        try:
            result = wikipedia.summary(search_term)[:1020]
            return result
        except wikipedia.exceptions.DisambiguationError as e:
            result = wikipedia.summary(e.options[0])[:1020]
            return result
        except Exception as e:
            logger.warning(f"An error occurred: {e}")
            return f"An error occurred: {e}"
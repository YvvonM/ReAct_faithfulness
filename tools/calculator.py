from sympy import sympify
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

class Calculator:
    def run(self, expression: str) -> str:
        try:
            result = sympify(expression)
            return str(result)
        except Exception as e:
            logger.warning(f"An error occured: {e}")
            return f"An error occurred: {e}"




    
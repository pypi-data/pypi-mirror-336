# Metadata for the package
__version__ = "4.0.0"  # Version of the package
__author__ = "John Doe"  # Your name or the author's name
__email__ = "efexzium@gmail.com"  # Contact email
__license__ = "MIT"  # License under which the package is distributed
__description__ = "A Python package for managing Ollama environments."

# # Expose modules or functions for easier imports
# from .ollamax import function1, Class1

# Optional: You can add logs or initialization logic here
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("ollamax package initialized successfully")
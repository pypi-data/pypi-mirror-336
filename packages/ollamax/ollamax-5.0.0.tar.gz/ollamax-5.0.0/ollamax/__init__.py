# Metadata for the package
__version__ = "5.0.0"  # Version of the package
__author__ = "John Doe"  # Your name or the author's name
__email__ = "efexzium@gmail.com"  # Contact email
__license__ = "MIT"  # License under which the package is distributed
__description__ = "A Python package for managing Ollama environments."

# # Expose modules or functions for easier imports
from .ollamax import OllamaService

# Optional: You can add logs or initialization logic here
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("ollamax package initialized successfully")
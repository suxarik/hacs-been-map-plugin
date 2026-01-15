"""Debug configuration for Been Map integration."""
import logging

# Set up detailed logging
logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger("been_map")
_LOGGER.setLevel(logging.DEBUG)

# Create file handler for debugging
file_handler = logging.FileHandler("/tmp/been_map_debug.log")
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
_LOGGER.addHandler(file_handler)

print("Debug logging configured. Logs will be saved to /tmp/been_map_debug.log")

import logging

# Set up logging configuration
def setup_logging():
    # Define the log format with timestamp, log level, and custom tag
    log_format = "%(asctime)s [%(levelname)s] - %(message)s"
    logging.basicConfig(
        format=log_format, 
        level=logging.DEBUG,   # You can change this to INFO, WARNING, ERROR, etc.
        handlers=[logging.StreamHandler()]  # Output to console
    )
import logging

# Set up logging configuration
def setup_logging():
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    # Define the log format with timestamp, log level, and custom tag
    log_format = "%(asctime)s [%(levelname)s] - %(message)s"
    logging.basicConfig(
        format=log_format, 
        level=logging.debug,   # You can change this to INFO, WARNING, ERROR, etc.
        handlers=[logging.StreamHandler()]  # Output to console
    )

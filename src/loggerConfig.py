import logging
import os
import sys


def setup_logging():
    """
    Configures logging to output to both the console and a file.
    """
    # Create a 'logs' directory if it doesn't exist
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, 'app.log')

    # Configure the root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),        # Log to the file
            logging.StreamHandler(sys.stdout)   # Log to the console
        ]
    )

    logging.info("Logging configured successfully.")
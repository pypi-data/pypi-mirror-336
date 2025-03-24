import os
import socket
import sys

LOG_DIR = "logs"
DEFAULT_LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Store default metadata to ensure it's applied consistently
DEFAULT_METADATA = {"program": sys.argv[0], "hostname": socket.gethostname()}

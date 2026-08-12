import secrets
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
LOGO_PATH = r"C:\Users\12797\Music\Data Link MONTh\Screenshot 2025-09-10 170918.png"
FALLBACK_LOGO = r"C:\Users\12797\Music\Final CODE OF MQTT\fallback.png"

# Security
SECRET_KEY = secrets.token_hex(32)

# Server
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8090
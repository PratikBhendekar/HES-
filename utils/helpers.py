import base64
from pathlib import Path

def load_logo(path):
    """Load and encode logo image"""
    fallback_path = r"C:\Users\12797\Music\Final CODE OF MQTT\fallback.png"
    try:
        if Path(path).exists():
            with open(path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
            return f"data:image/png;base64,{encoded}"
        else:
            if Path(fallback_path).exists():
                with open(fallback_path, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode()
                return f"data:image/png;base64,{encoded}"
            return ""
    except Exception as e:
        print(f"Error loading logo: {e}")
        return ""
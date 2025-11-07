import logging
from core.app import GraphicsApp

# Configure logging
logging.basicConfig(level=logging.INFO)

# Application constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

if __name__ == "__main__":
    app = GraphicsApp(WINDOW_WIDTH, WINDOW_HEIGHT)
    app.run()
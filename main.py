import logging

from core.app import GraphicsApp


def main() -> None:
    """Entry point for the OpenGL Paint application."""
    logging.basicConfig(level=logging.INFO)

    window_width = 800
    window_height = 800

    app = GraphicsApp(window_width, window_height)
    app.run()


if __name__ == "__main__":
    main()
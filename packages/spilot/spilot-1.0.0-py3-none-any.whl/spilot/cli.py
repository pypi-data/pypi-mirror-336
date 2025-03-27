"""
Command line interface for spilot
"""
import sys

def main():
    """Entry point for the application script"""
    try:
        from spilot.app import SlurmPilotApp
        app = SlurmPilotApp()
        app.run()
    except ImportError as e:
        print(f"Error: Required package not found. Please make sure textual is installed: {e}")
        print("You can install it with: pip install textual")
        sys.exit(1)
    except Exception as e:
        print(f"Error launching application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
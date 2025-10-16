
"""
Alternative entry point for Location Wizard
Redirects to Streamlit app
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit application"""
    print("🌍 Starting Location-Based Wind & Seismic Zone Wizard...")
    print("📍 For OsdagBridge - Interactive Map Interface")
    print("-" * 50)
    
    # Get the directory of this script
    app_dir = os.path.dirname(os.path.abspath(__file__))
    streamlit_app = os.path.join(app_dir, "streamlit_app.py")
    
    try:
        # Launch Streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", streamlit_app,
            "--server.port", "8501",
            "--server.address", "localhost"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f" Error launching Streamlit app: {e}")
        print(" Try running directly: streamlit run streamlit_app.py")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n Application stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
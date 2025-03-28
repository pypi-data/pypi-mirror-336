import win32com.client
import pythoncom
from win32com.client import gencache

TD_PROGID = 'ThinkDesign.Application'

def GetOrCreateApplication():
    """Get or Create TD application."""
    try:
        app = win32com.client.Dispatch(TD_PROGID)
        return app
    except Exception as e:
        print(f"Error to get or create TD application: {e}")
        return None
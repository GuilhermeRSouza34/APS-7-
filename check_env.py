import sys
import os

print("Python version:", sys.version)
print("Python executable:", sys.executable)
print("Current working directory:", os.getcwd())
print("\nTrying to import PyQt6...")
try:
    import PyQt6
    print("PyQt6 version:", PyQt6.__version__)
except ImportError as e:
    print("Error importing PyQt6:", str(e))

print("\nTrying to import tkinter...")
try:
    import tkinter
    print("Tkinter version:", tkinter.TkVersion)
except ImportError as e:
    print("Error importing tkinter:", str(e)) 
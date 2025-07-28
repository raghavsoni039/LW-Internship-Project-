import os
import webbrowser

def javascript_tasks():
    path = os.path.abspath("index.html")
    webbrowser.open(url=f"file://{path}")

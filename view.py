import webbrowser
import os

html_file = "test_output.html"
file_path = os.path.abspath(html_file)

# Open in the default browser
webbrowser.open(f"file://{file_path}")

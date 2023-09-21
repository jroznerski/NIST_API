import nbformat
from nbconvert import PythonExporter
import subprocess

def run_program(filename):
    result = subprocess.run(["python", filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
    if result.returncode == 0:
        print(f"{filename} został uruchomiony poprawnie.")
    else:
        print(f"{filename} nie został uruchomiony poprawnie. Błąd:\n{result.stderr}")

with open("my_json.ipynb", "r", encoding="utf-8") as nb_file:
    notebook = nbformat.read(nb_file, as_version=4)

exporter = PythonExporter()
python_code, _ = exporter.from_notebook_node(notebook)

with open("my_json.py", "w", encoding="utf-8") as py_file:
    py_file.write(python_code)

run_program("applications.py")

run_program("nist.py")

run_program("my_json.py")

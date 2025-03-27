import subprocess
import os
import io

params = ["python", f"{os.path.dirname(__file__)}\\test1.py"]
env = os.environ.copy()
env["PYTHONIOENCODING"] = "utf-8" 
proc = subprocess.Popen(params, env=env, stdout=subprocess.PIPE, text=True, bufsize=1)
while (line := proc.stdout.readline()) != "":
    print(line)
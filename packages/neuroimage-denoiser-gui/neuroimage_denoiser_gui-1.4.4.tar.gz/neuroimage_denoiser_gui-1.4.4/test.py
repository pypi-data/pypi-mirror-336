import subprocess, os
result = subprocess.run(["python", "-c", "print(1/7)"], capture_output=True, env=os.environ.copy())
print(result.stdout)
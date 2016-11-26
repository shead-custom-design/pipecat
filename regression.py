import subprocess

subprocess.call(["coverage", "run", "--append", "--source", "datacat", "-m", "behave"])
subprocess.call(["coverage", "report"])
subprocess.call(["coverage", "html", "--directory", ".cover"])

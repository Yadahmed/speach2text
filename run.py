import subprocess

# Run record.py in the background
record_process = subprocess.Popen(["python", "record.py"])

# Run transcribe.py in the foreground
transcribe_process = subprocess.Popen(["python", "transcribe.py"])

# Wait for transcribe.py to finish
transcribe_process.wait()

# Terminate the record.py process
record_process.terminate()

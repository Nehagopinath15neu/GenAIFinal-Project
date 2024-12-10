import subprocess
import time

# Command to run the Flask backend
backend_command = ["python", "app.py"]

# Command to run the Streamlit frontend
frontend_command = ["streamlit", "run", "frontend.py"]

# Start the Flask backend process
print("Starting the Flask backend...")
backend_process = subprocess.Popen(backend_command)

# Give the backend some time to start (adjust the sleep time if necessary)
time.sleep(5)

# Start the Streamlit frontend process
print("Starting the Streamlit frontend...")
frontend_process = subprocess.Popen(frontend_command)

# Wait for both processes to complete
try:
    backend_process.wait()
    frontend_process.wait()
except KeyboardInterrupt:
    print("\nShutting down both processes...")
    backend_process.terminate()
    frontend_process.terminate()

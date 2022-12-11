# This is to demonstrate how to kick off invokai in the background
import subprocess, os, time

invokeai = 'python scripts/metadata.py'
venv = os.environ.copy()
print('Starting InvokeAI')
process = subprocess.Popen(invokeai, env=venv, shell=True)

i = 1
while 1:
    if process.poll() is not None:
        print('InvokeAI has finished')
        break
    else:
        print(f'InvokeAI is still running, iteration {i}')
        i += 1
        time.sleep(30)
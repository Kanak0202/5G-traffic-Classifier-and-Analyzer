import time
import subprocess

while True:
    # Run the dis_3.py script
    subprocess.run(["python", "PacketAnalysis.py"])
    
    # Wait for 30 seconds
    time.sleep(5)

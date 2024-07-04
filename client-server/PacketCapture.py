import subprocess
import pymongo
import datetime
import time
from threading import Timer

# Connect to MongoDB
try:
    client = pymongo.MongoClient("your_mongoDB_URI") # update monogDB URI
    db = client["network_data"]
    collection = db["frames"]
except pymongo.errors.ConnectionError as e:
    print(f"Failed to connect to MongoDB: {e}")
    exit(1)

print("Begin capturing data")

# Define the tshark command to read from the pcap file
tshark_command = ["tshark", "-i", "eth0", "-d", "tcp.port==8000,http2", "-V"]

batch_size = 15
batch_data = []
flush_interval = 3  # seconds

def insert_batch(batch_data):
    if batch_data:
        try:
            collection.insert_many(batch_data)
            batch_data.clear()
        except pymongo.errors.BulkWriteError as e:
            print(f"Failed to insert batch: {e.details}")

def flush_batch():
    insert_batch(batch_data)
    Timer(flush_interval, flush_batch).start()

# Start the periodic flush
Timer(flush_interval, flush_batch).start()

try:
    with subprocess.Popen(tshark_command, stdout=subprocess.PIPE, text=True) as process:
        http2Flag = False
        frame_data = []
        arrival_time = ""

        for line in process.stdout:
            packet_data = line.strip()

            if "Arrival Time:" in packet_data and "Epoch Arrival Time:" not in packet_data and "UTC Arrival Time:" not in packet_data:
                arrival_time = packet_data.split("Arrival Time:")[1].strip()
            if "HyperText Transfer Protocol 2" in packet_data:
                http2Flag = True

            frame_data.append(packet_data)

            if packet_data == "":
                if frame_data and http2Flag:
                    document = {
                        "timestamp": datetime.datetime.now(datetime.timezone.utc),
                        "arrival_time": arrival_time,
                        "frame_data": "\n".join(frame_data),
                        "analyzed":False
                    }
                    batch_data.append(document)
                    http2Flag = False

                frame_data = []

                if len(batch_data) >= batch_size:
                    insert_batch(batch_data)

except KeyboardInterrupt:
    print("Exiting capture")

# Insert any remaining data
insert_batch(batch_data)

print("End of capture")

# Close the MongoDB client
client.close()

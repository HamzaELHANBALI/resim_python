import json
import matplotlib.pyplot as plt

# Define constants
TIME_TO_COLLISION_THRESHOLD = 2.0
INPUT_FILE = 'recorded_data.json'
OUTPUT_FILE = 'recorded_data_with_braking.json'

def check_emergency_brake(vehicle_speed, object_speed, object_position_x):
    relative_speed = vehicle_speed - object_speed
    if relative_speed <= 0:
        return False, float('inf')
    ttc = object_position_x / relative_speed
    return ttc < TIME_TO_COLLISION_THRESHOLD, ttc

# Read the recorded data and process it
with open(INPUT_FILE, 'r') as file:
    data = json.load(file)

vehicle_data = data['vehicle_data']
timestamps = []
ttc_values = []
emergency_brake_flags = []

for entry in vehicle_data:
    timestamps.append(entry['timestamp'])
    brake_flag, ttc = check_emergency_brake(entry['vehicle_speed'], entry['object_speed'], entry['object_position']['x'])
    emergency_brake_flags.append(brake_flag)
    ttc_values.append(ttc)
    entry['braking_state'] = brake_flag

# Create and show plots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

ax1.plot(timestamps, ttc_values, marker='o', linestyle='-', color='c', label='TTC')
ax1.axhline(y=TIME_TO_COLLISION_THRESHOLD, color='r', linestyle='--', label='TTC Threshold')
ax1.set_ylabel('Time to Collision (TTC)')
ax1.set_title('Time to Collision (TTC) Over Time')
ax1.legend()

ax2.plot(timestamps, emergency_brake_flags, marker='o', linestyle='-', color='r')
ax2.set_xlabel('Timestamp')
ax2.set_ylabel('Brake Signal (True/False)')
ax2.set_title('Emergency Braking Signal Over Time')

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Write the updated data to a new JSON file
with open(OUTPUT_FILE, 'w') as file:
    json.dump(data, file, indent=2)

print(f"New JSON file '{OUTPUT_FILE}' has been created with braking state information.")

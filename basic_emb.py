import json
import matplotlib.pyplot as plt

# Read the recorded data
with open('recorded_data.json', 'r') as file:
    data = json.load(file)

vehicle_data = data['vehicle_data']
timestamps = [entry['timestamp'] for entry in vehicle_data]
vehicle_speeds = [entry['vehicle_speed'] for entry in vehicle_data]
object_speeds = [entry['object_speed'] for entry in vehicle_data]
object_positions_x = [entry['object_position']['x'] for entry in vehicle_data]

# Define threshold for time to collision
TIME_TO_COLLISION_THRESHOLD = 2.0  # if TCC is below this value, then emergency braking is needed

# Function to determine if emergency braking is needed and calculate TTC
def check_emergency_brake(vehicle_speed, object_speed, object_position_x):
    relative_speed = vehicle_speed - object_speed
    if relative_speed > 0:
        time_to_collision = object_position_x / relative_speed
        if time_to_collision < TIME_TO_COLLISION_THRESHOLD:
            return 1, time_to_collision
        return 0, time_to_collision
    return 0, float('inf')

# Check for each data point if emergency braking is needed and calculate TTC
emergency_brake_flags = []
ttc_values = []

for i in range(len(vehicle_data)):
    brake_flag, ttc = check_emergency_brake(vehicle_speeds[i], object_speeds[i], object_positions_x[i])
    emergency_brake_flags.append(brake_flag)
    ttc_values.append(ttc)

# Create subplots
fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

# Plot TTC and TTC threshold
axs[0].plot(timestamps, ttc_values, marker='o', linestyle='-', color='c', label='TTC')
axs[0].axhline(y=TIME_TO_COLLISION_THRESHOLD, color='r', linestyle='--', label='TTC Threshold')
axs[0].set_ylabel('Time to Collision (TTC)')
axs[0].set_title('Time to Collision (TTC) Over Time')
axs[0].legend()

# Plot emergency braking signal
axs[1].plot(timestamps, emergency_brake_flags, marker='o', linestyle='-', color='r')
axs[1].set_xlabel('Timestamp')
axs[1].set_ylabel('Brake Signal (1 = ON, 0 = OFF)')
axs[1].set_title('Emergency Braking Signal Over Time')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

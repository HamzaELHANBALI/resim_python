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
weather_conditions = [entry['weather_condition'] for entry in vehicle_data]

# Define thresholds and factors
TIME_TO_COLLISION_THRESHOLD = 2.0  # Example time to collision threshold in seconds
DRIVER_REACTION_TIME = 1.5  # Average reaction time in seconds

# Function to determine if emergency braking is needed and calculate TTC
def check_emergency_brake(vehicle_speed, object_speed, object_position_x, weather, driver_reaction_time):
    relative_speed = vehicle_speed - object_speed
    if relative_speed > 0:
        time_to_collision = object_position_x / relative_speed
        
        # Adjust time to collision threshold based on weather
        if weather == 'wet':
            time_to_collision_threshold = TIME_TO_COLLISION_THRESHOLD * 1.5
        elif weather == 'icy':
            time_to_collision_threshold = TIME_TO_COLLISION_THRESHOLD * 2.0
        else:
            time_to_collision_threshold = TIME_TO_COLLISION_THRESHOLD
        
        # Consider driver reaction time
        effective_time_to_collision = time_to_collision - driver_reaction_time
        
        if effective_time_to_collision < time_to_collision_threshold:
            return 1, time_to_collision, time_to_collision_threshold
        return 0, time_to_collision, time_to_collision_threshold
    return 0, float('inf'), TIME_TO_COLLISION_THRESHOLD

# Check for each data point if emergency braking is needed and calculate TTC
emergency_brake_flags = []
ttc_values = []
ttc_thresholds = []

for i in range(len(vehicle_data)):
    brake_flag, ttc, ttc_threshold = check_emergency_brake(
        vehicle_speeds[i], 
        object_speeds[i], 
        object_positions_x[i], 
        weather_conditions[i], 
        DRIVER_REACTION_TIME
    )
    emergency_brake_flags.append(brake_flag)
    ttc_values.append(ttc)
    ttc_thresholds.append(ttc_threshold)

# Create subplots
fig, axs = plt.subplots(3, 1, figsize=(10, 15), sharex=True)

# Plot TTC and TTC threshold
axs[0].plot(timestamps, ttc_values, marker='o', linestyle='-', color='c', label='TTC')
axs[0].plot(timestamps, ttc_thresholds, linestyle='--', color='r', label='TTC Threshold')
axs[0].set_ylabel('Time to Collision (TTC)')
axs[0].set_title('Time to Collision (TTC) Over Time')
axs[0].legend()

# Plot weather condition
axs[1].plot(timestamps, weather_conditions, marker='o', linestyle='-', color='k')
axs[1].set_ylabel('Weather Condition')
axs[1].set_title('Weather Condition Over Time')

# Plot emergency braking signal
axs[2].plot(timestamps, emergency_brake_flags, marker='o', linestyle='-', color='r')
axs[2].set_xlabel('Timestamp')
axs[2].set_ylabel('Brake Signal (1 = ON, 0 = OFF)')
axs[2].set_title('Emergency Braking Signal Over Time')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
"""
Weather-Aware Autonomous Emergency Braking (AEB) System Simulator

This script simulates an AEB system that considers weather conditions when
calculating Time to Collision (TTC). It processes input data from a JSON file,
adjusts braking thresholds based on weather, determines when emergency braking
should be applied, and generates visualizations of the results.

Features:
- Calculates TTC considering weather conditions (dry/wet)
- Adjusts braking thresholds based on weather
- Generates plots for TTC, weather conditions, and emergency braking signals
- Outputs an updated JSON file with braking state information

Author: Hamza EL HANBALI

Usage: python aeb_weather.py
"""

import json
import matplotlib.pyplot as plt

# Define constants
TIME_TO_COLLISION_THRESHOLD = 2.0
INPUT_FILE = 'recorded_data.json'
OUTPUT_FILE = 'recorded_data_with_simple_braking.json'

def check_emergency_brake(vehicle_speed, object_speed, object_position_x, weather):
    relative_speed = vehicle_speed - object_speed
    if relative_speed <= 0:
        return 0, float('inf'), TIME_TO_COLLISION_THRESHOLD
    
    time_to_collision = object_position_x / relative_speed
    
    # Adjust time to collision threshold based on weather
    if weather == 'wet':
        time_to_collision_threshold = TIME_TO_COLLISION_THRESHOLD * 1.5
    else:
        time_to_collision_threshold = TIME_TO_COLLISION_THRESHOLD
    
    return int(time_to_collision < time_to_collision_threshold), time_to_collision, time_to_collision_threshold

# Read the recorded data
with open(INPUT_FILE, 'r') as file:
    data = json.load(file)

vehicle_data = data['vehicle_data']
timestamps = []
vehicle_speeds = []
object_speeds = []
object_positions_x = []
weather_conditions = []
emergency_brake_flags = []
ttc_values = []
ttc_thresholds = []

for entry in vehicle_data:
    timestamps.append(entry['timestamp'])
    vehicle_speeds.append(entry['vehicle_speed'])
    object_speeds.append(entry['object_speed'])
    object_positions_x.append(entry['object_position']['x'])
    weather_conditions.append(entry['weather_condition'])
    
    brake_flag, ttc, ttc_threshold = check_emergency_brake(
        entry['vehicle_speed'],
        entry['object_speed'],
        entry['object_position']['x'],
        entry['weather_condition']
    )
    
    emergency_brake_flags.append(brake_flag)
    ttc_values.append(ttc)
    ttc_thresholds.append(ttc_threshold)
    
    # Add braking state to the entry
    entry['braking_state'] = bool(brake_flag)

# Create subplots
fig, axs = plt.subplots(3, 1, figsize=(10, 15), sharex=True)

# Plot TTC and TTC threshold
axs[0].plot(timestamps, ttc_values, marker='o', linestyle='-', color='c', label='TTC')
axs[0].plot(timestamps, ttc_thresholds, linestyle='--', color='r', label='TTC Threshold')
axs[0].set_ylabel('Time to Collision (TTC)')
axs[0].set_title('Simple Time to Collision (TTC) Over Time')
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

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Write the updated data to a new JSON file
with open(OUTPUT_FILE, 'w') as file:
    json.dump(data, file, indent=2)

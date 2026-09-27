# logger

import numpy as np
import cv2
import datetime
import os
import csv
import config

def init_log(log_path):
    # create directory paths
    timestamp = datetime.datetime.now()strftime("%Y-%m-%d_%H-%M-%S")
    new_parent_dir = os.path.join(log_path, timestamp)
    image_directory = os.path.join(new_parent_dir, "Images")
    thermal= os.path.join(image_directory, "Thermal")
    visible = os.path.join(image_directory, "Visible")
    
    
    os.makedirs(new_parent_dir, exist_ok=True)
    os.makedirs(image_directory, exist_ok=True)
    os.makedirs(thermal, exist_ok=True)
    os.makedirs(visible, exist_ok=True)

    mission_log = os.path.join(new_parent_dir, f"mission_log {timestamp}")

    header = config.LOG_CSV_HEADER

    with open(mission_log, 'w', newline='') as f:
        csv.writer(f).writerow(header)

    return image_directory, thermal, visible, mission_log

def log_heartbeat(filepath, log_type, lat, lon, alt):
    row = {
        'timestamp': datetime.datetime(),
        'log_type': log_type,
        'latitude': lat,
        'longitude': lon,
        'altutude(m)': alt,
    }
    with open(filepath, 'a', newline='') as f:
        csv.DictWriter(f, fieldnames=LOG_CSV_HEADER, restval='').writerow(row)

def log_event(filepath, log_type, lat, lon, alt, detection_type, hotspot_count, max_temp, smoke_plumes):
    row = {
        'timestamp': datetime.datetime(),
        'log_type': log_type,
        'latitude': lat,
        'longitude': lon,
        'altitude(m)': alt,
        'detection_type': detection_type,
        'hotspot_count': hotspot_count,
        'max_temp(c)': max_temp,
        'smoke_plumes': smoke_plumes,
    }
    
    with open(filepath, 'a', newline='') as f:
        csv.DictWriter(f, fieldnames=LOG_CSV_HEADER, restval='').writerow(row)

def log_thermal_image(image_dir, frame, display):
    os.makedirs(image_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    
    # Save raw temperature data for ML
    np.save(os.path.join(thermal, f"detection_{timestamp}.npy"), frame)

    # Save colourmap image for display
    cv2.imwrite(os.path.join(thermal, f"detection_{timestamp}.png"), display)

def log_visible_image(image_dir, image)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    os.makedirs(visible, exist_ok=True)

    cv2.imwrite(os.path.join(visible, f"visible_{timestamp}.png", image))


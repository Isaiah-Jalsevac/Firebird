# logger

import numpy as np
import cv2
import datetime
import os
import csv

def init_log(log_path):
    # create directory paths
    timestamp = datetime.datetime.now()strftime("%Y-%m-%d_%H-%M-%S")
    new_parent_dir = os.path.join(log_path, timestamp)
    image_directory = os.path.join(new_parent_dir, "Images")
    thermal_raw = os.path.join(image_directory, "Raw Thermal")
    thermal_image = os.path.join(image_directory, "RGB Thermal")
    visible_contours = os.path.join(image_directory, "Visible Contours")
    visible_image = os.path.join(image_directory, "RGB Visible")
    
    
    os.makedirs(new_parent_dir, exist_ok=True)
    os.makedirs(image_directory, exist_ok=True)
    os.makedirs(thermal_raw, exist_ok=True)
    os.makedirs(thermal_image, exist_ok=True)
    os.makedirs(visible_contours, exist_ok=True)
    os.makedirs(visible_image, exist_ok=True)

    mission_log = os.path.join(new_parent_dir, f"mission_log {timestamp}")

    header = config.LOG_CSV_HEADER

    with open(mission_log, 'w', newline='') as f:
        csv.writer(f).writerow(header)

    return image_directory, thermal_raw, thermal_image, visible_contours, visible_image, mission_log

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
    np.save(os.path.join(image_dir, f"detection_{timestamp}.npy"), frame)

    # Save colourmap image for display
    cv2.imwrite(os.path.join(image_dir, f"detection_{timestamp}.png"), display)



                                                                           

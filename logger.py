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

    header = 

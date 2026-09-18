# thermal_loop

import config
import cv2
import numpy as np
import time

# Takes THERMAL_DEVICE, grabs frame, and outputs visual frame and a temp map in celsius
class ThermalCamera:
    def __init__(self):
        self.cap = cv2.VideoCapture(config.THERMAL_DEVICE)
        self.cap.set(cv2.CAP_PROP_CONVERT_RGB, 0) # Raw data, not processed RGB

        if not self.cap.isOpened():
            raise RuntimeError(f"Could not open thermal camera on device {config.THERMAL_DEVICE}")
                               
        print(f"Thermal camera opened on /dev/video{config.THERMAL_DEVICE}")

    def get_frame(self):
        ret, frame = self.cap.read()

        if not ret or frame is None:
            return None, None, None # Used for periodic NUC dropout. Also handels read errors.
        
        # Split frame into visual and thermal halves
        raw_thermal = frame[config.FRAME_HEIGHT:, :]

        # Decode raw 16-bit temperature data
        raw_16 = raw_thermal[:, :, 1].astype(np.uint16) * 256 + raw_thermal[:, :, 0].astype(np.uint16)
        celsius_temp_map = (raw_16 / 64.0) - 273.15 # Outputs a temperatue map with shape[FRAME_HEIGHT, FRAME_WIDTH]
                                                    # This points to the temperature in celsius


        # Build display image
        display = cv2.normalize(celsius_temp_map, None, 0, 255, cv2.NORM_MINMAX)
        display = display.astype(np.uint8)
        display = cv2.applyColorMap(display, cv2.COLORMAP_INFERNO)
        
        return frame, celsius_temp_map, display

    # Cleanly relase camera
    def release(self):
        self.cap.release()
 
# Takes celsius temperature map and returns contours of pixels over threshold
def detect_hotspot_const(temp_map):
    # creates bool map of temperatures over threshold
    bool_map = temp_map > config.DETECTION_THRESHOLD_CONST
    binary_mask = bool_map.astype(np.uint8) * 255 # Convert to a binary array so it can be read by cv2
    # Find contours over MIN_HOTSPOT_AREA
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    valid_contours = [c for c in contours if cv2.contourArea(c) > config.MIN_HOTSPOT_AREA]

    return valid_contours

def detect_hotspot_mean(temp_map):
    mean_temp = np.mean(temp_map)
    bool_map = temp_map > (mean_temp + config.DETECTION_THRESHOLD_OVER_MEAN)
    binary_mask = bool_map.astype(np.uint8) * 255 # Convert to a binary array so it can be read by cv2
    # Find contours over MIN_HOTSPOT_AREA
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    valid_contours = [c for c in contours if cv2.contourArea(c) > config.MIN_HOTSPOT_AREA]

    return valid_contours

heartbeat = time.time()
def run():
    heartbeat.value = time.time()
    # setup camera connection
    try:
        camera = ThermalCamera()
    except RuntimeError as e:
        print(f"failed to initialize camera: {e}")
        exit(1)

    running = True
    while running == True:
        frame, contour_map, display = camera.get_frame()

        contours_const = []
        contours_mean = []

        if config.DETECTION_TYPE == 0: # Checks which detection method is being used
            contours_mean = detect_hotspot_mean(temp_map)
        if config.DETECTION_TYPE == 1:
            contours_const = detect_hotspot_const(temp_map)
        if config.DETECTION_TYPE == 2:
            contours_mean = detect_hotspot_mean(temp_map)
            contours_const = detect_hotspot_const(temp_map)

       if contours_mean:# if detection occured, log it
            max_temp = temp_map.max()
            total_area_mean = sum(cv2.contourArea(c) for c in contours_mean)
            #TODO: send detection log request

            if current_time - last_frame_save_mean > config.IMAGE_SAVE_COOLDOWN:
                #TODO: send image log request 
                last_frame_save_mean = time.time()

        if contours_const:# if detection occured, log it
            max_temp = temp_map.max()
            total_area_const = sum(cv2.contourArea(c) for c in contours_const)
            #TODO: send detection log request

            if current_time - last_frame_save_const > config.IMAGE_SAVE_COOLDOWN:
                #TODO: send image log request
                last_frame_save_const = time.time()


        #Send allert to GCS
        if contours_const or contours_mean:
            if current_time - last_gcs_alert > config.GCS_ALERT_FREQUENCY:
                if config.DETECTION_TYPE == 0:
                    #TODO: send GCS detection allert
                    last_gcs_alert = current_time
                if config.DETECTION_TYPE [1, 2]:    
                    #TODO: send GCS detection allert
                    last_gcs_alert = current_time
 
    #TODO: if main.py sends shutdown request, clean up and shutoff


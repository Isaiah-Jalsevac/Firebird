# config.py

# main
PROCESSES = {
    "thermal": thermal_detection.run,
    "visible": stubb_visible_loop,
    "mavlink": stubb_mavlink_loop,
}

TERMINATE_GRACE_PERIOD = 1.0
HEARTBEAT_CHECK_FREQUENCY = 1 # time in hz inbetween heartbeat checks

# thermal_camera
FRAME_WIDTH = 256
FRAME_HEIGHT = 192
THERMAL_DEVICE = 4

# visible_camera
FRAME_WIDTH = # TODO:
FRAME_HIGHT = # TODO:
VISIBLE_DEVICE = # TODO:

# thermal_detection
DETECTION_TYPE = 1 # 0 is mean, 1 is constant, 2 is both
DETECTION_THRESHOLD_CONST = 35
MIN_HOTSPOT_AREA = 5
DETECTION_THRESHOLD_OVER_MEAN = 10 

# logging
LOG_PATH = 'data/logs' # file path for detection logs
IMAGE_SAVE_COOLDOWN = 1.0 # cooldown between saving images

# mavlink
MAVLINK_PORT = '/dev/ttyS0'
MAVLINK_BAUD = 57600
MAVLINK_SYSTEM_ID = 1
MAVLINK_COMPONENT_ID = 191
MAVLINK_GPS_RATE_HZ = 2


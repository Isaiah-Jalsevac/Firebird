import numpy as np
import time
import signal
from multiprocessing import Process, Value

def stubb_thermal_loop(heartbeat: Value):
    while True:
        hearbeat.value = time.time()
        time.sleep(0.2)

        
def stubb_visible_loop(heartbeat: Value):
    while True:
        hearbeat.value = time.time()
        time.sleep(0.2)


def stubb_mavlink_loop(heartbeat: Valui):
    while True:
        hearbeat.value = time.time()
        time.sleep(0.2)


def stubb_logging_loop(heartbeat: Value):
    while True:
        hearbeat.value = time.time()
        time.sleep(0.2)



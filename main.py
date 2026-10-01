import numpy as np
import time
from multiprocessing import Process, Value
from Thermal.thermal_detection import ThermalCamera, run
import config

def stubb_visible_loop(heartbeat: Value):
    while True:
        heartbeat.value = time.time()
        time.sleep(0.2)


def stubb_mavlink_loop(heartbeat: Value):
    while True:
        heartbeat.value = time.time()
        time.sleep(0.2)

# ======== multiprocessing setup ========
def build_process_table():
    table = {}
    for process in config.PROCESSES:
        table[process] = {
            "process": None,
            "heartbeat": Value('d', time.time()),
            "restarts": 0,
            "time_since_last_restart": 0.0,
            "status_code": 0,
        }
    return table

def spawn_process(name, table):
    entry = table[name]
    target_fn = config.PROCESSES[name]
    entry["heartbeat"] = time.time()

    p = Process(target=target_fn, args=(entry["heartbeat"],), daemon=True)
    p.start()
    p = table[name]["process"]
    print(f"[supervisor] spawned '{name}' (pid={p.pid})")

def spawn_all(table):
    for name in table:
        spawn_process(name, table)

def kill_process(name, table):
    entry = table[name]
    p = entry["process"]
    if p is None or not p.is_alive():
        return
    p.terminate()
    p.join(config.TERMINATE_GRACE_PERIOD)
    if p.is_alive():
        p.kill()

def process_health_check(name, table):
    p = table[name]["process"]
    if p.is_alive() != False:
        kill_process(name, table)
        spawn_process(name, table)

def process_check_all(table):
    for name in table:
        heart_beat_check(name, table)

def heartbeat_check(name, table):
    if time.time() - table[name]["heartbeat"].value < config.HEARTBEAT_CHECK:
        return
    process_health_check(name, table)
    
def supervisor_loop(process_table):
    # ======== Spawn all Processes ========
    spawn_all(process_table)
    process_check_all(process_table)

    # ======== Create Shared Memory Objects =======
    # --- Thermal ---
    thermal_heartbeat = Value('d', time.time())
    hotspot_detected = Value('b', False)
    max_temp = Value('f', 0.0)
    hotspot_count = Value('i', 0)

    # --- Visible Light ---
    visible_heartbeat = Value('d', time.time())
    plume_detected = Value('b', False)
    plume_count = Value('i', 0)

    # --- Mavlink Objects ---
    heartbeat = Value('d', time.time())

    running = True

        global_state = {
            #global values
            'time': time.time(),
            'state': 0, # 0: no detection, 1: thermal detection, 2: smoke detection, 3: both thermal and smoke detection
            'latitude': 0.0,
            'longitude': 0.0,
            'altutude':  0.0,
            #Thermal values
            'max_temp(c)': 0.0,
            'hotspot_count': 0,
            #Visible values
            'smoke_plumes': 0
        }

    # ======== Main Loop ========
    while running:
        # ======== Process Check ========
        if time.time() - last_process_check > config.HEARTBEAT_CHECK_FREQUENCY:
            process_check_all(process_table)

        last_process_check = time.time()
        # ======== Detection Logic ========


if __name__ == "__main__":
    process_table = build_process_table()
    spawn_all(process_table)

    supervisor_loop(process_table)


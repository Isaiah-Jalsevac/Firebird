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
def spawn_process(process, process_table):
    target_fn, data = process_table[process]
    data["heartbeat"] = time.time()
    p = Process(target=target_fn, args=(data["heartbeat"],), daemon=True)
    p.start()
    p = data["process"]
    print(f"[supervisor] spawned '{name}' (pid={p.pid})")

def spawn_all(process_table):
    for process in process_table:
        spawn_process(process, process_table)

def kill_process(process, process_table):
    entry = process_table[process]
    p = entry["process"]
    if p is None or not p.is_alive():
        return
    p.terminate()
    p.join(config.TERMINATE_GRACE_PERIOD)
    if p.is_alive():
        p.kill()

def process_health_check(process, process_table):
    p = process_table[process]["process"]
    if p.is_alive() != False:
        kill_process(process, process_table)
        spawn_process(process, process_table)

def process_check_all(process_table):
    for process in process_table:
        heart_beat_check(process, process_table)

def heartbeat_check(process, process_table):
    if time.time() - process_table[process]["heartbeat"].value < config.HEARTBEAT_CHECK:
        return
    process_health_check(process, process_table)
    
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

    # ======== Main Loop ========
    while running:
        # ======== Process Check ========
        if time.time() - last_process_check > config.HEARTBEAT_CHECK_FREQUENCY:
            process_check_all(process_table)

        last_process_check = time.time()
        # ======== Detection Logic ========


if __name__ == "__main__":
    state = config.PROCESSES
    spawn_all(state)

    supervisor_loop(state)


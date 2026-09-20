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
    
# ======== Main Loop ========
# main loop, this coordinates all the other loops for logging detections, sending 
# allerts etc. also used to check on processes and restart in necessary
def supervisor_loop(process_table):
    running = True
    while running:
        # spawn all processes
        # check on all processes every 1hz 
        # (just set up an if time passed > x run heartbeat checks)
        # run detection coordination logic

        spawn_all(process_table)

        last_process_check = time.time()
        
        process_check_all(process_table)




if __name__ == "__main__":
    process_table = build_process_table()
    spawn_all(process_table)

    supervisor_loop(process_table)


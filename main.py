import numpy as np
import time
import signal
from multiprocessing import Process, Value
from Thermal.thermal_detection import ThermalCamera, run

def stubb_visible_loop(heartbeat: Value):
    while True:
        heartbeat.value = time.time()
        time.sleep(0.2)


def stubb_mavlink_loop(heartbeat: Value):
    while True:
        heartbeat.value = time.time()
        time.sleep(0.2)


def stubb_logging_loop(heartbeat: Value):
    while True:
        heartbeat.value = time.time()
        time.sleep(0.2)


def build_process_table():
    table = {}
    for process in config.PROCESSES:
        table[process] = {
            "process": None,
            "heartbeat": Value('d', time.time()),
            "restarts": 0,
            "time_since_last_restart": 0.0,
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
    p.join(config.TIMOUT_GRACE_PERIOD)

    if p.is_alive():
        p.kill()
        p.join()

def child_health_check(name, table):



def heartbeat_check(name, table):
    if time.time() - table[name]["heartbeat"] < config.HEARTBEAT_CHECK:
        return
        child_health_check(name)
    





if __name__ == "__main__":
    process_table = process_table()
    spawn_all(process_table)


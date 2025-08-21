import re
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

RAW_DIR = "AsamAminoClean/"
OUT_DIR = "processed/"
os.makedirs(OUT_DIR, exist_ok=True)

def process_file(filepath):
    """Bersihkan dan potong file insulin"""
    with open(filepath) as f:
        raw_data = f.read()

    # Bersihkan data
    cleaned = raw_data.replace("ORIGIN", "").replace("//", "")
    cleaned = re.sub(r'[^a-zA-Z]', '', cleaned).lower()

    filename = os.path.splitext(os.path.basename(filepath))[0]

    # Simpan full sequence
    clean_file = os.path.join(OUT_DIR, f"{filename}-seq-clean.txt")
    with open(clean_file, "w") as f:
        f.write(cleaned)

    print(f"[OK] {filename}: Full sequence length = {len(cleaned)}")

    # Potong bagian
    lsinsulin = cleaned[0:24]
    binsulin = cleaned[24:54]
    cinsulin = cleaned[54:89]
    ainsulin = cleaned[89:110]

    # Simpan bagian
    with open(os.path.join(OUT_DIR, f"ls{filename}-seq-clean.txt"), "w") as f: f.write(lsinsulin)
    with open(os.path.join(OUT_DIR, f"b{filename}-seq-clean.txt"), "w") as f: f.write(binsulin)
    with open(os.path.join(OUT_DIR, f"c{filename}-seq-clean.txt"), "w") as f: f.write(cinsulin)
    with open(os.path.join(OUT_DIR, f"a{filename}-seq-clean.txt"), "w") as f: f.write(ainsulin)

    print(f"    Signal: {len(lsinsulin)}, B-chain: {len(binsulin)}, "
          f"C-peptide: {len(cinsulin)}, A-chain: {len(ainsulin)}")

class Watcher(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".txt"):
            print(f"[NEW FILE DETECTED] {event.src_path}")
            process_file(event.src_path)

class InsulinHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".csv"):
            print(f"File baru terdeteksi: {event.src_path}")
            os.system(f"python3 insulin_cleaning.py {event.src_path}")

if __name__ == "__main__":
    path_to_watch = "/home/ec2-user/environment/insulin_data"  
    event_handler = InsulinHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=False)
    observer.start()
    print(f"Watcher aktif memantau {path_to_watch} ...")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

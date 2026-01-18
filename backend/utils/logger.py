import datetime

def _log(level, msg):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{level}] {ts} | {msg}")

def info(msg): _log("INFO", msg)
def progress(msg): _log("PROGRESS", msg)
def success(msg): _log("SUCCESS", msg)
def error(msg): _log("ERROR", msg)

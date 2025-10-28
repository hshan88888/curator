import csv
from datetime import datetime
from collections import defaultdict

def parse_time(t):
    # Remove any extra characters that may exist at the beginning and end of the time string.
    t = t.strip()
    # If the time string contains a decimal point, handle the microsecond part.
    if '.' in t:
        parts = t.split('.')
        t = parts[0] + '.' + parts[1][:6]
    try:
        return datetime.strptime(t, "%H:%M:%S.%f")
    except ValueError:
        print(f"Unable to parse the time format: {t}")
        return None

def parse_procmon_csv(csv_file):
    func_times = defaultdict(list)
    entry_times = {}

    with open(csv_file, newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 7:
                continue

            time_str, process, pid, event, col4, col5, message = row
            time = parse_time(time_str)
            if not time:
                continue

            message = message.strip()

            if message.startswith("Output: ==>"):
                func_name = message.replace("Output: ==>","").strip()
                entry_times[func_name] = time

            elif message.startswith("Output: <=="):
                func_name = message.replace("Output: <==","").strip()
                if func_name in entry_times:
                    duration = (time - entry_times[func_name]).total_seconds()
                    func_times[func_name].append(duration)

    print("\n=== Function Execution Times (seconds) ===")
    for func, times in func_times.items():
        total_time = sum(times)
        print(f"{func}: total {total_time:.6f}s over {len(times)} call(s) (avg {total_time/len(times):.6f}s)")

parse_procmon_csv("EvenimenteProcMonTest2.CSV")


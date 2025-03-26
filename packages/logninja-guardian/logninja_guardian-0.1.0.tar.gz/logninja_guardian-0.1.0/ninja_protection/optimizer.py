import psutil
import os
import time
import redis
import argparse
import threading
from termcolor import colored
import hashlib

# Set up Redis connection (Ensure Redis is running)
r = redis.Redis(host='redis', port=6379, db=0)

# Directory for storing logs
LOGS_DIR = os.path.join(os.path.dirname(__file__), 'logs')

# Ensure the logs directory exists, create it if it doesn't
os.makedirs(LOGS_DIR, exist_ok=True)

# Now, you can use LOGS_DIR to store your logs
log_file_path = os.path.join(LOGS_DIR, 'logfile.log')

# Example of logging to the file
with open(log_file_path, 'a') as log_file:
    log_file.write("This is a log entry.\n")

print(f"Logs are being saved in {log_file_path}")


# Define DefCon levels
DEFCON_LEVELS = {
    1: 'Critical',  # Most severe
    2: 'High',      # High priority
    3: 'Medium',    # Normal operations
    4: 'Low',       # Low priority
    5: 'Normal'     # Non-priority
}

# Function to hash a log message
def hash_log_message(message):
    return hashlib.sha256(message.encode('utf-8')).hexdigest()

# Ninja log filter function with time stamps and colored logs based on DefCon level
def ninja_log(message, emoji='💻', priority=False, defcon_level=3):
    if not message:
        message = "No action needed."
        
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    ninja_message = f"[{timestamp}] [NINJA PROTECTION] {emoji} - {message}"

    # Hash the message before sending to Redis
    hashed_message = hash_log_message(ninja_message)
    
    # Define colors based on DefCon level
    defcon_colors = {
        1: 'red',
        2: 'yellow',
        3: 'green',
        4: 'blue',
        5: 'white'
    }
    
    # Get the color for the current DefCon level
    color = defcon_colors.get(defcon_level, 'white')
    
    # Color the message
    colored_message = colored(ninja_message, color)
    
    # Log the original message to a log file
    log_file_path = os.path.join(LOGS_DIR, 'logfile.log')
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"{ninja_message}\n")
    
    # Send the hashed message to Redis (only store the hash)
    if priority:
        r.lpush('loggie_ninja_defcon', hashed_message)
    else:
        r.lpush('$LOGGIE_ChainSeal-LogNinja_Optimization', hashed_message)
    
    # Print the colored message to console
    print(colored_message)
    print(colored(f"[$LOGGIE] ChainSeal: {hashed_message}", 'grey'))

# Function to optimize CPU usage
def optimize_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    defcon_level = 3  # Default to medium priority

    # Log the current CPU usage
    ninja_log(f"[CPU] Current CPU Usage: {cpu_usage}%", emoji='🔥', defcon_level=defcon_level)

    if cpu_usage > 85:
        defcon_level = 1  # Critical
        ninja_log("[CPU] High CPU usage detected. The ninja swiftly limits non-essential processes... 🥷", emoji='⚡', priority=True, defcon_level=defcon_level)
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            if proc.info['cpu_percent'] > 10:
                ninja_log(f"[CPU] Lowering priority of {proc.info['name']} (PID {proc.info['pid']}) ⚙️", emoji='⚔️', priority=True, defcon_level=defcon_level)
                p = psutil.Process(proc.info['pid'])
                p.nice(19)  
    else:
        defcon_level = 5  
        ninja_log("[CPU] CPU usage is within optimal range. The ninja stands watch silently... 🥷", emoji='🛡️', defcon_level=defcon_level)

# Function to optimize memory usage
def optimize_memory_usage():
    memory = psutil.virtual_memory()
    ninja_log(f"[MEMORY] Total Memory: {memory.total / (1024 ** 3):.2f} GB | Used Memory: {memory.used / (1024 ** 3):.2f} GB", emoji='🧠')
    ninja_log(f"[MEMORY] Free Memory: {memory.available / (1024 ** 3):.2f} GB | Memory Usage: {memory.percent}%", emoji='💡')

    if memory.percent > 80:
        ninja_log("[MEMORY] High memory usage detected. The ninja clears the cache to free up memory... 🧹", emoji='🔧', priority=True, defcon_level=1)
        try:
            # Attempt to clear the cache
            os.system('sync; echo 3 > /proc/sys/vm/drop_caches')
        except PermissionError:
            ninja_log("[MEMORY] Permission denied while clearing cache. Please run with sudo to clear caches.", emoji='⚠️', defcon_level=1)
    else:
        ninja_log("[MEMORY] Memory usage is within optimal range. The ninja rests... 🥷", emoji='💤', defcon_level=5)

# Function to optimize disk usage
def optimize_disk_usage():
    ninja_log("[MEMORY] \nDisk Info: 🗂️", emoji='📀')
    partitions = psutil.disk_partitions()
    for partition in partitions:
        if "loop" in partition.device:
            ninja_log(f"[MEMORY] Skipping cleanup for loop device: {partition.device} 🚫", emoji='❌')
            continue
        usage = psutil.disk_usage(partition.mountpoint)
        ninja_log(f"[MEMORY] Device: {partition.device} | Total: {usage.total / (1024 ** 3):.2f} GB | Used: {usage.used / (1024 ** 3):.2f} GB", emoji='💾')
        ninja_log(f"[MEMORY] Free: {usage.free / (1024 ** 3):.2f} GB | Usage: {usage.percent}%", emoji='📊')

        if usage.percent > 80:
            ninja_log(f"[MEMORY] High disk usage detected on {partition.device}. The ninja begins a cleanup... 🧹", emoji='🛠️', priority=True, defcon_level=2)
            os.system("sudo apt-get clean")
        else:
            ninja_log(f"[MEMORY] Disk usage on {partition.device} is within optimal range. The ninja stands guard... 🥷", emoji='🔒', defcon_level=5)

# Function to optimize network usage
def optimize_network_usage():
    ninja_log("[NETWORK] \nNetwork Info: 🌐", emoji='📡')
    net_io = psutil.net_io_counters()
    ninja_log(f"[NETWORK] Bytes Sent: {net_io.bytes_sent / (1024 ** 2):.2f} MB | Bytes Received: {net_io.bytes_recv / (1024 ** 2):.2f} MB", emoji='💬')
    ninja_log(f"[NETWORK] Packets Sent: {net_io.packets_sent} | Packets Received: {net_io.packets_recv}", emoji='📦')

    interfaces = psutil.net_if_addrs()
    selected_interface = None
    for iface, addrs in interfaces.items():
        if iface.startswith("lo") or "docker" in iface or "br-" in iface:
            continue
        for addr in addrs:
            if addr.family.name == 'AF_INET':  
                selected_interface = iface
                break
        if selected_interface:
            break

    if net_io.bytes_sent / (1024 ** 2) > 500 or net_io.bytes_recv / (1024 ** 2) > 500:
        ninja_log("[NETWORK] High network usage detected. The ninja considers throttling non-essential connections... ⚡", emoji='🌀', priority=True, defcon_level=1)
        if selected_interface:
            try:
                ninja_log(f"[NETWORK] Primary interface detected: {selected_interface}. Initiating soft throttle protocol... 🚦", emoji='🔧', defcon_level=3)
                os.system(f"[NETWORK] sudo tc qdisc add dev {selected_interface} root tbf rate 1mbit burst 32kbit latency 400ms")
            except Exception as e:
                ninja_log(f"[NETWORK] Error applying throttle: {str(e)}", emoji='⚠️', priority=True, defcon_level=1)
        else:
            ninja_log("[NETWORK] No valid network interface found. The ninja abandons the task... 🚫", emoji='⚠️', priority=True, defcon_level=2)
    else:
        ninja_log("[NETWORK] Network usage is within optimal range. The ninja watches over the network silently... 🥷", emoji='🔍', defcon_level=5)

# Main function to run all optimizations
def run_optimization():
    ninja_log("[NETWORK] Starting system optimization... 🥷", emoji='⚔️', defcon_level=3)
    optimize_cpu_usage()
    optimize_memory_usage()
    optimize_disk_usage()
    optimize_network_usage()
    ninja_log("[NETWORK] \nOptimization completed. The ninja remains vigilant... 🥷", emoji='🛡️', defcon_level=5)

# Function to run optimizations with threading
def run_optimization_with_threads():
    threads = []

    # Create threads for each optimization function with detailed logging
    print("Starting CPU optimization...")
    cpu_thread = threading.Thread(target=optimize_cpu_usage)
    threads.append(cpu_thread)

    print("Starting memory optimization...")
    memory_thread = threading.Thread(target=optimize_memory_usage)
    threads.append(memory_thread)

    print("Starting disk optimization...")
    disk_thread = threading.Thread(target=optimize_disk_usage)
    threads.append(disk_thread)

    print("Starting network optimization...")
    network_thread = threading.Thread(target=optimize_network_usage)
    threads.append(network_thread)

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Log completion of each optimization
    print("CPU optimization completed.")
    print("Memory optimization completed.")
    print("Disk optimization completed.")
    print("Network optimization completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Optimize system resources based on usage thresholds.")
    parser.add_argument("--interval", type=int, default=10, help="Interval in seconds to run optimization")
    parser.add_argument("--defcon", type=int, choices=[1, 2, 3, 4, 5], default=3, help="Set default DefCon level")
    args = parser.parse_args()

    print("\n💻 Ninja Protection System 🥷")
    print(f"⚙️  Optimizing system resources with interval: {args.interval} seconds.")
    print(f"⛔  Default DefCon Level set to: {DEFCON_LEVELS[args.defcon]}")

    # Introducing a 5-second delay before starting optimization
    print("\n⏳ Waiting for 5 seconds before starting optimization...")
    time.sleep(5)  # Set to 5 seconds before the first cycle

    # Run optimization on a defined interval
    while True:
        run_optimization_with_threads()  # Run the optimization cycle
        time.sleep(args.interval)  # Wait for the specified interval before running again

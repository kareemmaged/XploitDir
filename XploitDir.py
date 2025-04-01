import requests
import sys
import threading
import queue
import os
import time
import argparse
from urllib.parse import urljoin

# Tool banner with enhanced visuals
BANNER = """
\033[95m

██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗██████╗ ██╗██████╗ 
╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝██╔══██╗██║██╔══██╗
 ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   ██║  ██║██║██████╔╝
 ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   ██║  ██║██║██╔══██╗
██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   ██████╔╝██║██║  ██║
╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   ╚═════╝ ╚═╝╚═╝  ╚═╝

\033[0m
\033[1;93mXploitDir - Directory Enumeration Tool by [megoz]\033[0m
"""

# ANSI escape codes for colors
GREEN = "\033[92m"
RESET = "\033[0m"

# Function to create a boxed message
def create_boxed_message(message, color=GREEN):
    lines = message.split('\n')
    max_length = max(len(line) for line in lines)
    box_top = f"{color}╔═{'═' * max_length}═╗{RESET}"
    box_bottom = f"{color}╚═{'═' * max_length}═╝{RESET}"
    boxed_lines = [f"{color}║ {line.ljust(max_length)} ║{RESET}" for line in lines]
    return '\n'.join([box_top] + boxed_lines + [box_bottom])

# Function to check if a directory exists
def check_directory(url, directory, stop_event, counter, lock, total_dirs, log_file, timeout, user_agent):
    if stop_event.is_set():
        return
    target_url = urljoin(url, directory)
    headers = {"User-Agent": user_agent}
    try:
        start_time = time.time()
        response = requests.get(target_url, timeout=timeout, headers=headers)
        elapsed_time = time.time() - start_time
        with lock:  # Thread-safe counter update
            counter[0] += 1
            print(f"\r[*] Tried {counter[0]}/{total_dirs} directories", end='', flush=True)
        if response.status_code == 200:
            boxed_message = create_boxed_message(f"[+] Found directory: {target_url}")
            print(f"\n{boxed_message}")
            with open(log_file, 'a') as f:
                f.write(f"[{time.ctime()}] {target_url} - Status: 200 - Time: {elapsed_time:.2f}s\n")
    except requests.RequestException:
        pass

# Main function to run the directory enumeration
def enumerate_directories(base_url, wordlist_file, num_threads, timeout, user_agent, log_file):
    if not base_url.endswith('/'):
        base_url += '/'

    try:
        with open(wordlist_file, 'r') as file:
            directories = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"[!] Error: Wordlist file '{wordlist_file}' not found.")
        sys.exit(1)

    total_dirs = len(directories)
    print(f"[*] Loaded {total_dirs} directories from {wordlist_file}")
    print(f"[*] Starting enumeration on {base_url} with {num_threads} threads...")

    q = queue.Queue()
    stop_event = threading.Event()
    counter = [0]  # Mutable list for thread-safe counter
    lock = threading.Lock()
    for directory in directories:
        q.put(directory)

    def worker():
        while not stop_event.is_set():
            try:
                directory = q.get_nowait()
                check_directory(base_url, directory, stop_event, counter, lock, total_dirs, log_file, timeout, user_agent)
            except queue.Empty:
                break
            finally:
                q.task_done()

    threads = []
    for _ in range(min(num_threads, len(directories))):
        t = threading.Thread(target=worker)
        t.daemon = True  # Daemon threads exit with main program
        t.start()
        threads.append(t)

    try:
        while any(t.is_alive() for t in threads):
            time.sleep(0.1)  # Check threads periodically
        print(f"\n[*] XploitDir enumeration completed. Results saved to {log_file}")
    except KeyboardInterrupt:
        print("\n[!] Ctrl+C detected. Terminating XploitDir...")
        stop_event.set()  # Signal threads to stop
        for t in threads:
            t.join(timeout=1.0)  # Give threads 1 second to finish
        sys.exit(0)

# Main entry point with argument parsing
if __name__ == "__main__":
    print(BANNER)

    usage_instructions = """
\033[1;94mUsage:\033[0m
  python xploitdir.py <target_url> <wordlist_file> [options]

\033[1;94mOptions:\033[0m
  -t, --threads <num>     Number of threads (default: 10)
  -o, --output <file>     Output log file (default: xploitdir_results.txt)
  --timeout <seconds>     Request timeout in seconds (default: 5.0)
  --user-agent <string>   Custom User-Agent (default: XploitDir/1.0)
  -h, --help              Show this help message and exit

\033[1;94mExamples:\033[0m
  python xploitdir.py http://example.com wordlist.txt
  python xploitdir.py http://example.com wordlist.txt -t 20 -o results.txt --timeout 10 --user-agent "MyScanner/2.0"

Note: Only use this tool on systems you have permission to test.
"""
    print(usage_instructions)

    parser = argparse.ArgumentParser(
        description="XploitDir - Advanced Directory Enumeration Tool",
        formatter_class=argparse.RawTextHelpFormatter,  # Preserves formatting
        epilog="Note: Only use this tool on systems you have permission to test."
    )

    parser.add_argument("target_url", help="Target URL to enumerate (e.g., http://example.com)")
    parser.add_argument("wordlist_file", help="Path to the wordlist file")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads (default: 10)")
    parser.add_argument("-o", "--output", default="xploitdir_results.txt", help="Output log file (default: xploitdir_results.txt)")
    parser.add_argument("--timeout", type=float, default=5.0, help="Request timeout in seconds (default: 5.0)")
    parser.add_argument("--user-agent", default="XploitDir/1.0", help="Custom User-Agent (default: XploitDir/1.0)")

    args = parser.parse_args()

    try:
        enumerate_directories(args.target_url, args.wordlist_file, args.threads, args.timeout, args.user_agent, args.output)
    except KeyboardInterrupt:
        print("\n[!] Ctrl+C detected. Terminating XploitDir...")
        sys.exit(0)

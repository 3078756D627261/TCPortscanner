#! /usr/bin/python3

from queue import Queue
import argparse
import threading
import socket
from datetime import datetime

# Colors
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

def banner():
    print(f"""
    {CYAN}{BOLD}
╭──────────────────────────────────────────╮
│           TCP Port Scanner v1.0          │
╰──────────────────────────────────────────╯
    {RESET}""")

def port_scanner(host, port):
    try:
        # Create a new socket for this port (TCP)
        socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set timeout for the connection attempt.
        socket_obj.settimeout(1)

         # Attempt TCP connection
        socket_obj.connect((host, port))

        return True

    except socket.timeout:
        # Timeout usually means the port is filtered or the host didn't respond
        return False
    except ConnectionRefusedError:
        # Connection refused means the port is closed
        return False
    except OSError as error:
        # Other socket/network errors
        return False
    finally:
        socket_obj.close()

def worker(host, queue, open_ports, lock):
    # Takes a port from queue (port_list), scan it, and stores the port if it is open.
    while True:
        port = queue.get()
        # If there is no port, None tells the worker to stop
        if port is None:
            queue.task_done()
            break
        # Scan the port
        try:
            is_open = port_scanner(host, port)
            if is_open:
                # Protect with a lock
                with lock:
                    open_ports.append(port)
        finally:
            queue.task_done()

def main():
    # Create an argument parser
    # ArgumentDefaultsHelpFormatter ensures default values are shown in the help text
    parser = argparse.ArgumentParser(description="Simple Port scanner with thread", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Define the command-line arguments
    parser.add_argument("-t", "--target", metavar="HOST", default="192.168.1.1", help="Target machine's IP Address")
    parser.add_argument("-s", "--start", metavar="PORT", type=int, default=1, help="Beginning of port range")
    parser.add_argument("-e", "--end", metavar="PORT", type=int, default=10, help="End of port range")
    parser.add_argument("-T", "--threads", metavar="NUMBER", type=int, default=20, help="Number of worker threads")

    # Parse and use the arguments
    args = parser.parse_args()

    # Validate ports
    if not 1 <= args.start <= 65535:
        # parser.error() is specifically designed for command-line argument errors
        # argparse treats this as a command-line usage error. It prints an error message and terminates the program
        parser.error("Start port must be between 1 and 65535")

    if not 1 <= args.end <= 65535:
        parser.error("End port must be between 1 and 65535")

    if args.start > args.end:
        parser.error("Start port can't be greater than end port")

    if args.threads < 1:
        parser.error("Number of threads must be at least 1")

    # Queue containing ports to scan
    port_queue = Queue()

    # Shared list of open ports
    open_ports = []

    # When multiple threads share the same data, a Lock makes sure that only one thread at a time can access a protected section of code
    # Lock protects access to open_ports
    lock = threading.Lock()

    # Add ports to the queue
    for port in range(args.start, args.end + 1):
        port_queue.put(port)
    
    # Create worker threads
    threads = []

    for _ in range(args.threads):
        thread = threading.Thread(target=worker, args=(args.target, port_queue, open_ports, lock))
        thread.start()
        threads.append(thread)

    # Print banner
    banner()
    print(f"{YELLOW}Target       : {RESET}{args.target}")
    print(f"{YELLOW}Total ports  : {RESET}{args.end - args.start}")
    print()
    print(f"{CYAN}[•] Starting TCP port scan on {args.target} at {datetime.now().strftime("%H:%M:%S")}{RESET}")

    # Wait until every port has been processed
    port_queue.join()

    # Tell every worker to stop
    for _ in threads:
        port_queue.put(None)

    # Wait for all workers to finish
    for thread in threads:
        thread.join()

    # Sort because threads finish in arbitrary order.
    open_ports.sort()

    # Display the result
    print()
    print(f"{YELLOW}{"PORT":<8} {"STATE"}{RESET}")

    if open_ports:
        for port in open_ports:
            print(f"{str(port) + "/tcp":<8} {GREEN}OPEN{RESET}")
        print()
        print(f"{CYAN}[•] Port scan done: {GREEN}{len(open_ports)}{RESET} are open")
    else:
        print(f"{RED}[!] No open ports found{RESET}")

    
main()
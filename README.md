# 🔍 TCP Port Scanner

[![GitHub](https://img.shields.io/badge/github-repo-3776AB?style=for-the-badge&logo=github&logoColor=white)](https://github.com/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=yellow)](https://www.python.org/)
[![OS](https://img.shields.io/badge/Platform-Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black")](https://img.shields.io/)
[![LAB](https://img.shields.io/badge/Security-Lab-8A2BE2?style=for-the-badge)]("https://github.com/3078756D627261/DNSBrute/")

---

## ⚠️ Disclaimer
> [!WARNING]
> This tool is intended for **educational purposes** and **authorized network** testing. Use it only against systems you **own** or have **explicit permission** to assess. Unauthorized port scanning may `violate organizational policies`, `service agreements`, or `applicable laws`. Before scanning a system, make sure you understand the scope of your authorization and any restrictions imposed by the network owner.

---

## 📌 Overview

TCP Port Scanner is a simple, command-line network scanning tool developed in `Python`. It uses `TCP` connections and `multithreading` to check a specified range of ports on a target host.

The scanner uses `Python's built-in socket` library to attempt connections, a `thread-safe Queue` to distribute port scanning tasks, and `worker threads` to scan multiple ports concurrently.

Designed for `learning` and `authorized lab` testing, this project demonstrates fundamental concepts in Python networking, concurrency, and command-line argument handling.

---

## ✨ Features
| Feature | Description |
|:---|:---|
| ⚡ Multi-threaded scanning | Scan multiple TCP ports concurrently using worker threads |
| 🎯 Custom targets | Specify the target IP address or hostname |
| 🔢 Configurable port ranges | Choose the starting and ending ports |
| 🧵 Adjustable thread count | Control the number of worker threads |
| 🎨 Colored terminal output | Display scan results with ANSI colors |
| 📊 Open-port detection | Identify ports that accept TCP connections |
| ⏱️ Connection timeout | Limit individual connection attempts to one second |
| 🛠️ Built-in argument validation | Reject invalid port ranges and thread counts |
| 📦 No external dependencies | Uses Python's standard library |

---

## 📂 Project Structure

A suggested repository structure is:

```text
TCPortscanner/
|
├── Portscanner.py   # Main Python script
└── README.md        # Project documentation
```

---

## 🧠 How It Works

The scanner follows a straightforward workflow.

### 1. Parse command-line arguments

Python's `argparse` module processes the `target`, `port range`, and `number of worker threads`.

The script validates the port range and ensures that at least one worker thread is configured.

### 2. Create a queue of ports

Every port in the specified range is added to a `Queue`.

For example, a range of 20–25 produces the following tasks:

```text
20, 21, 22, 23, 24, 25
```

The queue allows worker threads to retrieve scanning tasks `safely`.

### 3. Start worker threads

The script creates the requested number of threads.

Each worker retrieves a port from the queue and passes it to the TCP scanning function.

This allows multiple connection attempts to occur `concurrently` rather than scanning every port `sequentially`.

### 4. Attempt TCP connections

For each port, the scanner:

```text
- Creates a TCP socket.
- Sets a connection timeout of one second.
- Attempts to connect to the target.
- Marks the port as open if the connection succeeds.
- Closes the socket.
```

A successful connection indicates that the target accepted the TCP connection at the time of the scan.

### 5. Collect open ports

When a connection succeeds, the corresponding port is added to a shared list.

A `threading.Lock` protects updates to that list.

### 6. Display the results

After all scanning tasks have been processed, the script:

```text
- Stops the worker threads.
- Sorts the discovered open ports.
- Displays the open ports in ascending order.
- Reports the number of discovered open ports.
```

---

## 🖥️ Demo

The scanner displays a `banner`, `target information`, `scan progress`, and a `list of discovered open ports`.

Example output:

```text
╭──────────────────────────────────────────╮
│           TCP Port Scanner v1.0          │
╰──────────────────────────────────────────╯

Target       : 192.168.1.1
Total ports  : 9

[•] Starting TCP port scan on 192.168.1.1 at 14:30:25

PORT     STATE
22/tcp   OPEN
80/tcp   OPEN
443/tcp  OPEN

[•] Port scan done: 3 are open
```

> [!NOTE]
> This is an `illustrative` example. Actual results depend on the target host, network conditions, and the selected port range.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|:---|:---|
| `Python 3` |	Core programming language |
| `socket` |	TCP connection attempts |
| `threading` |	Concurrent port scanning |
| `queue.Queue` |	Thread-safe task distribution |
| `argparse` |	Command-line argument parsing |
| `datetime` |	Displaying the scan start time |
| `ANSI escape codes` |	Colored terminal output |

All components are provided by `Python's standard library`.

---

## ⚡ Performance Considerations

`Multithreading` can improve scanning speed because a worker can attempt another connection while other connection attempts are waiting for responses.

However, scanning performance depends on several factors:

```text
- The number of ports being scanned.
- The number of worker threads.
- Network latency and packet loss.
- Target responsiveness.
- Firewall and filtering behavior.
- Operating system networking limits.
```

The connection timeout is set to `one second per attempt`, but this does not guarantee that the entire scan will finish within one second. Total scan time depends on the` number of ports`, `concurrency`, and `network conditions`.

`Increasing the thread count does not always improve performance`. Excessive concurrency may increase resource usage or cause connection attempts to fail.

For most small lab environments, start with the default settings and adjust them as needed.

---

## ⚙️ Requirements

Before running the scanner, make sure you have:

- Python 3 installed.
- Network connectivity to the target.
- Permission to scan the target system.

The script relies entirely on Python's standard library, so no third-party packages are required.

Check your Python installation:

```text
python3 --version
```

---

## 🚀 Installation

### 1. Clone the repository

```text
git clone https://github.com/3078756D627261/TCPortscanner.git
```

### 2. Navigate to the project directory

```text
cd TCPortscanner
```

### 3. Run the scanner

```text
python3 Portscanner.py
```

---

## 💻 Usage

The scanner accepts four command-line arguments:

```text
python3 Portscanner.py [-h] [-t HOST] [-s PORT] [-e PORT] [-T NUMBER]
```

Arguments

| Argument | Long option | Description | Default |
|:---|:---|:---|:---|
| -h | --help |	Display the help message |	— |
| -t | --target |	Target IP address or hostname | 192.168.1.1 |
| -s | --start | First port to scan | 1 |
| -e | --end | Last port to scan | 10 |
| -T | --threads | Number of worker threads |	20 |

> [!IMPORTANT]
> Both the starting and ending ports are included in the scan.

Examples

### 1. Scan the default target and port range

```text
python3 Portscanner.py
```

Scans ports 1–10 on 192.168.1.1 using 20 worker threads.

### 2. Specify a target IP address

```text
python3 Portscanner.py -t 192.168.1.100
```

Scans the default port range on the specified target.

### 3. Scan a custom port range

```text
python3 Portscanner.py -t 192.168.1.100 -s 1 -e 100
```

Scans TCP ports 1–100.

### 4. Scan common service ports

```text
python3 Portscanner.py -t 192.168.1.100 -s 20 -e 443
```

Scans TCP ports 20–443, inclusive.

### 5. Increase the number of threads

```text
python3 Portscanner.py -t 192.168.1.100 -s 1 -e 1000 -T 100
```

Scans ports 1–1000 using 100 worker threads.

### 6. Display the help menu

```text
python3 Portscanner.py --help
```

Displays the available command-line options and their default values.

---

## ⚠️ Limitations

This project is intentionally simple and has several limitations.

- **TCP only**: It does not perform `UDP` scanning.
- **IPv4 only**: The socket is configured with `socket.AF_INET`.
- **Open ports only**: It does not report detailed states such as closed and filtered.
- **No service detection:** It does not identify the applications or services listening on open ports.
- **No banner grabbing**: It does not retrieve service `banners` or application `versions`.
- **Basic timeout handling**: Connection attempts use a fixed one-second timeout.
- **No scan progress indicator**: Results are displayed after the scan completes.
- **No result export**: Results are not automatically saved to a file.
- **No rate limiting**: There is no explicit mechanism for controlling the rate of connection attempts.

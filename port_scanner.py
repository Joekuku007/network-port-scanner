#!/usr/bin/env python3
"""
Network Port Scanner
A simple yet effective port scanner for identifying open ports on a target host.
Useful for network reconnaissance and security auditing.
"""

import socket
import argparse
import sys
from threading import Thread, Lock
from queue import Queue
import time


class PortScanner:
    """Scans a target host for open ports."""

    def __init__(self, target, start_port=1, end_port=65535, timeout=1, threads=50):
        """
        Initialize the port scanner.
        
        Args:
            target: IP address or hostname to scan
            start_port: Starting port number (default: 1)
            end_port: Ending port number (default: 65535)
            timeout: Socket timeout in seconds (default: 1)
            threads: Number of worker threads (default: 50)
        """
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.timeout = timeout
        self.threads_count = threads
        self.open_ports = []
        self.lock = Lock()
        self.queue = Queue()

    def resolve_target(self):
        """Resolve hostname to IP address."""
        try:
            self.target_ip = socket.gethostbyname(self.target)
            print(f"[*] Target resolved: {self.target} -> {self.target_ip}")
            return True
        except socket.gaierror:
            print(f"[!] Error: Could not resolve hostname '{self.target}'")
            return False

    def scan_port(self, port):
        """Attempt to connect to a specific port."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((self.target_ip, port))
            sock.close()

            if result == 0:
                with self.lock:
                    self.open_ports.append(port)
                print(f"[+] Port {port}: OPEN")
            return result == 0
        except socket.timeout:
            return False
        except Exception as e:
            print(f"[!] Error scanning port {port}: {e}")
            return False

    def worker(self):
        """Worker thread that processes ports from the queue."""
        while True:
            port = self.queue.get()
            if port is None:
                break
            self.scan_port(port)
            self.queue.task_done()

    def run(self):
        """Execute the port scan."""
        print(f"\n[*] Scanning {self.target_ip} from port {self.start_port} to {self.end_port}")
        print(f"[*] Using {self.threads_count} threads\n")

        start_time = time.time()

        # Start worker threads
        threads = []
        for _ in range(self.threads_count):
            thread = Thread(target=self.worker, daemon=True)
            thread.start()
            threads.append(thread)

        # Add ports to queue
        for port in range(self.start_port, self.end_port + 1):
            self.queue.put(port)

        # Wait for queue to be processed
        self.queue.join()

        # Stop workers
        for _ in range(self.threads_count):
            self.queue.put(None)
        for thread in threads:
            thread.join()

        elapsed_time = time.time() - start_time

        # Print results
        print(f"\n{'='*50}")
        print(f"Scan Results for {self.target_ip}")
        print(f"{'='*50}")
        if self.open_ports:
            self.open_ports.sort()
            print(f"\nOpen ports found: {len(self.open_ports)}\n")
            for port in self.open_ports:
                service = self.get_service_name(port)
                print(f"  Port {port}: {service}")
        else:
            print("\nNo open ports found.")
        print(f"\nScan completed in {elapsed_time:.2f} seconds")
        print(f"{'='*50}\n")

    @staticmethod
    def get_service_name(port):
        """Get the service name for a given port."""
        common_services = {
            21: "FTP",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            143: "IMAP",
            443: "HTTPS",
            445: "SMB",
            3306: "MySQL",
            3389: "RDP",
            5432: "PostgreSQL",
            5900: "VNC",
            8080: "HTTP-Alt",
            8443: "HTTPS-Alt",
        }
        return common_services.get(port, "Unknown")


def main():
    parser = argparse.ArgumentParser(
        description="Network Port Scanner - Scan a host for open ports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python port_scanner.py 192.168.1.1
  python port_scanner.py example.com -p 1-1000
  python port_scanner.py 10.0.0.1 -p 80,443,3306 -t 5
        """
    )

    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument(
        "-p", "--ports",
        default="1-65535",
        help="Port range (default: 1-65535) or comma-separated list (e.g., 80,443,3306)"
    )
    parser.add_argument(
        "-t", "--timeout",
        type=float,
        default=1,
        help="Socket timeout in seconds (default: 1)"
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=50,
        help="Number of worker threads (default: 50)"
    )

    args = parser.parse_args()

    # Parse ports argument
    if "-" in args.ports:
        try:
            start, end = map(int, args.ports.split("-"))
            start_port, end_port = start, end
        except ValueError:
            print("[!] Invalid port range format. Use 'START-END' (e.g., 1-1000)")
            sys.exit(1)
    else:
        try:
            ports = [int(p.strip()) for p in args.ports.split(",")]
            start_port = min(ports)
            end_port = max(ports)
        except ValueError:
            print("[!] Invalid port format.")
            sys.exit(1)

    # Validate port range
    if start_port < 1 or end_port > 65535 or start_port > end_port:
        print("[!] Invalid port range. Ports must be between 1 and 65535.")
        sys.exit(1)

    # Create and run scanner
    scanner = PortScanner(args.target, start_port, end_port, args.timeout, args.threads)

    if not scanner.resolve_target():
        sys.exit(1)

    try:
        scanner.run()
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
        sys.exit(1)


if __name__ == "__main__":
    main()

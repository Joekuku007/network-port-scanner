#!/usr/bin/env python3
"""
Example usage of the Network Port Scanner
"""

from port_scanner import PortScanner


def example_basic_scan():
    """Example: Basic port scan on localhost."""
    scanner = PortScanner("localhost", start_port=1, end_port=1024)
    if scanner.resolve_target():
        scanner.run()


def example_specific_ports():
    """Example: Scan specific ports."""
    scanner = PortScanner(
        "example.com",
        start_port=80,
        end_port=80,
        threads=10
    )
    if scanner.resolve_target():
        scanner.run()


def example_with_custom_timeout():
    """Example: Scan with custom timeout."""
    scanner = PortScanner(
        "192.168.1.1",
        start_port=1,
        end_port=5000,
        timeout=2,
        threads=100
    )
    if scanner.resolve_target():
        scanner.run()


if __name__ == "__main__":
    print("Network Port Scanner - Example Usage\n")
    example_basic_scan()

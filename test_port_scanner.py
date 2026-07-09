#!/usr/bin/env python3
"""
Unit tests for the Network Port Scanner
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import socket
from port_scanner import PortScanner


class TestPortScanner(unittest.TestCase):
    """Test cases for PortScanner class."""

    def setUp(self):
        """Set up test fixtures."""
        self.scanner = PortScanner("127.0.0.1", start_port=1, end_port=100, threads=5)

    def test_init(self):
        """Test scanner initialization."""
        self.assertEqual(self.scanner.target, "127.0.0.1")
        self.assertEqual(self.scanner.start_port, 1)
        self.assertEqual(self.scanner.end_port, 100)
        self.assertEqual(self.scanner.timeout, 1)
        self.assertEqual(self.scanner.threads_count, 5)
        self.assertEqual(self.scanner.open_ports, [])

    @patch('socket.gethostbyname')
    def test_resolve_target_valid(self, mock_resolve):
        """Test resolving a valid hostname."""
        mock_resolve.return_value = "93.184.216.34"
        result = self.scanner.resolve_target()
        self.assertTrue(result)
        self.assertEqual(self.scanner.target_ip, "93.184.216.34")

    @patch('socket.gethostbyname')
    def test_resolve_target_invalid(self, mock_resolve):
        """Test resolving an invalid hostname."""
        mock_resolve.side_effect = socket.gaierror()
        result = self.scanner.resolve_target()
        self.assertFalse(result)

    @patch('socket.socket')
    def test_scan_port_open(self, mock_socket):
        """Test scanning an open port."""
        mock_instance = MagicMock()
        mock_socket.return_value = mock_instance
        mock_instance.connect_ex.return_value = 0

        self.scanner.target_ip = "127.0.0.1"
        result = self.scanner.scan_port(80)

        self.assertTrue(result)
        self.assertIn(80, self.scanner.open_ports)

    @patch('socket.socket')
    def test_scan_port_closed(self, mock_socket):
        """Test scanning a closed port."""
        mock_instance = MagicMock()
        mock_socket.return_value = mock_instance
        mock_instance.connect_ex.return_value = 1

        self.scanner.target_ip = "127.0.0.1"
        result = self.scanner.scan_port(443)

        self.assertFalse(result)
        self.assertNotIn(443, self.scanner.open_ports)

    def test_get_service_name_known_port(self):
        """Test getting service name for known ports."""
        self.assertEqual(PortScanner.get_service_name(80), "HTTP")
        self.assertEqual(PortScanner.get_service_name(443), "HTTPS")
        self.assertEqual(PortScanner.get_service_name(22), "SSH")

    def test_get_service_name_unknown_port(self):
        """Test getting service name for unknown ports."""
        self.assertEqual(PortScanner.get_service_name(9999), "Unknown")


if __name__ == "__main__":
    unittest.main()

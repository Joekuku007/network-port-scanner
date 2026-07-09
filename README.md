# Network Port Scanner

A fast, multi-threaded port scanner written in Python. Identify open ports on target hosts for network reconnaissance and security auditing.

## Features

- **Multi-threaded scanning** for speed (default: 50 threads)
- **Flexible port selection** - scan ranges or specific ports
- **Service identification** - shows common service names for open ports
- **Hostname resolution** - works with IP addresses or domain names
- **Customizable timeout** - adjust based on network conditions
- **Clean output** - easy-to-read results with timing information

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Installation

```bash
git clone https://github.com/Joekuku007/network-port-scanner.git
cd network-port-scanner
```

## Usage

### Basic Usage

Scan all ports on a target:
```bash
python port_scanner.py 192.168.1.1
```

### Scan a Specific Port Range

```bash
python port_scanner.py example.com -p 1-1000
```

### Scan Specific Ports

```bash
python port_scanner.py 10.0.0.1 -p 80,443,3306,8080
```

### Advanced Options

```bash
python port_scanner.py 192.168.1.1 \
  -p 1-10000 \
  --timeout 2 \
  --threads 100
```

## Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--ports` | `-p` | Port range (START-END) or comma-separated list | `1-65535` |
| `--timeout` | `-t` | Socket timeout in seconds | `1` |
| `--threads` | | Number of worker threads | `50` |

## Examples

Scan common web ports:
```bash
python port_scanner.py 192.168.1.100 -p 80,443,8080,8443
```

Scan with longer timeout for slow networks:
```bash
python port_scanner.py example.com -p 1-10000 --timeout 3
```

Increase threads for faster scanning (use with caution):
```bash
python port_scanner.py 10.0.0.50 -p 1-1000 --threads 200
```

## Output Example

```
[*] Target resolved: example.com -> 93.184.216.34
[*] Scanning 93.184.216.34 from port 1 to 10000
[*] Using 50 threads

[+] Port 80: OPEN
[+] Port 443: OPEN

==================================================
Scan Results for 93.184.216.34
==================================================

Open ports found: 2

  Port 80: HTTP
  Port 443: HTTPS

Scan completed in 3.45 seconds
==================================================
```

## Security Note

- Only scan networks and systems you own or have explicit permission to scan
- Unauthorized port scanning may be illegal in your jurisdiction
- Use responsibly and ethically

## How It Works

The scanner uses Python's `socket` module to attempt TCP connections to ports on the target host. If a connection succeeds, the port is marked as open. Multi-threading significantly speeds up the scan by testing multiple ports simultaneously.

## Learning Outcomes

Building this project demonstrates:
- Socket programming and network protocols
- Multi-threading and concurrent operations
- Command-line argument parsing
- Basic network security concepts
- Python standard library usage

## License

MIT License - Feel free to use and modify

## Contributing

Pull requests welcome! Feel free to enhance the scanner with features like:
- UDP scanning
- Service version detection
- Export results to JSON/CSV
- Scan rate limiting

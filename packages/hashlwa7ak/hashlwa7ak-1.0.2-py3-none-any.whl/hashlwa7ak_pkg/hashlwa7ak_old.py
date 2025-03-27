import socket
import ssl
import ipaddress
from concurrent.futures import ThreadPoolExecutor
import paramiko
import ftplib
import requests
import urllib3
from bs4 import BeautifulSoup
from rich import print
from rich.console import Console
from datetime import datetime
import json
import sys

# Setup console for rich output
console = Console()

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

COMMON_PORTS = [21, 22, 80, 443, 3306]
ADMIN_PATHS = ["/admin", "/login", "/dashboard", "/cpanel", "/admin.php"]
SUBDOMAINS = ["admin", "vpn", "dev", "test", "portal", "mail"]
SECURITY_HEADERS = ["X-Frame-Options", "Content-Security-Policy", "Strict-Transport-Security", "X-XSS-Protection"]

PORT_SERVICES = {
    21: "FTP",
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL",
}

PORT_VULNS = {
    21: "FTP often allows anonymous or default logins",
    22: "SSH could be brute-forced if default creds are used",
    80: "HTTP may expose outdated CMS, XSS, SQLi, etc.",
    443: "HTTPS might have weak SSL configs or expired certs",
    3306: "MySQL may be exposed with no password"
}

DEFAULT_CREDS = {
    21: [("anonymous", "anonymous"), ("ftp", "ftp")],
    22: [("root", "toor"), ("admin", "admin")]
}

report_lines = []
html_report = []
json_report = {
    "targets": [],
    "open_ports": [],
    "security_issues": [],
    "cookies": [],
    "admin_paths": [],
    "subdomains": []
}

summary = {
    "total_ports_open": 0,
    "cookies_found": 0,
    "admin_paths": 0,
    "hosts_scanned": 0
}

def write_report(line):
    """Appends a message to both the console and the HTML/text reports."""
    report_lines.append(line)
    html_report.append(f"<p>{line}</p>")
    console.print(line)

def check_license_key():
    """Reads 'license.txt' and compares it against a valid license key."""
    try:
        with open("license.txt", "r") as f:
            stored_key = f.read().strip()  # Read the key from the file
            
        valid_license_key = "1234567890abcdef"  # Example valid key

        if stored_key == valid_license_key:
            print("License key is valid!")
            return True
        else:
            print("Invalid license key!")
            return False
    except FileNotFoundError:
        print("License file 'license.txt' not found!")
        return False

def try_ftp_login(ip):
    """Attempts FTP login with default creds."""
    for username, password in DEFAULT_CREDS[21]:
        try:
            with ftplib.FTP() as ftp:
                ftp.connect(ip, 21, timeout=1)
                ftp.login(user=username, passwd=password)
                write_report(f"[bold red][!] FTP Login SUCCESS on {ip} with {username}:{password}[/bold red]")
                return
        except:
            continue

def try_ssh_login(ip):
    """Attempts SSH login with default creds."""
    for username, password in DEFAULT_CREDS[22]:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, port=22, username=username, password=password, timeout=2)
            write_report(f"[bold red][!] SSH Login SUCCESS on {ip} with {username}:{password}[/bold red]")
            ssh.close()
            return
        except:
            continue

def get_ssl_cert(ip):
    """Retrieves and prints SSL cert details for HTTPS scanning."""
    try:
        context = ssl.create_default_context()
        with socket.create_connection((ip, 443), timeout=3) as sock:
            with context.wrap_socket(sock, server_hostname=ip) as ssock:
                cert = ssock.getpeercert()
                subject = dict(x[0] for x in cert['subject'])
                issuer = dict(x[0] for x in cert['issuer'])
                write_report(f"    └─ 🔒 SSL Cert Subject: {subject.get('commonName', 'N/A')}")
                write_report(f"    └─ 🔒 SSL Cert Issuer: {issuer.get('commonName', 'N/A')}")
                write_report(f"    └─ 🔒 SSL Expiry: {cert['notAfter']}")
    except Exception as e:
        write_report(f"    └─ ⚠️  SSL cert parse failed: {e}")

def scan_web(ip, port):
    """Scans HTTP/HTTPS for security headers, cookies, robots.txt, login forms, admin paths."""
    protocol = "https" if port == 443 else "http"
    url = f"{protocol}://{ip}"
    write_report(f"[cyan]    🌐 Scanning Web: {url}[/cyan]")

    # If HTTPS, try to parse SSL certificate
    if port == 443:
        get_ssl_cert(ip)

    try:
        response = requests.get(url, timeout=5, verify=False)
        server = response.headers.get('Server', 'Unknown')
        write_report(f"    └─ 🛠️  Server Header: {server}")

        # Check security headers
        for header in SECURITY_HEADERS:
            if header in response.headers:
                write_report(f"    └─ ✅ Security Header Found: {header}")
            else:
                write_report(f"    └─ ❌ Missing Security Header: {header}")
                json_report["security_issues"].append({"ip": ip, "header_missing": header})

        # Cookies
        cookies = response.cookies
        if cookies:
            cookie_names = [c.name for c in cookies]
            summary["cookies_found"] += len(cookie_names)
            write_report(f"    └─ 🍪 Cookies: {cookie_names}")
            json_report["cookies"].append({"ip": ip, "cookies": cookie_names})
        else:
            write_report("    └─ 🍪 No cookies found.")

        # Attempt to get robots.txt
        try:
            robots = requests.get(f"{url}/robots.txt", timeout=3, verify=False)
            if robots.status_code == 200:
                write_report("    └─ 🤖 robots.txt found:")
                for line in robots.text.splitlines():
                    if line.strip():
                        write_report(f"        • {line.strip()}")
            else:
                write_report("    └─ 🤖 No robots.txt found.")
        except:
            write_report("    └─ 🤖 robots.txt scan failed.")

        # Check for a login form
        soup = BeautifulSoup(response.text, 'html.parser')
        forms = soup.find_all('form')
        for form in forms:
            if form.find('input', {'type': 'password'}):
                write_report("    └─ 🔐 Login form detected on main page")
                break

        # Brute-force known admin paths
        for path in ADMIN_PATHS:
            full_url = url + path
            try:
                r = requests.get(full_url, timeout=3, verify=False)
                if r.status_code == 200:
                    write_report(f"    └─ 🕵️ Admin path found: {path}")
                    summary["admin_paths"] += 1
                    json_report["admin_paths"].append({"ip": ip, "path": path})
            except:
                continue
    except Exception as e:
        write_report(f"    └─ ⚠️  Web scan failed: {e}")

def scan_port(ip, port):
    """Attempts to connect on the given port. If open, tries known checks (FTP, SSH, etc.)."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            result = s.connect_ex((str(ip), port))
            if result == 0:
                summary["total_ports_open"] += 1
                service = PORT_SERVICES.get(port, "Unknown")
                vuln = PORT_VULNS.get(port, "No known default vuln in this scan.")
                write_report(f"[green][+] {ip}:{port} ({service}) is OPEN[/green]")
                write_report(f"    └─ 💡 Potential Vuln: {vuln}")
                # Store in JSON
                json_report["open_ports"].append({
                    "ip": str(ip),
                    "port": port,
                    "service": service
                })

                # Perform extra checks
                if port in [80, 443]:
                    scan_web(str(ip), port)
                if port == 21:
                    try_ftp_login(str(ip))
                elif port == 22:
                    try_ssh_login(str(ip))
    except Exception:
        pass

def scan_ip_range(start_ip, end_ip):
    """Scans all IPs in the given start->end range, storing results."""
    start = ipaddress.IPv4Address(start_ip)
    end = ipaddress.IPv4Address(end_ip)
    total_hosts = int(end) - int(start) + 1
    summary["hosts_scanned"] += total_hosts
    write_report(f"[*] Scanning from {start} to {end}...\n")

    with ThreadPoolExecutor(max_workers=100) as executor:
        for ip_int in range(int(start), int(end) + 1):
            ip = ipaddress.IPv4Address(ip_int)
            # Convert to string before storing in JSON
            json_report["targets"].append(str(ip))
            for port in COMMON_PORTS:
                executor.submit(scan_port, ip, port)

def brute_subdomains(base_ip_or_domain):
    """Attempts to resolve known subdomains for the given IP or domain."""
    write_report("\n[bold cyan]🔎 Starting Subdomain Scan...[/bold cyan]")
    for sub in SUBDOMAINS:
        subdomain = f"{sub}.{base_ip_or_domain}"
        try:
            socket.gethostbyname(subdomain)
            write_report(f"[blue]✔️ Subdomain Found: {subdomain}[/blue]")
            json_report["subdomains"].append(subdomain)
        except:
            continue

def hashlwa7ak_scan(target, output_name="report"):
    """Main function to run the license check, parse IP, run scans, and save reports."""
    # License check
    if not check_license_key():
        print("Exiting due to invalid or missing license key.")
        sys.exit(1)

    # Parse single IP or CIDR
    if "/" in target:
        net = ipaddress.ip_network(target, strict=False)
        start_ip = str(net.network_address)
        end_ip = str(net.broadcast_address)
    else:
        start_ip = end_ip = target

    # Scan
    scan_ip_range(start_ip, end_ip)
    brute_subdomains(start_ip)

    # Summaries
    write_report("\n[bold yellow]📊 Scan Summary:[/bold yellow]")
    write_report(f"• Hosts scanned: {summary['hosts_scanned']}")
    write_report(f"• Total open ports: {summary['total_ports_open']}")
    write_report(f"• Admin paths found: {summary['admin_paths']}")
    write_report(f"• Cookies found: {summary['cookies_found']}")

    # Save .txt
    with open(f"{output_name}.txt", "w") as f:
        for line in report_lines:
            f.write(f"{line}\n")

    # Save .html
    with open(f"{output_name}.html", "w") as f:
        f.write("""
        <html>
        <head>
        <title>hashlwa7ak Report</title>
        <style>
        body { font-family: Arial, sans-serif; background: #0e0e0e; color: #00ff88; padding: 20px; }
        h1 { color: #00ffff; }
        p { margin: 5px 0; }
        </style>
        </head>
        <body>
        <h1>hashlwa7ak Scan Report</h1>
        """)
        for line in html_report:
            f.write(line)
        f.write("</body></html>")

    # Save .json with default=str to handle IPv4Address
    with open(f"{output_name}.json", "w") as f:
        json.dump(json_report, f, indent=2, default=str)

    console.print(
        f"\n[bold green]✅ Scan complete. Results saved to [underline]{output_name}.txt[/underline], "
        f"[underline]{output_name}.html[/underline], and [underline]{output_name}.json[/underline][/bold green]"
    )

if __name__ == "__main__":
    start_ip = input("Enter start IP (or CIDR): ").strip()
    if "/" in start_ip:
        net = ipaddress.ip_network(start_ip, strict=False)
        start_ip = str(net.network_address)
        end_ip = str(net.broadcast_address)
    else:
        end_ip = input("Enter end IP: ").strip()

    hashlwa7ak_scan(start_ip, end_ip)

from hashlwa7ak_pkg.hashlwa7ak_old import hashlwa7ak_scan
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='hashlwa7ak - Cyber Recon Scanner')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan an IP or CIDR')
    scan_parser.add_argument('--target', required=True, help='Target IP or CIDR')
    scan_parser.add_argument('--output', help='Output report base name (default: report)')

    args = parser.parse_args()

    if args.command == 'scan':
        base_name = args.output if args.output else "report"
        hashlwa7ak_scan(target=args.target, output_name=base_name)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()

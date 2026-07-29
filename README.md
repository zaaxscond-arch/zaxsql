
readme_content = """# ZAXSQL_ - Advanced SQL Injection Toolkit

```
    ███████╗ █████╗ ██╗  ██╗███████╗ ██████╗ ██╗     
    ╚══███╔╝██╔══██╗╚██╗██╔╝██╔════╝██╔═══██╗██║     
      ███╔╝ ███████║ ╚███╔╝ ███████╗██║   ██║██║     
     ███╔╝  ██╔══██║ ██╔██╗ ╚════██║██║▄▄ ██║██║     
    ███████╗██║  ██║██╔╝ ██╗███████║╚██████╔╝███████╗
    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚══▀▀═╝ ╚══════╝
                    v2.0 - By zaxsql_
```

## Overview

ZAXSQL_ is a comprehensive SQL injection testing toolkit designed for security professionals and researchers. It supports multiple DBMS types, various injection techniques, and advanced evasion methods.

## Features

- **Multiple Injection Types**: Error-based, Union-based, Boolean-based Blind, Time-based Blind, Stacked Queries
- **DBMS Support**: MySQL, PostgreSQL, MSSQL, Oracle, SQLite
- **WAF Evasion**: Built-in tamper scripts and encoding techniques
- **Data Extraction**: Automated database, table, column enumeration and data dumping
- **Proxy Support**: HTTP/HTTPS proxy, Tor integration
- **Multi-threading**: Fast scanning with configurable thread count

## Installation

```bash
git clone https://github.com/zaxsql_/zaxsql_.git
cd zaxsql_
pip install -r requirements.txt
```

## Usage

### Basic Scan
```bash
python zaxsql_.py -u "http://target.com/page.php?id=1"
```

### Enumerate Databases
```bash
python zaxsql_.py -u "http://target.com/page.php?id=1" --dbs
```

### Dump All Data
```bash
python zaxsql_.py -u "http://target.com/page.php?id=1" --dump
```

### POST Request
```bash
python zaxsql_.py -u "http://target.com/login.php" --data "username=admin&password=test"
```

### With Proxy
```bash
python zaxsql_.py -u "http://target.com/page.php?id=1" --proxy http://127.0.0.1:8080
```

### Tor Support
```bash
python zaxsql_.py -u "http://target.com/page.php?id=1" --tor
```

### Tamper Scripts
```bash
python zaxsql_.py -u "http://target.com/page.php?id=1" --tamper space2comment
```

### Full Scan
```bash
python zaxsql_.py -u "http://target.com/page.php?id=1" --level 5 --risk 3 --dbs --tables --dump
```

## Options

| Option | Description |
|--------|-------------|
| `-u, --url` | Target URL |
| `--data` | POST data |
| `--cookie` | HTTP cookies |
| `--headers` | Custom headers |
| `--proxy` | Proxy URL |
| `--threads` | Number of threads (default: 10) |
| `--timeout` | Request timeout (default: 10) |
| `--level` | Scan level 1-5 (default: 1) |
| `--risk` | Risk level 1-3 (default: 1) |
| `--dbms` | Force DBMS type |
| `--dump` | Dump database contents |
| `--dbs` | Enumerate databases |
| `--tables` | Enumerate tables |
| `--columns` | Enumerate columns |
| `--batch` | Non-interactive mode |
| `--tamper` | Use tamper script |
| `--random-agent` | Random User-Agent |
| `--tor` | Use Tor proxy |

## Tamper Scripts

| Script | Description |
|--------|-------------|
| `space2comment` | Replace spaces with `/**/` |
| `space2plus` | Replace spaces with `+` |
| `charencode` | URL encode all characters |
| `randomcase` | Randomize case |
| `base64encode` | Base64 encode payload |

## Project Structure

```
zaxsql_/
├── zaxsql_.py              # Entry point utama
├── core/
│   ├── scanner.py          # Deteksi SQLi vulnerability
│   ├── injector.py         # Payload injection engine
│   ├── extractor.py        # Data extraction
│   ├── waf_bypass.py       # WAF/IDS evasion
│   ├── tamper.py           # Payload tampering
│   └── blind.py            # Blind SQLi
├── payloads/
│   ├── error_based.txt
│   ├── union_based.txt
│   ├── blind_time.txt
│   ├── blind_bool.txt
│   └── stacked.txt
├── utils/
│   ├── colors.py
│   ├── requester.py
│   ├── parser.py
│   └── logger.py
├── config/
│   └── settings.py
├── requirements.txt
├── README.md
└── LICENSE
```

## Requirements

- Python 3.8+
- requests
- beautifulsoup4
- lxml
- colorama
- pysocks
- urllib3

## License

MIT License - See LICENSE file for details.

## Author

**zaxsql_**

---

*This tool is intended for authorized security testing and research purposes only.*
"""

with open('/mnt/agents/output/README.md', 'w', encoding='utf-8') as f:
    f.write(readme_content)

print("README.md created successfully!")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Global Configuration
"""

import os

class Config:
    # Request settings
    DEFAULT_TIMEOUT = 10
    DEFAULT_THREADS = 10
    MAX_RETRIES = 3
    DELAY_BETWEEN_REQUESTS = 0.5
    
    # Scan settings
    DEFAULT_LEVEL = 1
    MAX_LEVEL = 5
    DEFAULT_RISK = 1
    MAX_RISK = 3
    
    # Payload settings
    PAYLOADS_DIR = os.path.join(os.path.dirname(__file__), '..', 'payloads')
    
    # Output settings
    OUTPUT_DIR = 'output'
    LOG_DIR = 'logs'
    
    # Proxy settings
    TOR_PROXY = 'socks5h://127.0.0.1:9050'
    
    # User agents
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
    ]
    
    # DBMS fingerprints
    DBMS_FINGERPRINTS = {
        'mysql': ['@@version', 'information_schema'],
        'mssql': ['@@VERSION', 'sysdatabases', 'sysobjects'],
        'postgres': ['version()', 'pg_catalog', 'pg_database'],
        'oracle': ['v$version', 'ALL_TABLES', 'DUAL'],
        'sqlite': ['sqlite_version()', 'sqlite_master'],
    }

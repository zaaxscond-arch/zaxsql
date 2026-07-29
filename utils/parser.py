#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
URL & Form Parser
"""

import urllib.parse
import re
from bs4 import BeautifulSoup

class URLParser:
    @staticmethod
    def extract_params(url):
        parsed = urllib.parse.urlparse(url)
        return urllib.parse.parse_qs(parsed.query)
    
    @staticmethod
    def build_url(base, params):
        query = urllib.parse.urlencode(params, doseq=True)
        parsed = urllib.parse.urlparse(base)
        return urllib.parse.urlunparse(parsed._replace(query=query))
    
    @staticmethod
    def is_valid_url(url):
        regex = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, url) is not None

class FormParser:
    @staticmethod
    def parse_forms(html):
        soup = BeautifulSoup(html, 'html.parser')
        forms = []
        
        for form in soup.find_all('form'):
            form_data = {
                'action': form.get('action', ''),
                'method': form.get('method', 'GET').upper(),
                'inputs': []
            }
            
            for input_tag in form.find_all(['input', 'textarea', 'select']):
                input_data = {
                    'name': input_tag.get('name', ''),
                    'type': input_tag.get('type', 'text'),
                    'value': input_tag.get('value', '')
                }
                form_data['inputs'].append(input_data)
            
            forms.append(form_data)
        
        return forms

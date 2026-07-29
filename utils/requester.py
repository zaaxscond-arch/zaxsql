#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTTP Request Handler
"""

import requests
import random
import time
from urllib.parse import urlparse

class Requester:
    def __init__(self, proxy=None, timeout=10, random_agent=False, tor=False):
        self.session = requests.Session()
        self.timeout = timeout
        self.random_agent = random_agent
        self.proxy = proxy
        self.tor = tor
        
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101',
        ]
        
        if tor:
            self.proxy = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
        elif proxy:
            self.proxy = {'http': proxy, 'https': proxy}
        else:
            self.proxy = None
        
        self.session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
    
    def _get_headers(self, custom_headers=None):
        headers = dict(self.session.headers)
        
        if self.random_agent:
            headers['User-Agent'] = random.choice(self.user_agents)
        else:
            headers['User-Agent'] = self.user_agents[0]
        
        if custom_headers:
            if isinstance(custom_headers, str):
                # Parse string headers
                for line in custom_headers.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        headers[key.strip()] = value.strip()
            elif isinstance(custom_headers, dict):
                headers.update(custom_headers)
        
        return headers
    
    def get(self, url, headers=None, cookies=None):
        try:
            response = self.session.get(
                url,
                headers=self._get_headers(headers),
                cookies=cookies,
                proxies=self.proxy,
                timeout=self.timeout,
                allow_redirects=True,
                verify=False
            )
            return response
        except requests.exceptions.RequestException as e:
            return None
    
    def post(self, url, data=None, headers=None, cookies=None):
        try:
            response = self.session.post(
                url,
                data=data,
                headers=self._get_headers(headers),
                cookies=cookies,
                proxies=self.proxy,
                timeout=self.timeout,
                allow_redirects=True,
                verify=False
            )
            return response
        except requests.exceptions.RequestException as e:
            return None
    
    def put(self, url, data=None, headers=None, cookies=None):
        try:
            response = self.session.put(
                url,
                data=data,
                headers=self._get_headers(headers),
                cookies=cookies,
                proxies=self.proxy,
                timeout=self.timeout,
                allow_redirects=True,
                verify=False
            )
            return response
        except requests.exceptions.RequestException as e:
            return None

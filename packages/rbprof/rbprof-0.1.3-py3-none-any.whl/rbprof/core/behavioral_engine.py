import json
import hashlib
from datetime import datetime
import numpy as np  

class BehaviorEngine:
    def __init__(self):
        self.crypto_apis = ["CryptEncrypt", "BCryptEncrypt"]
        self.suspicious_ips = {"185.143.223.47"}

    def analyze(self, x_prime):
        """Transform X' → X'' with behavioral indicators"""
        # Simulate API monitoring (real-world: use API hooks)
        api_calls = self._trace_apis(x_prime["file"])
        
        # Simulate network analysis
        network = self._check_network(x_prime["file"])
        
        return {
            **x_prime,
            "apis": api_calls,
            "network": network,
            "process_tree": self._get_process_tree(),
            "timestamp": str(datetime.now())
        }

    def _trace_apis(self, filepath):
        """Mock: Replace with actual API monitoring"""
        if "malware" in filepath:
            return ["FindFirstFileW", "CryptEncrypt", "DeleteShadowCopies"]
        return []

    def _check_network(self, filepath):
        """Mock: Replace with packet capture"""
        return {
            "connections": [
                {"dst_ip": "185.143.223.47", "port": 443, "protocol": "HTTPS"}
            ] if "malware" in filepath else []
        }

    def _get_process_tree(self):
        """Mock: Get parent-child processes"""
        return ["explorer.exe → cmd.exe → vssadmin.exe"] if "malware" in filepath else []
import json
import hashlib
from datetime import datetime
import numpy as np  

class MonitoringModule:
    @staticmethod
    def calculate_entropy(data):
        """Compute Shannon entropy (0-8 scale)"""
        if not data:
            return 0
        entropy = 0
        for x in range(256):
            p_x = data.count(x) / len(data)
            if p_x > 0:
                entropy += -p_x * np.log2(p_x)
        return entropy

    def scan(self, filepath):
        """Transform X → X' with initial flags"""
        with open(filepath, "rb") as f:
            data = f.read()
        
        return {
            "file": filepath,
            "entropy": self.calculate_entropy(data),
            "size_MB": len(data) / (1024 * 1024),
            "extension": filepath.split(".")[-1],
            "is_suspicious": self.calculate_entropy(data) > 7.0 
        }
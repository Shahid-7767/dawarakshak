import hashlib
import json
from datetime import datetime, timezone

class Block:
    def __init__(self, index, transactions, previous_hash, timestamp=None):
        self.index = index
        self.timestamp = timestamp or datetime.now(timezone.utc).isoformat()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        content = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
        }
        encoded = json.dumps(content, sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha256(encoded).hexdigest()

    def to_dict(self):
        return {
            "index": self.index, "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash, "hash": self.hash
        }

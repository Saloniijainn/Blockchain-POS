import hashlib
import json
import time
import random

class PoSBlockchain:
    def __init__(self):
        self.chain = []
        self.stakes = {}  # node_id → amount staked
        self.create_block(validator="genesis", previous_hash='0')

    def register_node(self, node_id, stake_amount):
        """Add or top up a node's stake."""
        if stake_amount <= 0:
            raise ValueError("Stake amount must be positive")
        self.stakes[node_id] = self.stakes.get(node_id, 0) + stake_amount

    def total_stake(self):
        return sum(self.stakes.values())

    def choose_validator(self):
        """Randomly pick a node weighted by its stake."""
        total = self.total_stake()
        if total == 0:
            return None
        pick = random.uniform(0, total)
        current = 0
        for node, stake in self.stakes.items():
            current += stake
            if current >= pick:
                return node

    def create_block(self, validator, previous_hash):
        """Create a new block in the blockchain."""
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'validator': validator,
            'previous_hash': previous_hash,
            'transactions': [],  # For future extensibility
            'stake_distribution': dict(self.stakes)  # Snapshot of current stakes
        }
        block['hash'] = self.hash(block)
        self.chain.append(block)
        return block

    def propose_block(self):
        """Create and add a new block to the chain."""
        validator = self.choose_validator()
        if not validator:
            raise RuntimeError("No stakes registered - cannot choose validator")
        prev_hash = self.chain[-1]['hash']
        return self.create_block(validator, prev_hash)

    @staticmethod
    def hash(block):
        """Create a SHA-256 hash of a block."""
        block_copy = block.copy()
        block_copy.pop('hash', None)  # Don't hash the existing hash
        block_string = json.dumps(block_copy, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def is_chain_valid(self):
        """Verify the blockchain's integrity."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current['previous_hash'] != previous['hash']:
                return False
            if current['hash'] != self.hash(current):
                return False
        return True
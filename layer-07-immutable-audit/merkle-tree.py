#!/usr/bin/env python3
"""
AVIK Sandbox Shield - Layer 7: Merkle Tree Implementation
---------------------------------------------------------
A standalone, robust implementation of a cryptographic Merkle Tree.
Used by the Immutable Audit daemon to mathematically prove the 
integrity of the system logs.
"""

import hashlib
from typing import List

class MerkleNode:
    """Represents a node in the Merkle Tree."""
    def __init__(self, left, right, value: str):
        self.left = left
        self.right = right
        self.value = value
        self.hash = self._calculate_hash(value) if value else self._calculate_parent_hash(left, right)

    @staticmethod
    def _calculate_hash(data: str) -> str:
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    @staticmethod
    def _calculate_parent_hash(left, right) -> str:
        combined = left.hash + right.hash
        return hashlib.sha256(combined.encode('utf-8')).hexdigest()


class MerkleTree:
    """
    Constructs a Merkle Tree from a list of data blocks (log entries).
    Provides functions to retrieve the Root Hash and verify integrity.
    """
    def __init__(self, data_blocks: List[str]):
        self.leaves = []
        self.root = None
        
        if not data_blocks:
            # Handle empty tree
            self.root = MerkleNode(None, None, "EMPTY_TREE")
            return
            
        self._build_tree(data_blocks)

    def _build_tree(self, data_blocks: List[str]):
        # Create leaf nodes
        for data in data_blocks:
            self.leaves.append(MerkleNode(None, None, data))

        # Build tree level by level
        current_level = self.leaves
        while len(current_level) > 1:
            next_level = []
            
            # Group nodes in pairs
            for i in range(0, len(current_level), 2):
                left_node = current_level[i]
                
                # If odd number of nodes, duplicate the last node to form a pair
                if i + 1 < len(current_level):
                    right_node = current_level[i + 1]
                else:
                    right_node = left_node
                    
                parent_node = MerkleNode(left_node, right_node, None)
                next_level.append(parent_node)
                
            current_level = next_level
            
        self.root = current_level[0]

    def get_root_hash(self) -> str:
        """Returns the cryptographic root hash of the entire tree."""
        if self.root:
            return self.root.hash
        return ""

    @staticmethod
    def verify_integrity(original_root_hash: str, current_data_blocks: List[str]) -> bool:
        """
        Rebuilds the tree from the current data blocks and checks 
        if the new root hash matches the known good original root hash.
        """
        temp_tree = MerkleTree(current_data_blocks)
        return temp_tree.get_root_hash() == original_root_hash


if __name__ == "__main__":
    # Quick sanity check
    logs = ["Event A", "Event B", "Event C"]
    tree = MerkleTree(logs)
    print(f"Sanity Check Root Hash: {tree.get_root_hash()}")

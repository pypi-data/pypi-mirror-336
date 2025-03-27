from abc import ABC, abstractmethod
from typing import Tuple, List, Optional, Iterator, Any, Protocol, TypeVar, Generic
import bisect
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from error import Error

T = TypeVar('T')

# 抽象存储引擎接口定义，接入不同的存储引擎，目前支持内存和简单的磁盘 KV 存储
class Engine(ABC):
    """
    Abstract storage engine interface.
    Supports different storage engines like memory and simple disk KV storage.
    """
    
    @abstractmethod
    def begin(self, readonly: bool = False):
        """
        Begin a transaction.
        
        Args:
            readonly: Whether the transaction is read-only
            
        Returns:
            A transaction object
            
        Raises:
            Error: If the operation fails
        """
        pass
    
    @abstractmethod
    def set(self, key: bytes, value: bytes) -> None:
        """
        Set key/value pair in the engine.
        
        Args:
            key: The key in bytes
            value: The value in bytes
        
        Raises:
            Error: If the operation fails
        """
        pass
    
    @abstractmethod
    def get(self, key: bytes) -> Optional[bytes]:
        """
        Get value for given key.
        
        Args:
            key: The key to look up
            
        Returns:
            The value if found, None otherwise
            
        Raises:
            Error: If the operation fails
        """
        pass
    
    @abstractmethod
    def delete(self, key: bytes) -> None:
        """
        Delete the key and its associated value.
        If key doesn't exist, the operation is ignored.
        
        Args:
            key: The key to delete
            
        Raises:
            Error: If the operation fails
        """
        pass
    
    @abstractmethod
    def scan(self, start: Optional[bytes] = None, end: Optional[bytes] = None, 
             include_start: bool = True, include_end: bool = False) -> Iterator[Tuple[bytes, bytes]]:
        """
        Scan the engine for key-value pairs within a range.
        
        Args:
            start: Start of the range (inclusive if include_start is True)
            end: End of the range (inclusive if include_end is True)
            include_start: Whether to include the start key in results
            include_end: Whether to include the end key in results
            
        Returns:
            Iterator of (key, value) tuples
            
        Raises:
            Error: If the operation fails
        """
        pass
    
    def scan_prefix(self, prefix: bytes) -> Iterator[Tuple[bytes, bytes]]:
        """
        Scan the engine for key-value pairs with a given prefix.
        
        Args:
            prefix: The prefix to scan for
            
        Returns:
            Iterator of (key, value) tuples where key starts with prefix
            
        Raises:
            Error: If the operation fails
        """
        # Calculate the upper bound by incrementing the last byte of the prefix
        if not prefix:
            return self.scan()
            
        end_prefix = bytearray(prefix)
        # Find the last byte and increment it
        for i in range(len(end_prefix) - 1, -1, -1):
            if end_prefix[i] < 255:
                end_prefix[i] += 1
                break
            else:
                end_prefix[i] = 0
                # If we've reached the start and haven't broken, all bytes are 255
                if i == 0:
                    # Add a new byte
                    end_prefix.append(0)
                
        return self.scan(prefix, bytes(end_prefix), include_start=True, include_end=False)
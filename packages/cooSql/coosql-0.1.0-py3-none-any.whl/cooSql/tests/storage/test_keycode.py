import unittest
import os
import sys
import struct

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from storage.keycode import KeyEncoder, KeyDecoder


class TestKeycode(unittest.TestCase):
    """键编码和解码测试"""
    
    def test_key_encode_decode(self):
        """测试键的编码和解码"""
        # 测试用例：(前缀, 键, 编码后的期望结果)
        test_cases = [
            (b"", b"", b"\x00"),
            (b"", b"a", b"a\x00"),
            (b"", b"abc", b"abc\x00"),
            (b"prefix", b"", b"prefix\x00"),
            (b"prefix", b"key", b"prefixkey\x00"),
            # 测试边界字符
            (b"", bytes([0]), bytes([0, 0])),
            (b"", bytes([255]), bytes([255, 0])),
            # 复杂前缀和键
            (b"p1\x00p2", b"k1\x00k2", b"p1\x00p2k1\x00k2\x00"),
        ]
        
        encoder = KeyEncoder()
        decoder = KeyDecoder()
        
        for prefix, key, expected in test_cases:
            # 测试编码
            encoded = encoder.encode(prefix, key)
            self.assertEqual(encoded, expected, f"编码错误: prefix={prefix}, key={key}")
            
            # 测试解码
            decoded = decoder.decode(encoded, len(prefix))
            self.assertEqual(decoded, key, f"解码错误: encoded={encoded}, prefix_len={len(prefix)}")
    
    def test_prefix_encode(self):
        """测试前缀编码"""
        encoder = KeyEncoder()
        
        # 测试用例：(前缀, 编码后的期望结果)
        test_cases = [
            (b"", b""),
            (b"a", b"a"),
            (b"abc", b"abc"),
            (b"a\x00b", b"a\x00b"),
        ]
        
        for prefix, expected in test_cases:
            encoded = encoder.encode_prefix(prefix)
            self.assertEqual(encoded, expected, f"前缀编码错误: prefix={prefix}")
    
    def test_transaction_key_encode_decode(self):
        """测试事务键的编码和解码"""
        encoder = KeyEncoder()
        decoder = KeyDecoder()
        
        # 测试用例：(事务ID, 键, 编码后的期望结果)
        test_cases = [
            (1, b"key1", b"\x00\x00\x00\x00\x00\x00\x00\x01key1\x00"),
            (123456789, b"", b"\x00\x00\x00\x00\x07[\xcd\x15\x00"),
            (0, b"abc", b"\x00\x00\x00\x00\x00\x00\x00\x00abc\x00"),
            # 最大事务ID
            (0xffffffffffffffff, b"key", b"\xff\xff\xff\xff\xff\xff\xff\xffkey\x00"),
        ]
        
        for tx_id, key, expected in test_cases:
            # 测试编码
            encoded = encoder.encode_txn(tx_id, key)
            self.assertEqual(encoded, expected, f"事务键编码错误: tx_id={tx_id}, key={key}")
            
            # 测试解码
            decoded_id, decoded_key = decoder.decode_txn(encoded)
            self.assertEqual(decoded_id, tx_id, f"事务ID解码错误: encoded={encoded}")
            self.assertEqual(decoded_key, key, f"事务键解码错误: encoded={encoded}")
    
    def test_ts_key_encode_decode(self):
        """测试时间戳键的编码和解码"""
        encoder = KeyEncoder()
        decoder = KeyDecoder()
        
        # 测试用例：(时间戳, 编码后的期望结果)
        test_cases = [
            (1, b"ts\0\0\0\0\0\0\0\0\1"),
            (123456789, b"ts\0\0\0\0\0\07[\xcd\x15"),
            (0, b"ts\0\0\0\0\0\0\0\0\0"),
            # 最大时间戳
            (0xffffffffffffffff, b"ts\0\xff\xff\xff\xff\xff\xff\xff\xff"),
        ]
        
        for ts, expected in test_cases:
            # 测试编码
            encoded = encoder.encode_ts(ts)
            self.assertEqual(encoded, expected, f"时间戳键编码错误: ts={ts}")
            
            # 测试解码
            decoded = decoder.decode_ts(encoded)
            self.assertEqual(decoded, ts, f"时间戳解码错误: encoded={encoded}")


if __name__ == "__main__":
    unittest.main()
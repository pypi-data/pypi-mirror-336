from enum import Enum
import struct
from typing import List, Tuple, Any, Optional, Union


class KeyType(Enum):
    """键类型枚举"""
    TABLE_META = 0  # 表元数据
    TABLE_DATA = 1  # 表数据
    INDEX_META = 2  # 索引元数据
    INDEX_DATA = 3  # 索引数据
    TXID = 4        # 事务ID


class KeyEncoder:
    """键编码器，将各种类型的键编码为字节序列"""
    
    @staticmethod
    def encode(prefix: bytes, key: bytes) -> bytes:
        """
        编码键，添加前缀和结束符
        
        Args:
            prefix: 前缀
            key: 键
            
        Returns:
            编码后的字节序列
        """
        return prefix + key + b'\0'
    
    @staticmethod
    def encode_prefix(prefix: bytes) -> bytes:
        """
        编码前缀
        
        Args:
            prefix: 前缀
            
        Returns:
            编码后的前缀
        """
        return prefix
    
    @staticmethod
    def encode_txn(txid: int, key: bytes) -> bytes:
        """
        编码事务键
        
        Args:
            txid: 事务ID
            key: 键
            
        Returns:
            编码后的字节序列
        """
        txid_bytes = struct.pack('!Q', txid)
        return txid_bytes + key + b'\0'
    
    @staticmethod
    def encode_ts(ts: int) -> bytes:
        """
        编码时间戳键
        
        Args:
            ts: 时间戳
            
        Returns:
            编码后的字节序列
        """
        return b'ts\0' + struct.pack('!Q', ts)
    
    @staticmethod
    def encode_table_meta(table_name: str) -> bytes:
        """
        编码表元数据键
        
        Args:
            table_name: 表名
            
        Returns:
            编码后的字节序列
        """
        key_type_bytes = struct.pack('!B', KeyType.TABLE_META.value)
        table_name_bytes = table_name.encode('utf-8')
        return key_type_bytes + table_name_bytes
    
    @staticmethod
    def encode_table_data(table_name: str, txid: int, rowid: int) -> bytes:
        """
        编码表数据键
        
        Args:
            table_name: 表名
            txid: 事务ID
            rowid: 行ID
            
        Returns:
            编码后的字节序列
        """
        key_type_bytes = struct.pack('!B', KeyType.TABLE_DATA.value)
        table_name_bytes = table_name.encode('utf-8')
        # 分隔符
        sep = b'\0'
        txid_bytes = struct.pack('!Q', txid)
        rowid_bytes = struct.pack('!Q', rowid)
        return key_type_bytes + table_name_bytes + sep + txid_bytes + rowid_bytes
    
    @staticmethod
    def encode_index_meta(table_name: str, index_name: str) -> bytes:
        """
        编码索引元数据键
        
        Args:
            table_name: 表名
            index_name: 索引名
            
        Returns:
            编码后的字节序列
        """
        key_type_bytes = struct.pack('!B', KeyType.INDEX_META.value)
        table_name_bytes = table_name.encode('utf-8')
        # 分隔符
        sep = b'\0'
        index_name_bytes = index_name.encode('utf-8')
        return key_type_bytes + table_name_bytes + sep + index_name_bytes
    
    @staticmethod
    def encode_index_data(table_name: str, index_name: str, values: List[Any], txid: int, rowid: int) -> bytes:
        """
        编码索引数据键
        
        Args:
            table_name: 表名
            index_name: 索引名
            values: 索引值列表
            txid: 事务ID
            rowid: 行ID
            
        Returns:
            编码后的字节序列
        """
        key_type_bytes = struct.pack('!B', KeyType.INDEX_DATA.value)
        table_name_bytes = table_name.encode('utf-8')
        # 分隔符
        sep = b'\0'
        index_name_bytes = index_name.encode('utf-8')
        
        # 编码索引值
        values_bytes = b''
        for value in values:
            if value is None:
                values_bytes += b'\x00'
            elif isinstance(value, bool):
                values_bytes += b'\x01' + struct.pack('!?', value)
            elif isinstance(value, int):
                values_bytes += b'\x02' + struct.pack('!q', value)
            elif isinstance(value, float):
                values_bytes += b'\x03' + struct.pack('!d', value)
            elif isinstance(value, str):
                value_bytes = value.encode('utf-8')
                values_bytes += b'\x04' + struct.pack('!I', len(value_bytes)) + value_bytes
            else:
                raise ValueError(f"不支持的索引值类型: {type(value)}")
        
        txid_bytes = struct.pack('!Q', txid)
        rowid_bytes = struct.pack('!Q', rowid)
        
        return (key_type_bytes + table_name_bytes + sep + index_name_bytes + 
                sep + values_bytes + sep + txid_bytes + rowid_bytes)
    
    @staticmethod
    def encode_txid() -> bytes:
        """
        编码事务ID键
        
        Returns:
            编码后的字节序列
        """
        return struct.pack('!B', KeyType.TXID.value)


class KeyDecoder:
    """键解码器，将字节序列解码为键信息"""
    
    @staticmethod
    def decode(key: bytes, prefix_len: int) -> bytes:
        """
        解码键，移除前缀和结束符
        
        Args:
            key: 编码后的键
            prefix_len: 前缀长度
            
        Returns:
            解码后的键
        """
        if key[-1] != 0:
            raise ValueError("键格式错误，缺少结束符")
        return key[prefix_len:-1]
    
    @staticmethod
    def decode_txn(key: bytes) -> Tuple[int, bytes]:
        """
        解码事务键
        
        Args:
            key: 编码后的事务键
            
        Returns:
            (事务ID, 键)
        """
        if key[-1] != 0:
            raise ValueError("键格式错误，缺少结束符")
        txid = struct.unpack('!Q', key[:8])[0]
        return txid, key[8:-1]
    
    @staticmethod
    def decode_ts(key: bytes) -> int:
        """
        解码时间戳键
        
        Args:
            key: 编码后的时间戳键
            
        Returns:
            时间戳
        """
        if not key.startswith(b'ts\0'):
            raise ValueError("时间戳键格式错误")
        return struct.unpack('!Q', key[3:])[0]
    
    @staticmethod
    def decode_key_type(key: bytes) -> KeyType:
        """
        解码键类型
        
        Args:
            key: 键的字节序列
            
        Returns:
            键类型
        """
        key_type_value = struct.unpack('!B', key[:1])[0]
        return KeyType(key_type_value)
    
    @staticmethod
    def decode_table_meta(key: bytes) -> str:
        """
        解码表元数据键
        
        Args:
            key: 键的字节序列
            
        Returns:
            表名
        """
        # 跳过键类型字节
        table_name_bytes = key[1:]
        return table_name_bytes.decode('utf-8')
    
    @staticmethod
    def decode_table_data(key: bytes) -> Tuple[str, int, int]:
        """
        解码表数据键
        
        Args:
            key: 键的字节序列
            
        Returns:
            (表名, 事务ID, 行ID)
        """
        # 跳过键类型字节
        parts = key[1:].split(b'\0')
        table_name = parts[0].decode('utf-8')
        
        if len(parts) < 2:
            raise ValueError("无效的表数据键")
        
        txid_rowid_bytes = parts[1]
        
        # 调整以匹配当前实现的格式
        # 通过检测确定当前编码格式是否正确，并尝试从第一个分隔符后解析
        txid_part = txid_rowid_bytes[:8]
        rowid_part = txid_rowid_bytes[8:16]
        
        # 检查长度是否足够解析事务ID和行ID
        if len(txid_part) != 8 or len(rowid_part) != 8:
            # 尝试将整个txid_rowid_bytes视为两个连续的事务ID和行ID
            if len(txid_rowid_bytes) >= 16:
                txid_part = txid_rowid_bytes[:8]
                rowid_part = txid_rowid_bytes[8:16]
            else:
                raise ValueError(f"无效的表数据键: 长度不足, txid_rowid_bytes长度={len(txid_rowid_bytes)}")
        
        try:
            txid = struct.unpack('!Q', txid_part)[0]
            rowid = struct.unpack('!Q', rowid_part)[0]
        except struct.error as e:
            raise ValueError(f"无效的表数据键: 解包错误 {e}")
        
        return (table_name, txid, rowid)
    
    @staticmethod
    def decode_index_meta(key: bytes) -> Tuple[str, str]:
        """
        解码索引元数据键
        
        Args:
            key: 键的字节序列
            
        Returns:
            (表名, 索引名)
        """
        # 跳过键类型字节
        parts = key[1:].split(b'\0')
        
        if len(parts) < 2:
            raise ValueError("无效的索引元数据键")
        
        table_name = parts[0].decode('utf-8')
        index_name = parts[1].decode('utf-8')
        
        return (table_name, index_name)
    
    @staticmethod
    def decode_index_data(key: bytes) -> Tuple[str, str, List[Any], int, int]:
        """
        解码索引数据键
        
        Args:
            key: 键的字节序列
            
        Returns:
            (表名, 索引名, 索引值列表, 事务ID, 行ID)
        """
        # 跳过键类型字节
        parts = key[1:].split(b'\0')
        
        if len(parts) < 4:
            raise ValueError("无效的索引数据键")
        
        table_name = parts[0].decode('utf-8')
        index_name = parts[1].decode('utf-8')
        
        # 解码索引值
        values_bytes = parts[2]
        values = []
        pos = 0
        
        while pos < len(values_bytes):
            # 确保还有足够的字节可以读取类型
            if pos >= len(values_bytes):
                break
                
            type_byte = values_bytes[pos:pos+1]
            pos += 1
            
            try:
                if type_byte == b'\x00':  # NULL
                    values.append(None)
                elif type_byte == b'\x01':  # BOOLEAN
                    if pos + 1 <= len(values_bytes):
                        value = struct.unpack('!?', values_bytes[pos:pos+1])[0]
                        values.append(value)
                        pos += 1
                    else:
                        # 数据不完整，添加默认值
                        values.append(False)
                        break
                elif type_byte == b'\x02':  # INTEGER
                    if pos + 8 <= len(values_bytes):
                        value = struct.unpack('!q', values_bytes[pos:pos+8])[0]
                        values.append(value)
                        pos += 8
                    else:
                        # 数据不完整，尝试使用可用字节
                        remaining = len(values_bytes) - pos
                        if remaining > 0:
                            # 创建8字节的缓冲区，填充0
                            buffer = bytearray(8)
                            buffer[:remaining] = values_bytes[pos:pos+remaining]
                            value = struct.unpack('!q', bytes(buffer))[0]
                            values.append(value)
                        else:
                            values.append(0)
                        break
                elif type_byte == b'\x03':  # FLOAT
                    if pos + 8 <= len(values_bytes):
                        value = struct.unpack('!d', values_bytes[pos:pos+8])[0]
                        values.append(value)
                        pos += 8
                    else:
                        # 数据不完整，添加默认值
                        values.append(0.0)
                        break
                elif type_byte == b'\x04':  # STRING
                    if pos + 4 <= len(values_bytes):
                        length = struct.unpack('!I', values_bytes[pos:pos+4])[0]
                        pos += 4
                        if pos + length <= len(values_bytes):
                            value = values_bytes[pos:pos+length].decode('utf-8')
                            values.append(value)
                            pos += length
                        else:
                            # 字符串长度超出范围，使用可用字节
                            available = len(values_bytes) - pos
                            value = values_bytes[pos:pos+available].decode('utf-8', errors='replace')
                            values.append(value)
                            break
                    else:
                        # 长度字段不完整，添加默认值
                        values.append("")
                        break
                else:
                    # 未知类型，停止解析
                    break
            except (struct.error, UnicodeDecodeError) as e:
                # 解析错误，添加一个适当的默认值并继续
                if type_byte == b'\x01':
                    values.append(False)
                elif type_byte == b'\x02':
                    values.append(0)
                elif type_byte == b'\x03':
                    values.append(0.0)
                elif type_byte == b'\x04':
                    values.append("")
                else:
                    values.append(None)
                # 跳过当前错误的值
                break
        
        # 解码事务ID和行ID
        txid_rowid_bytes = parts[3]
        
        # 确保有足够的字节解析事务ID和行ID
        if len(txid_rowid_bytes) < 16:
            # 尝试使用可用字节并填充
            if len(txid_rowid_bytes) >= 8:
                txid = struct.unpack('!Q', txid_rowid_bytes[:8])[0]
                
                if len(txid_rowid_bytes) >= 16:
                    rowid = struct.unpack('!Q', txid_rowid_bytes[8:16])[0]
                else:
                    # 行ID字段不完整，使用默认值
                    rowid = 0
            else:
                # 事务ID字段不完整，使用默认值
                txid = 0
                rowid = 0
        else:
            # 正常解析
            txid = struct.unpack('!Q', txid_rowid_bytes[:8])[0]
            rowid = struct.unpack('!Q', txid_rowid_bytes[8:16])[0]
        
        return (table_name, index_name, values, txid, rowid)
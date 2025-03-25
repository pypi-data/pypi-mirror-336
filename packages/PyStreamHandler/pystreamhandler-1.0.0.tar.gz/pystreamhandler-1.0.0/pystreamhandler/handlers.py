#!/usr/bin/python3

import struct

class ReadStreamHandler:
    """
    This class is used to read data from a buffer.

    Attributes:
        buffer (bytearray): The buffer to read from.
        cursor (int): The current cursor position in the buffer.

    Methods:
        read_byte: Reads an unsigned byte from the buffer.
        read_short: Reads a signed short (2 bytes) from the buffer.
        read_int: Reads a signed int (4 bytes) from the buffer.
        read_long: Reads a signed long (8 bytes) from the buffer.
        get_length: Returns the length of the buffer.
        get_cursor: Returns the current cursor position.
        set_cursor: Sets the cursor position.
        get_buffer: Returns the underlying buffer.
        reset: Resets the cursor position to 0.
    """

    def __init__(self, buffer) -> None:
        """
        Initializes the ReadStreamHandler with a given buffer.

        :param buffer: The buffer to read from (iterable of ints or bytes).
        """
        # Ensure the buffer is a bytearray
        self.buffer = bytearray(buffer)
        self.cursor = 0


    def read_byte(self) -> int:
        """
        Reads an unsigned byte (1 byte) from the buffer.

        :return: The byte read as an int (0-255).
        :raises ValueError: If reading past the end of the buffer.
        """
        if self.cursor + 1 > len(self.buffer):
            raise ValueError("Buffer overflow")
        # 'B' unpacks an unsigned byte
        value = struct.unpack('B', self.buffer[self.cursor:self.cursor + 1])[0]
        self.cursor += 1
        return value


    def read_short(self) -> int:
        """
        Reads a signed short (2 bytes) from the buffer.

        :return: The short read as an int.
        :raises ValueError: If reading past the end of the buffer.
        """
        if self.cursor + 2 > len(self.buffer):
            raise ValueError("Buffer overflow")
        # '>h' unpacks a big-endian signed short
        value = struct.unpack('>h', self.buffer[self.cursor:self.cursor + 2])[0]
        self.cursor += 2
        return value


    def read_int(self) -> int:
        """
        Reads a signed int (4 bytes) from the buffer.

        :return: The int read from the buffer.
        :raises ValueError: If reading past the end of the buffer.
        """
        if self.cursor + 4 > len(self.buffer):
            raise ValueError("Buffer overflow")
        # '>i' unpacks a big-endian signed int
        value = struct.unpack('>i', self.buffer[self.cursor:self.cursor + 4])[0]
        self.cursor += 4
        return value


    def read_long(self) -> int:
        """
        Reads a signed long (8 bytes) from the buffer.

        :return: The long read from the buffer.
        :raises ValueError: If reading past the end of the buffer.
        """
        if self.cursor + 8 > len(self.buffer):
            raise ValueError("Buffer overflow")
        # '>q' unpacks a big-endian signed long (8 bytes)
        value = struct.unpack('>q', self.buffer[self.cursor:self.cursor + 8])[0]
        self.cursor += 8
        return value


    def read_bytes(self, length: int) -> bytearray:
        """
        Reads a number of bytes from the buffer.

        :param length: The number of bytes to read.
        :return: The bytes read from the buffer.
        :raises ValueError: If reading past the end of the buffer.
        """
        if self.cursor + length > len(self.buffer):
            raise ValueError("Buffer overflow")
        value = self.buffer[self.cursor:self.cursor + length]
        self.cursor += length
        return value


    def get_length(self) -> int:
        """
        Returns the total length of the buffer.

        :return: The length of the buffer.
        """
        return len(self.buffer)


    def get_cursor(self) -> int:
        """
        Returns the current cursor position.

        :return: The cursor position.
        """
        return self.cursor


    def set_cursor(self, index: int) -> None:
        """
        Sets the cursor position.

        :param index: The new cursor position.
        :raises ValueError: If the cursor position is out of bounds.
        """
        if index < 0 or index > len(self.buffer):
            raise ValueError("Invalid cursor position")
        self.cursor = index


    def get_buffer(self) -> bytearray:
        """
        Returns the underlying buffer.

        :return: The buffer as a bytearray.
        """
        return self.buffer


    def reset(self) -> None:
        """
        Resets the cursor position to 0.
        """
        self.cursor = 0


class WriteStreamHandler:
    """
    This class is used to write data to a buffer.

    Attributes:
        buffer (bytearray): The buffer to write to.

    Methods:
        write_byte: Writes a signed byte to the buffer.
        write_unsigned_byte: Writes an unsigned byte to the buffer.
        write_short: Writes a signed short to the buffer.
        write_unsigned_short: Writes an unsigned short to the buffer.
        write_int: Writes a signed int to the buffer.
        write_unsigned_int: Writes an unsigned int to the buffer.
        write_long: Writes a signed long to the buffer.
        write_unsigned_long: Writes an unsigned long to the buffer.
        get_length: Returns the length of the buffer.
        get_buffer: Returns the buffer.
        reset: Resets the buffer.
    """

    def __init__(self) -> None:
        """
        Initializes an empty WriteStreamHandler.
        """
        self.buffer = bytearray()


    def write_byte(self, value: int) -> None:
        """
        Writes a signed byte (1 byte) to the buffer.

        :param value: The signed byte to write (-128 to 127).
        :raises ValueError: If the value is out of range.
        """
        if value < -128 or value > 127:
            raise ValueError("Invalid byte value")
        # 'b' packs a signed byte
        self.buffer.extend(struct.pack('b', value))


    def write_unsigned_byte(self, value: int) -> None:
        """
        Writes an unsigned byte (1 byte) to the buffer.

        :param value: The unsigned byte to write (0 to 255).
        :raises ValueError: If the value is out of range.
        """
        if value < 0 or value > 255:
            raise ValueError("Invalid unsigned byte value")
        # 'B' packs an unsigned byte
        self.buffer.extend(struct.pack('B', value))


    def write_short(self, value: int) -> None:
        """
        Writes a signed short (2 bytes) to the buffer.

        :param value: The short to write (-32768 to 32767).
        :raises ValueError: If the value is out of range.
        """
        if value < -32768 or value > 32767:
            raise ValueError("Invalid short value")
        # '>h' packs a big-endian signed short
        self.buffer.extend(struct.pack('>h', value))


    def write_unsigned_short(self, value: int) -> None:
        """
        Writes an unsigned short (2 bytes) to the buffer.

        :param value: The unsigned short to write (0 to 65535).
        :raises ValueError: If the value is out of range.
        """
        if value < 0 or value > 65535:
            raise ValueError("Invalid unsigned short value")
        # '>H' packs a big-endian unsigned short
        self.buffer.extend(struct.pack('>H', value))


    def write_int(self, value: int) -> None:
        """
        Writes a signed int (4 bytes) to the buffer.

        :param value: The int to write (-2147483648 to 2147483647).
        :raises ValueError: If the value is out of range.
        """
        if value < -2147483648 or value > 2147483647:
            raise ValueError("Invalid int value")
        # '>i' packs a big-endian signed int
        self.buffer.extend(struct.pack('>i', value))


    def write_unsigned_int(self, value: int) -> None:
        """
        Writes an unsigned int (4 bytes) to the buffer.

        :param value: The unsigned int to write (0 to 4294967295).
        :raises ValueError: If the value is out of range.
        """
        if value < 0 or value > 4294967295:
            raise ValueError("Invalid unsigned int value")
        # '>I' packs a big-endian unsigned int
        self.buffer.extend(struct.pack('>I', value))


    def write_long(self, value: int) -> None:
        """
        Writes a signed long (8 bytes) to the buffer.

        :param value: The long to write (-9223372036854775808 to 9223372036854775807).
        :raises ValueError: If the value is out of range.
        """
        if value < -9223372036854775808 or value > 9223372036854775807:
            raise ValueError("Invalid long value")
        # '>q' packs a big-endian signed long
        self.buffer.extend(struct.pack('>q', value))


    def write_unsigned_long(self, value: int) -> None:
        """
        Writes an unsigned long (8 bytes) to the buffer.

        :param value: The unsigned long to write (0 to 18446744073709551615).
        :raises ValueError: If the value is out of range.
        """
        if value < 0 or value > 18446744073709551615:
            raise ValueError("Invalid unsigned long value")
        # '>Q' packs a big-endian unsigned long
        self.buffer.extend(struct.pack('>Q', value))


    def write_bytes(self, value: bytearray) -> None:
        """
        Writes a bytearray to the buffer.

        :param value: The bytearray to write.
        """
        self.buffer.extend(value)


    def get_length(self) -> int:
        """
        Returns the current length of the buffer.

        :return: The length of the buffer.
        """
        return len(self.buffer)


    def get_buffer(self) -> bytearray:
        """
        Returns the underlying buffer.

        :return: The buffer as a bytearray.
        """
        return self.buffer


    def reset(self) -> None:
        """
        Resets the buffer to an empty state.
        """
        self.buffer = bytearray()

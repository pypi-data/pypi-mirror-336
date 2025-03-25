import unittest
import struct

from StreamHandler import ReadStreamHandler, WriteStreamHandler


class TestWriteStreamHandler(unittest.TestCase):
    def setUp(self):
        self.writer = WriteStreamHandler()


    def test_write_byte_valid(self):
        # Valid signed byte range: -128 to 127
        self.writer.write_byte(-128)
        self.writer.write_byte(0)
        self.writer.write_byte(127)
        buffer = self.writer.get_buffer()
        self.assertEqual(len(buffer), 3)
        self.assertEqual(struct.unpack('b', buffer[0:1])[0], -128)
        self.assertEqual(struct.unpack('b', buffer[1:2])[0], 0)
        self.assertEqual(struct.unpack('b', buffer[2:3])[0], 127)


    def test_write_byte_invalid(self):
        with self.assertRaises(ValueError):
            self.writer.write_byte(-129)
        with self.assertRaises(ValueError):
            self.writer.write_byte(128)


    def test_write_unsigned_byte_valid(self):
        self.writer.write_unsigned_byte(0)
        self.writer.write_unsigned_byte(255)
        buffer = self.writer.get_buffer()
        self.assertEqual(len(buffer), 2)
        self.assertEqual(struct.unpack('B', buffer[0:1])[0], 0)
        self.assertEqual(struct.unpack('B', buffer[1:2])[0], 255)


    def test_write_unsigned_byte_invalid(self):
        with self.assertRaises(ValueError):
            self.writer.write_unsigned_byte(-1)
        with self.assertRaises(ValueError):
            self.writer.write_unsigned_byte(256)


    def test_write_short_valid(self):
        # Valid signed short range: -32768 to 32767
        self.writer.write_short(-32768)
        self.writer.write_short(0)
        self.writer.write_short(32767)
        buffer = self.writer.get_buffer()
        self.assertEqual(len(buffer), 6)
        self.assertEqual(struct.unpack('>h', buffer[0:2])[0], -32768)
        self.assertEqual(struct.unpack('>h', buffer[2:4])[0], 0)
        self.assertEqual(struct.unpack('>h', buffer[4:6])[0], 32767)


    def test_write_short_invalid(self):
        with self.assertRaises(ValueError):
            self.writer.write_short(-32769)
        with self.assertRaises(ValueError):
            self.writer.write_short(32768)


    def test_write_unsigned_short_valid(self):
        self.writer.write_unsigned_short(0)
        self.writer.write_unsigned_short(65535)
        buffer = self.writer.get_buffer()
        self.assertEqual(len(buffer), 4)
        self.assertEqual(struct.unpack('>H', buffer[0:2])[0], 0)
        self.assertEqual(struct.unpack('>H', buffer[2:4])[0], 65535)


    def test_write_unsigned_short_invalid(self):
        with self.assertRaises(ValueError):
            self.writer.write_unsigned_short(-1)
        with self.assertRaises(ValueError):
            self.writer.write_unsigned_short(65536)


    def test_write_int_valid(self):
        # Valid signed int range: -2147483648 to 2147483647
        self.writer.write_int(-2147483648)
        self.writer.write_int(0)
        self.writer.write_int(2147483647)
        buffer = self.writer.get_buffer()
        self.assertEqual(len(buffer), 12)
        self.assertEqual(struct.unpack('>i', buffer[0:4])[0], -2147483648)
        self.assertEqual(struct.unpack('>i', buffer[4:8])[0], 0)
        self.assertEqual(struct.unpack('>i', buffer[8:12])[0], 2147483647)


    def test_write_int_invalid(self):
        with self.assertRaises(ValueError):
            self.writer.write_int(-2147483649)
        with self.assertRaises(ValueError):
            self.writer.write_int(2147483648)


    def test_write_unsigned_int_valid(self):
        self.writer.write_unsigned_int(0)
        self.writer.write_unsigned_int(4294967295)
        buffer = self.writer.get_buffer()
        self.assertEqual(len(buffer), 8)
        self.assertEqual(struct.unpack('>I', buffer[0:4])[0], 0)
        self.assertEqual(struct.unpack('>I', buffer[4:8])[0], 4294967295)


    def test_write_unsigned_int_invalid(self):
        with self.assertRaises(ValueError):
            self.writer.write_unsigned_int(-1)
        with self.assertRaises(ValueError):
            self.writer.write_unsigned_int(4294967296)


    def test_write_long_valid(self):
        # Valid signed long range: -9223372036854775808 to 9223372036854775807
        self.writer.write_long(-9223372036854775808)
        self.writer.write_long(0)
        self.writer.write_long(9223372036854775807)
        buffer = self.writer.get_buffer()
        self.assertEqual(len(buffer), 24)
        self.assertEqual(struct.unpack('>q', buffer[0:8])[0], -9223372036854775808)
        self.assertEqual(struct.unpack('>q', buffer[8:16])[0], 0)
        self.assertEqual(struct.unpack('>q', buffer[16:24])[0], 9223372036854775807)


    def test_write_long_invalid(self):
        with self.assertRaises(ValueError):
            self.writer.write_long(-9223372036854775809)
        with self.assertRaises(ValueError):
            self.writer.write_long(9223372036854775808)


    def test_write_unsigned_long_valid(self):
        self.writer.write_unsigned_long(0)
        self.writer.write_unsigned_long(18446744073709551615)
        buffer = self.writer.get_buffer()
        self.assertEqual(len(buffer), 16)
        self.assertEqual(struct.unpack('>Q', buffer[0:8])[0], 0)
        self.assertEqual(struct.unpack('>Q', buffer[8:16])[0], 18446744073709551615)


    def test_write_unsigned_long_invalid(self):
        with self.assertRaises(ValueError):
            self.writer.write_unsigned_long(-1)
        with self.assertRaises(ValueError):
            self.writer.write_unsigned_long(18446744073709551616)


    def test_reset(self):
        self.writer.write_int(12345)
        self.assertNotEqual(len(self.writer.get_buffer()), 0)
        self.writer.reset()
        self.assertEqual(len(self.writer.get_buffer()), 0)


class TestReadStreamHandler(unittest.TestCase):
    def setUp(self):
        # Use WriteStreamHandler to create a known binary buffer.
        self.writer = WriteStreamHandler()
        self.writer.write_byte(100)                     # signed byte (read as unsigned 100)
        self.writer.write_short(12345)                  # signed short
        self.writer.write_int(123456789)                # signed int
        self.writer.write_long(1234567890123456789)       # signed long
        self.buffer = self.writer.get_buffer()
        self.reader = ReadStreamHandler(self.buffer)


    def test_get_length(self):
        self.assertEqual(self.reader.get_length(), len(self.buffer))


    def test_read_byte(self):
        value = self.reader.read_byte()
        self.assertEqual(value, 100)


    def test_read_short(self):
        # Reset and skip the first byte (1 byte) to read the short next.
        self.reader.reset()
        self.reader.read_byte()  # skip the byte
        value = self.reader.read_short()
        self.assertEqual(value, 12345)


    def test_read_int(self):
        # Skip byte (1) + short (2) = 3 bytes, then read the int.
        self.reader.reset()
        self.reader.read_byte()
        self.reader.read_short()
        value = self.reader.read_int()
        self.assertEqual(value, 123456789)


    def test_read_long(self):
        # Skip byte (1) + short (2) + int (4) = 7 bytes, then read the long.
        self.reader.reset()
        self.reader.read_byte()
        self.reader.read_short()
        self.reader.read_int()
        value = self.reader.read_long()
        self.assertEqual(value, 1234567890123456789)


    def test_reset_cursor(self):
        self.reader.read_byte()
        self.reader.read_short()
        self.reader.reset()
        self.assertEqual(self.reader.get_cursor(), 0)


    def test_set_cursor_invalid(self):
        with self.assertRaises(ValueError):
            self.reader.set_cursor(-1)
        with self.assertRaises(ValueError):
            self.reader.set_cursor(len(self.buffer) + 1)


    def test_buffer_overflow_read_byte(self):
        # Create a reader with an empty buffer.
        reader = ReadStreamHandler(bytearray())
        with self.assertRaises(ValueError):
            reader.read_byte()


    def test_buffer_overflow_read_short(self):
        # Create a reader with only 1 byte.
        reader = ReadStreamHandler(bytearray([0]))
        with self.assertRaises(ValueError):
            reader.read_short()


    def test_buffer_overflow_read_int(self):
        # Create a reader with only 3 bytes.
        reader = ReadStreamHandler(bytearray([0, 0, 0]))
        with self.assertRaises(ValueError):
            reader.read_int()


    def test_buffer_overflow_read_long(self):
        # Create a reader with only 7 bytes.
        reader = ReadStreamHandler(bytearray([0] * 7))
        with self.assertRaises(ValueError):
            reader.read_long()


if __name__ == '__main__':
    unittest.main()

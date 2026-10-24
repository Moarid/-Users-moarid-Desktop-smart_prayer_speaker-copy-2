# sdcard.py
# MicroPython SD card driver

from micropython import const
import time

_CMD_TIMEOUT = const(100)

_R1_IDLE_STATE = const(1 << 0)
_R1_ILLEGAL_COMMAND = const(1 << 2)
_TOKEN_CMD25 = const(0xFC)
_TOKEN_STOP_TRAN = const(0xFD)
_TOKEN_DATA = const(0xFE)


class SDCard:
    def __init__(self, spi, cs, baudrate=1320000):
        self.spi = spi
        self.cs = cs

        self.cmdbuf = bytearray(6)
        self.dummybuf = bytearray(512)
        self.tokenbuf = bytearray(1)
        self.singlebuf = bytearray(1)

        for i in range(512):
            self.dummybuf[i] = 0xFF

        self.cs.init(self.cs.OUT, value=1)
        self.init_card(baudrate)

    def init_spi(self, baudrate):
        try:
            self.spi.init(baudrate=baudrate, phase=0, polarity=0)
        except TypeError:
            self.spi.init(baudrate=baudrate)

    def init_card(self, baudrate):
        self.init_spi(100000)

        for _ in range(16):
            self.spi.write(b"\xff")

        for _ in range(5):
            if self.cmd(0, 0, 0x95) == _R1_IDLE_STATE:
                break
        else:
            raise OSError("no SD card")

        r = self.cmd(8, 0x01AA, 0x87)
        if r == _R1_IDLE_STATE:
            self.init_card_v2()
        elif r == (_R1_IDLE_STATE | _R1_ILLEGAL_COMMAND):
            self.init_card_v1()
        else:
            raise OSError("couldn't determine SD card version")

        if self.cmd(9, 0, 0) != 0:
            raise OSError("no response from SD card")

        csd = bytearray(16)
        self.readinto(csd)

        if csd[0] & 0xC0 == 0x40:
            c_size = ((csd[7] & 0x3F) << 16) | (csd[8] << 8) | csd[9]
            self.sectors = (c_size + 1) * 1024
        else:
            c_size = ((csd[6] & 0x03) << 10) | (csd[7] << 2) | ((csd[8] & 0xC0) >> 6)
            c_size_mult = ((csd[9] & 0x03) << 1) | ((csd[10] & 0x80) >> 7)
            read_bl_len = csd[5] & 0x0F
            capacity = (c_size + 1) * (2 ** (c_size_mult + 2)) * (2 ** read_bl_len)
            self.sectors = capacity // 512

        self.cmd(16, 512, 0)
        self.init_spi(baudrate)

    def init_card_v1(self):
        for _ in range(_CMD_TIMEOUT):
            self.cmd(55, 0, 0)
            if self.cmd(41, 0, 0) == 0:
                self.cdv = 512
                return
        raise OSError("timeout waiting for v1 card")

    def init_card_v2(self):
        for _ in range(4):
            self.spi.readinto(self.tokenbuf, 0xFF)

        for _ in range(_CMD_TIMEOUT):
            time.sleep_ms(50)
            self.cmd(58, 0, 0)
            self.cmd(55, 0, 0)
            if self.cmd(41, 0x40000000, 0) == 0:
                self.cmd(58, 0, 0)
                self.cdv = 1
                return
        raise OSError("timeout waiting for v2 card")

    def cmd(self, cmd, arg, crc, final=0):
        self.cs(0)

        buf = self.cmdbuf
        buf[0] = 0x40 | cmd
        buf[1] = arg >> 24
        buf[2] = arg >> 16
        buf[3] = arg >> 8
        buf[4] = arg
        buf[5] = crc

        self.spi.write(buf)

        if final:
            self.spi.write(b"\xff")

        for _ in range(_CMD_TIMEOUT):
            self.spi.readinto(self.tokenbuf, 0xFF)
            response = self.tokenbuf[0]
            if not (response & 0x80):
                self.cs(1)
                self.spi.write(b"\xff")
                return response

        self.cs(1)
        self.spi.write(b"\xff")
        return -1

    def readinto(self, buf):
        self.cs(0)

        for _ in range(_CMD_TIMEOUT):
            self.spi.readinto(self.tokenbuf, 0xFF)
            if self.tokenbuf[0] == _TOKEN_DATA:
                break
            time.sleep_ms(1)
        else:
            self.cs(1)
            raise OSError("timeout waiting for response")

        mv = memoryview(buf)
        self.spi.readinto(mv, 0xFF)
        self.spi.write(b"\xff")
        self.spi.write(b"\xff")

        self.cs(1)
        self.spi.write(b"\xff")

    def write(self, token, buf):
        self.cs(0)
        self.spi.read(1, 0xFF)
        self.spi.write(bytearray([token]))
        self.spi.write(buf)
        self.spi.write(b"\xff")
        self.spi.write(b"\xff")

        if (self.spi.read(1, 0xFF)[0] & 0x1F) != 0x05:
            self.cs(1)
            raise OSError("write failed")

        while self.spi.read(1, 0xFF)[0] == 0:
            pass

        self.cs(1)
        self.spi.write(b"\xff")

    def readblocks(self, block_num, buf):
        nblocks = len(buf) // 512
        assert nblocks and not len(buf) % 512

        if nblocks == 1:
            if self.cmd(17, block_num * self.cdv, 0) != 0:
                raise OSError("readblocks command failed")
            self.readinto(buf)
        else:
            if self.cmd(18, block_num * self.cdv, 0) != 0:
                raise OSError("readblocks command failed")
            offset = 0
            mv = memoryview(buf)
            while nblocks:
                self.readinto(mv[offset:offset + 512])
                offset += 512
                nblocks -= 1
            self.cmd(12, 0, 0xFF, final=1)

    def writeblocks(self, block_num, buf):
        nblocks = len(buf) // 512
        assert nblocks and not len(buf) % 512

        if nblocks == 1:
            if self.cmd(24, block_num * self.cdv, 0) != 0:
                raise OSError("writeblocks command failed")
            self.write(_TOKEN_DATA, buf)
        else:
            if self.cmd(25, block_num * self.cdv, 0) != 0:
                raise OSError("writeblocks command failed")
            offset = 0
            mv = memoryview(buf)
            while nblocks:
                self.write(_TOKEN_CMD25, mv[offset:offset + 512])
                offset += 512
                nblocks -= 1
            self.write(_TOKEN_STOP_TRAN, b"")

    def ioctl(self, op, arg):
        if op == 4:
            return self.sectors
        if op == 5:
            return 512
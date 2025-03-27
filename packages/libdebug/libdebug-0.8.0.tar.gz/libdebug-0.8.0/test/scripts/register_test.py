#
# This file is part of libdebug Python library (https://github.com/libdebug/libdebug).
# Copyright (c) 2023-2025 Gabriele Digregorio, Roberto Alessandro Bertolini, Francesco Panebianco. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

import sys
from io import StringIO
from unittest import TestCase, skipUnless
from utils.binary_utils import PLATFORM, RESOLVE_EXE

from libdebug import debugger

match PLATFORM:
    case "amd64":
        REGISTER_ACCESS = "rip"
    case "aarch64":
        REGISTER_ACCESS = "pc"
    case "i386":
        REGISTER_ACCESS = "eip"
    case _:
        raise NotImplementedError(f"Platform {PLATFORM} not supported by this test")

class RegisterTest(TestCase):
    @skipUnless(PLATFORM == "amd64", "Requires amd64")
    def test_registers_amd64(self):
        d = debugger(RESOLVE_EXE("basic_test"))

        d.run()

        bp1 = d.breakpoint(0x4011CA)
        bp2 = d.breakpoint(0x40128D)
        bp3 = d.breakpoint(0x401239)
        bp4 = d.breakpoint(0x4011F4)
        bp5 = d.breakpoint(0x401296)

        d.cont()
        self.assertTrue(bp1.address, d.regs.rip)

        self.assertTrue(d.regs.rax, 0x0011223344556677)
        self.assertTrue(d.regs.rbx, 0x1122334455667700)
        self.assertTrue(d.regs.rcx, 0x2233445566770011)
        self.assertTrue(d.regs.rdx, 0x3344556677001122)
        self.assertTrue(d.regs.rsi, 0x4455667700112233)
        self.assertTrue(d.regs.rdi, 0x5566770011223344)
        self.assertTrue(d.regs.rbp, 0x6677001122334455)
        self.assertTrue(d.regs.r8, 0xAABBCCDD11223344)
        self.assertTrue(d.regs.r9, 0xBBCCDD11223344AA)
        self.assertTrue(d.regs.r10, 0xCCDD11223344AABB)
        self.assertTrue(d.regs.r11, 0xDD11223344AABBCC)
        self.assertTrue(d.regs.r12, 0x11223344AABBCCDD)
        self.assertTrue(d.regs.r13, 0x223344AABBCCDD11)
        self.assertTrue(d.regs.r14, 0x3344AABBCCDD1122)
        self.assertTrue(d.regs.r15, 0x44AABBCCDD112233)

        d.cont()
        self.assertTrue(bp4.address, d.regs.rip)

        self.assertTrue(d.regs.al, 0x11)
        self.assertTrue(d.regs.bl, 0x22)
        self.assertTrue(d.regs.cl, 0x33)
        self.assertTrue(d.regs.dl, 0x44)
        self.assertTrue(d.regs.sil, 0x55)
        self.assertTrue(d.regs.dil, 0x66)
        self.assertTrue(d.regs.bpl, 0x77)
        self.assertTrue(d.regs.r8b, 0x88)
        self.assertTrue(d.regs.r9b, 0x99)
        self.assertTrue(d.regs.r10b, 0xAA)
        self.assertTrue(d.regs.r11b, 0xBB)
        self.assertTrue(d.regs.r12b, 0xCC)
        self.assertTrue(d.regs.r13b, 0xDD)
        self.assertTrue(d.regs.r14b, 0xEE)
        self.assertTrue(d.regs.r15b, 0xFF)

        d.cont()
        self.assertTrue(bp3.address, d.regs.rip)

        self.assertTrue(d.regs.ax, 0x1122)
        self.assertTrue(d.regs.bx, 0x2233)
        self.assertTrue(d.regs.cx, 0x3344)
        self.assertTrue(d.regs.dx, 0x4455)
        self.assertTrue(d.regs.si, 0x5566)
        self.assertTrue(d.regs.di, 0x6677)
        self.assertTrue(d.regs.bp, 0x7788)
        self.assertTrue(d.regs.r8w, 0x8899)
        self.assertTrue(d.regs.r9w, 0x99AA)
        self.assertTrue(d.regs.r10w, 0xAABB)
        self.assertTrue(d.regs.r11w, 0xBBCC)
        self.assertTrue(d.regs.r12w, 0xCCDD)
        self.assertTrue(d.regs.r13w, 0xDDEE)
        self.assertTrue(d.regs.r14w, 0xEEFF)
        self.assertTrue(d.regs.r15w, 0xFF00)

        d.cont()
        self.assertTrue(bp2.address, d.regs.rip)

        self.assertTrue(d.regs.eax, 0x11223344)
        self.assertTrue(d.regs.ebx, 0x22334455)
        self.assertTrue(d.regs.ecx, 0x33445566)
        self.assertTrue(d.regs.edx, 0x44556677)
        self.assertTrue(d.regs.esi, 0x55667788)
        self.assertTrue(d.regs.edi, 0x66778899)
        self.assertTrue(d.regs.ebp, 0x778899AA)
        self.assertTrue(d.regs.r8d, 0x8899AABB)
        self.assertTrue(d.regs.r9d, 0x99AABBCC)
        self.assertTrue(d.regs.r10d, 0xAABBCCDD)
        self.assertTrue(d.regs.r11d, 0xBBCCDD11)
        self.assertTrue(d.regs.r12d, 0xCCDD1122)
        self.assertTrue(d.regs.r13d, 0xDD112233)
        self.assertTrue(d.regs.r14d, 0x11223344)
        self.assertTrue(d.regs.r15d, 0x22334455)

        d.cont()
        self.assertTrue(bp5.address, d.regs.rip)

        self.assertTrue(d.regs.ah, 0x11)
        self.assertTrue(d.regs.bh, 0x22)
        self.assertTrue(d.regs.ch, 0x33)
        self.assertTrue(d.regs.dh, 0x44)

        d.cont()
        d.kill()
        d.terminate()

    @skipUnless(PLATFORM == "amd64", "Requires amd64")
    def test_registers_hardware_amd64(self):
        d = debugger(RESOLVE_EXE("basic_test"))

        d.run()

        bp1 = d.breakpoint(0x4011CA, hardware=True)
        bp2 = d.breakpoint(0x40128D, hardware=False)
        bp3 = d.breakpoint(0x401239, hardware=True)
        bp4 = d.breakpoint(0x4011F4, hardware=False)
        bp5 = d.breakpoint(0x401296, hardware=True)

        d.cont()
        self.assertTrue(bp1.address, d.regs.rip)

        self.assertTrue(d.regs.rax, 0x0011223344556677)
        self.assertTrue(d.regs.rbx, 0x1122334455667700)
        self.assertTrue(d.regs.rcx, 0x2233445566770011)
        self.assertTrue(d.regs.rdx, 0x3344556677001122)
        self.assertTrue(d.regs.rsi, 0x4455667700112233)
        self.assertTrue(d.regs.rdi, 0x5566770011223344)
        self.assertTrue(d.regs.rbp, 0x6677001122334455)
        self.assertTrue(d.regs.r8, 0xAABBCCDD11223344)
        self.assertTrue(d.regs.r9, 0xBBCCDD11223344AA)
        self.assertTrue(d.regs.r10, 0xCCDD11223344AABB)
        self.assertTrue(d.regs.r11, 0xDD11223344AABBCC)
        self.assertTrue(d.regs.r12, 0x11223344AABBCCDD)
        self.assertTrue(d.regs.r13, 0x223344AABBCCDD11)
        self.assertTrue(d.regs.r14, 0x3344AABBCCDD1122)
        self.assertTrue(d.regs.r15, 0x44AABBCCDD112233)

        d.cont()
        self.assertTrue(bp4.address, d.regs.rip)

        self.assertTrue(d.regs.al, 0x11)
        self.assertTrue(d.regs.bl, 0x22)
        self.assertTrue(d.regs.cl, 0x33)
        self.assertTrue(d.regs.dl, 0x44)
        self.assertTrue(d.regs.sil, 0x55)
        self.assertTrue(d.regs.dil, 0x66)
        self.assertTrue(d.regs.bpl, 0x77)
        self.assertTrue(d.regs.r8b, 0x88)
        self.assertTrue(d.regs.r9b, 0x99)
        self.assertTrue(d.regs.r10b, 0xAA)
        self.assertTrue(d.regs.r11b, 0xBB)
        self.assertTrue(d.regs.r12b, 0xCC)
        self.assertTrue(d.regs.r13b, 0xDD)
        self.assertTrue(d.regs.r14b, 0xEE)
        self.assertTrue(d.regs.r15b, 0xFF)

        d.cont()
        self.assertTrue(bp3.address, d.regs.rip)

        self.assertTrue(d.regs.ax, 0x1122)
        self.assertTrue(d.regs.bx, 0x2233)
        self.assertTrue(d.regs.cx, 0x3344)
        self.assertTrue(d.regs.dx, 0x4455)
        self.assertTrue(d.regs.si, 0x5566)
        self.assertTrue(d.regs.di, 0x6677)
        self.assertTrue(d.regs.bp, 0x7788)
        self.assertTrue(d.regs.r8w, 0x8899)
        self.assertTrue(d.regs.r9w, 0x99AA)
        self.assertTrue(d.regs.r10w, 0xAABB)
        self.assertTrue(d.regs.r11w, 0xBBCC)
        self.assertTrue(d.regs.r12w, 0xCCDD)
        self.assertTrue(d.regs.r13w, 0xDDEE)
        self.assertTrue(d.regs.r14w, 0xEEFF)
        self.assertTrue(d.regs.r15w, 0xFF00)

        d.cont()
        self.assertTrue(bp2.address, d.regs.rip)

        self.assertTrue(d.regs.eax, 0x11223344)
        self.assertTrue(d.regs.ebx, 0x22334455)
        self.assertTrue(d.regs.ecx, 0x33445566)
        self.assertTrue(d.regs.edx, 0x44556677)
        self.assertTrue(d.regs.esi, 0x55667788)
        self.assertTrue(d.regs.edi, 0x66778899)
        self.assertTrue(d.regs.ebp, 0x778899AA)
        self.assertTrue(d.regs.r8d, 0x8899AABB)
        self.assertTrue(d.regs.r9d, 0x99AABBCC)
        self.assertTrue(d.regs.r10d, 0xAABBCCDD)
        self.assertTrue(d.regs.r11d, 0xBBCCDD11)
        self.assertTrue(d.regs.r12d, 0xCCDD1122)
        self.assertTrue(d.regs.r13d, 0xDD112233)
        self.assertTrue(d.regs.r14d, 0x11223344)
        self.assertTrue(d.regs.r15d, 0x22334455)

        d.cont()
        self.assertTrue(bp5.address, d.regs.rip)

        self.assertTrue(d.regs.ah, 0x11)
        self.assertTrue(d.regs.bh, 0x22)
        self.assertTrue(d.regs.ch, 0x33)
        self.assertTrue(d.regs.dh, 0x44)

        d.cont()
        d.kill()
        d.terminate()

    @skipUnless(PLATFORM == "aarch64", "Requires aarch64")
    def test_registers_aarch64(self):
        d = debugger(RESOLVE_EXE("basic_test"))
        d.run()

        bp = d.breakpoint(0x4008a4, hardware=False)

        d.cont()

        self.assertEqual(d.regs.pc, bp.address)

        self.assertEqual(d.regs.x0, 0x4444333322221111)
        self.assertEqual(d.regs.x1, 0x8888777766665555)
        self.assertEqual(d.regs.x2, 0xccccbbbbaaaa9999)
        self.assertEqual(d.regs.x3, 0x1111ffffeeeedddd)
        self.assertEqual(d.regs.x4, 0x5555444433332222)
        self.assertEqual(d.regs.x5, 0x9999888877776666)
        self.assertEqual(d.regs.x6, 0xddddccccbbbbaaaa)
        self.assertEqual(d.regs.x7, 0x22221111ffffeeee)
        self.assertEqual(d.regs.x8, 0x6666555544443333)
        self.assertEqual(d.regs.x9, 0xaaaa999988887777)
        self.assertEqual(d.regs.x10, 0xeeeeddddccccbbbb)
        self.assertEqual(d.regs.x11, 0x333322221111ffff)
        self.assertEqual(d.regs.x12, 0x7777666655554444)
        self.assertEqual(d.regs.x13, 0xbbbbaaaa99998888)
        self.assertEqual(d.regs.x14, 0xffffeeeeddddcccc)
        self.assertEqual(d.regs.x15, 0x4444333322221111)
        self.assertEqual(d.regs.x16, 0x8888777766665555)
        self.assertEqual(d.regs.x17, 0xccccbbbbaaaa9999)
        self.assertEqual(d.regs.x18, 0x1111ffffeeeedddd)
        self.assertEqual(d.regs.x19, 0x5555444433332222)
        self.assertEqual(d.regs.x20, 0x9999888877776666)
        self.assertEqual(d.regs.x21, 0xddddccccbbbbaaaa)
        self.assertEqual(d.regs.x22, 0x22221111ffffeeee)
        self.assertEqual(d.regs.x23, 0x6666555544443333)
        self.assertEqual(d.regs.x24, 0xaaaa999988887777)
        self.assertEqual(d.regs.x25, 0xeeeeddddccccbbbb)
        self.assertEqual(d.regs.x26, 0x333322221111ffff)
        self.assertEqual(d.regs.x27, 0x7777666655554444)
        self.assertEqual(d.regs.x28, 0xbbbbaaaa99998888)
        self.assertEqual(d.regs.x29, 0xffffeeeeddddcccc)
        self.assertEqual(d.regs.x30, 0x4444333322221111)

        self.assertEqual(d.regs.lr, 0x4444333322221111)
        self.assertEqual(d.regs.fp, 0xffffeeeeddddcccc)
        self.assertEqual(d.regs.xzr, 0)
        self.assertEqual(d.regs.wzr, 0)

        d.regs.xzr = 0x123456789abcdef0
        d.regs.wzr = 0x12345678

        self.assertEqual(d.regs.xzr, 0)
        self.assertEqual(d.regs.wzr, 0)

        self.assertEqual(d.regs.w0, 0x22221111)
        self.assertEqual(d.regs.w1, 0x66665555)
        self.assertEqual(d.regs.w2, 0xaaaa9999)
        self.assertEqual(d.regs.w3, 0xeeeedddd)
        self.assertEqual(d.regs.w4, 0x33332222)
        self.assertEqual(d.regs.w5, 0x77776666)
        self.assertEqual(d.regs.w6, 0xbbbbaaaa)
        self.assertEqual(d.regs.w7, 0xffffeeee)
        self.assertEqual(d.regs.w8, 0x44443333)
        self.assertEqual(d.regs.w9, 0x88887777)
        self.assertEqual(d.regs.w10, 0xccccbbbb)
        self.assertEqual(d.regs.w11, 0x1111ffff)
        self.assertEqual(d.regs.w12, 0x55554444)
        self.assertEqual(d.regs.w13, 0x99998888)
        self.assertEqual(d.regs.w14, 0xddddcccc)
        self.assertEqual(d.regs.w15, 0x22221111)
        self.assertEqual(d.regs.w16, 0x66665555)
        self.assertEqual(d.regs.w17, 0xaaaa9999)
        self.assertEqual(d.regs.w18, 0xeeeedddd)
        self.assertEqual(d.regs.w19, 0x33332222)
        self.assertEqual(d.regs.w20, 0x77776666)
        self.assertEqual(d.regs.w21, 0xbbbbaaaa)
        self.assertEqual(d.regs.w22, 0xffffeeee)
        self.assertEqual(d.regs.w23, 0x44443333)
        self.assertEqual(d.regs.w24, 0x88887777)
        self.assertEqual(d.regs.w25, 0xccccbbbb)
        self.assertEqual(d.regs.w26, 0x1111ffff)
        self.assertEqual(d.regs.w27, 0x55554444)
        self.assertEqual(d.regs.w28, 0x99998888)
        self.assertEqual(d.regs.w29, 0xddddcccc)
        self.assertEqual(d.regs.w30, 0x22221111)

        d.cont()

        d.kill()
        d.terminate()

    @skipUnless(PLATFORM == "aarch64", "Requires aarch64")
    def test_registers_hardware_aarch64(self):
        d = debugger(RESOLVE_EXE("basic_test"))
        d.run()

        bp = d.breakpoint(0x4008a4, hardware=True)

        d.cont()

        self.assertEqual(d.regs.pc, bp.address)

        self.assertEqual(d.regs.x0, 0x4444333322221111)
        self.assertEqual(d.regs.x1, 0x8888777766665555)
        self.assertEqual(d.regs.x2, 0xccccbbbbaaaa9999)
        self.assertEqual(d.regs.x3, 0x1111ffffeeeedddd)
        self.assertEqual(d.regs.x4, 0x5555444433332222)
        self.assertEqual(d.regs.x5, 0x9999888877776666)
        self.assertEqual(d.regs.x6, 0xddddccccbbbbaaaa)
        self.assertEqual(d.regs.x7, 0x22221111ffffeeee)
        self.assertEqual(d.regs.x8, 0x6666555544443333)
        self.assertEqual(d.regs.x9, 0xaaaa999988887777)
        self.assertEqual(d.regs.x10, 0xeeeeddddccccbbbb)
        self.assertEqual(d.regs.x11, 0x333322221111ffff)
        self.assertEqual(d.regs.x12, 0x7777666655554444)
        self.assertEqual(d.regs.x13, 0xbbbbaaaa99998888)
        self.assertEqual(d.regs.x14, 0xffffeeeeddddcccc)
        self.assertEqual(d.regs.x15, 0x4444333322221111)
        self.assertEqual(d.regs.x16, 0x8888777766665555)
        self.assertEqual(d.regs.x17, 0xccccbbbbaaaa9999)
        self.assertEqual(d.regs.x18, 0x1111ffffeeeedddd)
        self.assertEqual(d.regs.x19, 0x5555444433332222)
        self.assertEqual(d.regs.x20, 0x9999888877776666)
        self.assertEqual(d.regs.x21, 0xddddccccbbbbaaaa)
        self.assertEqual(d.regs.x22, 0x22221111ffffeeee)
        self.assertEqual(d.regs.x23, 0x6666555544443333)
        self.assertEqual(d.regs.x24, 0xaaaa999988887777)
        self.assertEqual(d.regs.x25, 0xeeeeddddccccbbbb)
        self.assertEqual(d.regs.x26, 0x333322221111ffff)
        self.assertEqual(d.regs.x27, 0x7777666655554444)
        self.assertEqual(d.regs.x28, 0xbbbbaaaa99998888)
        self.assertEqual(d.regs.x29, 0xffffeeeeddddcccc)
        self.assertEqual(d.regs.x30, 0x4444333322221111)

        self.assertEqual(d.regs.lr, 0x4444333322221111)
        self.assertEqual(d.regs.fp, 0xffffeeeeddddcccc)
        self.assertEqual(d.regs.xzr, 0)
        self.assertEqual(d.regs.wzr, 0)

        d.regs.xzr = 0x123456789abcdef0
        d.regs.wzr = 0x12345678

        self.assertEqual(d.regs.xzr, 0)
        self.assertEqual(d.regs.wzr, 0)

        self.assertEqual(d.regs.w0, 0x22221111)
        self.assertEqual(d.regs.w1, 0x66665555)
        self.assertEqual(d.regs.w2, 0xaaaa9999)
        self.assertEqual(d.regs.w3, 0xeeeedddd)
        self.assertEqual(d.regs.w4, 0x33332222)
        self.assertEqual(d.regs.w5, 0x77776666)
        self.assertEqual(d.regs.w6, 0xbbbbaaaa)
        self.assertEqual(d.regs.w7, 0xffffeeee)
        self.assertEqual(d.regs.w8, 0x44443333)
        self.assertEqual(d.regs.w9, 0x88887777)
        self.assertEqual(d.regs.w10, 0xccccbbbb)
        self.assertEqual(d.regs.w11, 0x1111ffff)
        self.assertEqual(d.regs.w12, 0x55554444)
        self.assertEqual(d.regs.w13, 0x99998888)
        self.assertEqual(d.regs.w14, 0xddddcccc)
        self.assertEqual(d.regs.w15, 0x22221111)
        self.assertEqual(d.regs.w16, 0x66665555)
        self.assertEqual(d.regs.w17, 0xaaaa9999)
        self.assertEqual(d.regs.w18, 0xeeeedddd)
        self.assertEqual(d.regs.w19, 0x33332222)
        self.assertEqual(d.regs.w20, 0x77776666)
        self.assertEqual(d.regs.w21, 0xbbbbaaaa)
        self.assertEqual(d.regs.w22, 0xffffeeee)
        self.assertEqual(d.regs.w23, 0x44443333)
        self.assertEqual(d.regs.w24, 0x88887777)
        self.assertEqual(d.regs.w25, 0xccccbbbb)
        self.assertEqual(d.regs.w26, 0x1111ffff)
        self.assertEqual(d.regs.w27, 0x55554444)
        self.assertEqual(d.regs.w28, 0x99998888)
        self.assertEqual(d.regs.w29, 0xddddcccc)
        self.assertEqual(d.regs.w30, 0x22221111)

        d.cont()

        d.kill()
        d.terminate()

    @skipUnless(PLATFORM == "i386", "Requires i386")
    def test_registers_i386(self):
        d = debugger(RESOLVE_EXE("basic_test"))
        d.run()

        bp1 = d.breakpoint(0x8049186, hardware=False)
        bp2 = d.breakpoint(0x80491a3, hardware=False)
        bp3 = d.breakpoint(0x80491ac, hardware=False)
        bp4 = d.breakpoint(0x80491b5, hardware=False)

        d.cont()

        self.assertEqual(d.regs.eip, bp1.address)

        self.assertEqual(d.regs.eax, 0x00112233)
        self.assertEqual(d.regs.ebx, 0x11223344)
        self.assertEqual(d.regs.ecx, 0x22334455)
        self.assertEqual(d.regs.edx, 0x33445566)
        self.assertEqual(d.regs.esi, 0x44556677)
        self.assertEqual(d.regs.edi, 0x55667788)
        self.assertEqual(d.regs.ebp, 0x66778899)

        d.cont()

        self.assertEqual(d.regs.eip, bp2.address)

        self.assertEqual(d.regs.ax, 0x1122)
        self.assertEqual(d.regs.bx, 0x2233)
        self.assertEqual(d.regs.cx, 0x3344)
        self.assertEqual(d.regs.dx, 0x4455)
        self.assertEqual(d.regs.si, 0x5566)
        self.assertEqual(d.regs.di, 0x6677)
        self.assertEqual(d.regs.bp, 0x7788)

        d.cont()

        self.assertEqual(d.regs.eip, bp3.address)

        self.assertEqual(d.regs.al, 0x11)
        self.assertEqual(d.regs.bl, 0x22)
        self.assertEqual(d.regs.cl, 0x33)
        self.assertEqual(d.regs.dl, 0x44)

        d.cont()

        self.assertEqual(d.regs.eip, bp4.address)

        self.assertEqual(d.regs.ah, 0x12)
        self.assertEqual(d.regs.bh, 0x23)
        self.assertEqual(d.regs.ch, 0x34)
        self.assertEqual(d.regs.dh, 0x45)

        d.cont()

        d.kill()
        d.terminate()

    @skipUnless(PLATFORM == "i386", "Requires i386")
    def test_registers_hardware_i386(self):
        d = debugger(RESOLVE_EXE("basic_test"))
        d.run()

        bp1 = d.breakpoint(0x8049186, hardware=True)
        bp2 = d.breakpoint(0x80491a3, hardware=True)
        bp3 = d.breakpoint(0x80491ac, hardware=True)
        bp4 = d.breakpoint(0x80491b5, hardware=True)

        d.cont()

        self.assertEqual(d.regs.eip, bp1.address)

        self.assertEqual(d.regs.eax, 0x00112233)
        self.assertEqual(d.regs.ebx, 0x11223344)
        self.assertEqual(d.regs.ecx, 0x22334455)
        self.assertEqual(d.regs.edx, 0x33445566)
        self.assertEqual(d.regs.esi, 0x44556677)
        self.assertEqual(d.regs.edi, 0x55667788)
        self.assertEqual(d.regs.ebp, 0x66778899)

        d.cont()

        self.assertEqual(d.regs.eip, bp2.address)

        self.assertEqual(d.regs.ax, 0x1122)
        self.assertEqual(d.regs.bx, 0x2233)
        self.assertEqual(d.regs.cx, 0x3344)
        self.assertEqual(d.regs.dx, 0x4455)
        self.assertEqual(d.regs.si, 0x5566)
        self.assertEqual(d.regs.di, 0x6677)
        self.assertEqual(d.regs.bp, 0x7788)

        d.cont()

        self.assertEqual(d.regs.eip, bp3.address)

        self.assertEqual(d.regs.al, 0x11)
        self.assertEqual(d.regs.bl, 0x22)
        self.assertEqual(d.regs.cl, 0x33)
        self.assertEqual(d.regs.dl, 0x44)

        d.cont()

        self.assertEqual(d.regs.eip, bp4.address)

        self.assertEqual(d.regs.ah, 0x12)
        self.assertEqual(d.regs.bh, 0x23)
        self.assertEqual(d.regs.ch, 0x34)
        self.assertEqual(d.regs.dh, 0x45)

        d.cont()

        d.kill()
        d.terminate()

    @skipUnless(PLATFORM == "amd64", "Requires amd64")
    def test_register_find_amd64(self):
        d = debugger(RESOLVE_EXE("basic_test"))

        d.run()

        bp1 = d.breakpoint(0x4011CA)
        bp2 = d.breakpoint(0x40128D)
        bp3 = d.breakpoint(0x401239)
        bp4 = d.breakpoint(0x4011F4)
        bp5 = d.breakpoint(0x401296)

        d.cont()
        self.assertTrue(bp1.address == d.regs.rip)
        
        self.assertIn("rax", d.regs.filter(0x0011223344556677))
        self.assertIn("rbx", d.regs.filter(0x1122334455667700))
        self.assertIn("rcx", d.regs.filter(0x2233445566770011))
        self.assertIn("rdx", d.regs.filter(0x3344556677001122))
        self.assertIn("rsi", d.regs.filter(0x4455667700112233))
        self.assertIn("rdi", d.regs.filter(0x5566770011223344))
        self.assertIn("rbp", d.regs.filter(0x6677001122334455))
        self.assertIn("r8", d.regs.filter(0xAABBCCDD11223344))
        self.assertIn("r9", d.regs.filter(0xBBCCDD11223344AA))
        self.assertIn("r10", d.regs.filter(0xCCDD11223344AABB))
        self.assertIn("r11", d.regs.filter(0xDD11223344AABBCC))
        self.assertIn("r12", d.regs.filter(0x11223344AABBCCDD))
        self.assertIn("r13", d.regs.filter(0x223344AABBCCDD11))
        self.assertIn("r14", d.regs.filter(0x3344AABBCCDD1122))
        self.assertIn("r15", d.regs.filter(0x44AABBCCDD112233))
        
        d.cont()
        self.assertTrue(bp4.address == d.regs.rip)
        
        self.assertIn("al", d.regs.filter(0x11))
        self.assertIn("bl", d.regs.filter(0x22))
        self.assertIn("cl", d.regs.filter(0x33))
        self.assertIn("dl", d.regs.filter(0x44))
        self.assertIn("sil", d.regs.filter(0x55))
        self.assertIn("dil", d.regs.filter(0x66))
        self.assertIn("bpl", d.regs.filter(0x77))
        self.assertIn("r8b", d.regs.filter(0x88))
        self.assertIn("r9b", d.regs.filter(0x99))
        self.assertIn("r10b", d.regs.filter(0xAA))
        self.assertIn("r11b", d.regs.filter(0xBB))
        self.assertIn("r12b", d.regs.filter(0xCC))
        self.assertIn("r13b", d.regs.filter(0xDD))
        self.assertIn("r14b", d.regs.filter(0xEE))
        self.assertIn("r15b", d.regs.filter(0xFF))

        d.cont()
        self.assertTrue(bp3.address == d.regs.rip)
        
        self.assertIn("ax", d.regs.filter(0x1122))
        self.assertIn("bx", d.regs.filter(0x2233))
        self.assertIn("cx", d.regs.filter(0x3344))
        self.assertIn("dx", d.regs.filter(0x4455))
        self.assertIn("si", d.regs.filter(0x5566))
        self.assertIn("di", d.regs.filter(0x6677))
        self.assertIn("bp", d.regs.filter(0x7788))
        self.assertIn("r8w", d.regs.filter(0x8899))
        self.assertIn("r9w", d.regs.filter(0x99AA))
        self.assertIn("r10w", d.regs.filter(0xAABB))
        self.assertIn("r11w", d.regs.filter(0xBBCC))
        self.assertIn("r12w", d.regs.filter(0xCCDD))
        self.assertIn("r13w", d.regs.filter(0xDDEE))
        self.assertIn("r14w", d.regs.filter(0xEEFF))
        self.assertIn("r15w", d.regs.filter(0xFF00))

        d.cont()
        self.assertTrue(bp2.address == d.regs.rip)
        
        self.assertIn("eax", d.regs.filter(0x11223344))
        self.assertIn("ebx", d.regs.filter(0x22334455))
        self.assertIn("ecx", d.regs.filter(0x33445566))
        self.assertIn("edx", d.regs.filter(0x44556677))
        self.assertIn("esi", d.regs.filter(0x55667788))
        self.assertIn("edi", d.regs.filter(0x66778899))
        self.assertIn("ebp", d.regs.filter(0x778899AA))
        self.assertIn("r8d", d.regs.filter(0x8899AABB))
        self.assertIn("r9d", d.regs.filter(0x99AABBCC))
        self.assertIn("r10d", d.regs.filter(0xAABBCCDD))
        self.assertIn("r11d", d.regs.filter(0xBBCCDD11))
        self.assertIn("r12d", d.regs.filter(0xCCDD1122))
        self.assertIn("r13d", d.regs.filter(0xDD112233))
        self.assertIn("r14d", d.regs.filter(0x11223344))
        self.assertIn("r15d", d.regs.filter(0x22334455))
        

        d.cont()
        self.assertTrue(bp5.address == d.regs.rip)
        
        self.assertIn("ah", d.regs.filter(0x11))
        self.assertIn("bh", d.regs.filter(0x22))
        self.assertIn("ch", d.regs.filter(0x33))
        self.assertIn("dh", d.regs.filter(0x44))
        

        d.cont()
        d.kill()
        d.terminate()

    @skipUnless(PLATFORM == "aarch64", "Requires aarch64")
    def test_register_find_aarch64(self):
        d = debugger(RESOLVE_EXE("basic_test"))
        d.run()

        bp = d.breakpoint(0x4008a4)

        d.cont()

        assert d.regs.pc == bp.address
        
        self.assertIn("x0", d.regs.filter(0x4444333322221111))
        self.assertIn("x1", d.regs.filter(0x8888777766665555))
        self.assertIn("x2", d.regs.filter(0xccccbbbbaaaa9999))
        self.assertIn("x3", d.regs.filter(0x1111ffffeeeedddd))
        self.assertIn("x4", d.regs.filter(0x5555444433332222))
        self.assertIn("x5", d.regs.filter(0x9999888877776666))
        self.assertIn("x6", d.regs.filter(0xddddccccbbbbaaaa))
        self.assertIn("x7", d.regs.filter(0x22221111ffffeeee))
        self.assertIn("x8", d.regs.filter(0x6666555544443333))
        self.assertIn("x9", d.regs.filter(0xaaaa999988887777))
        self.assertIn("x10", d.regs.filter(0xeeeeddddccccbbbb))
        self.assertIn("x11", d.regs.filter(0x333322221111ffff))
        self.assertIn("x12", d.regs.filter(0x7777666655554444))
        self.assertIn("x13", d.regs.filter(0xbbbbaaaa99998888))
        self.assertIn("x14", d.regs.filter(0xffffeeeeddddcccc))
        self.assertIn("x15", d.regs.filter(0x4444333322221111))
        self.assertIn("x16", d.regs.filter(0x8888777766665555))
        self.assertIn("x17", d.regs.filter(0xccccbbbbaaaa9999))
        self.assertIn("x18", d.regs.filter(0x1111ffffeeeedddd))
        self.assertIn("x19", d.regs.filter(0x5555444433332222))
        self.assertIn("x20", d.regs.filter(0x9999888877776666))
        self.assertIn("x21", d.regs.filter(0xddddccccbbbbaaaa))
        self.assertIn("x22", d.regs.filter(0x22221111ffffeeee))
        self.assertIn("x23", d.regs.filter(0x6666555544443333))
        self.assertIn("x24", d.regs.filter(0xaaaa999988887777))
        self.assertIn("x25", d.regs.filter(0xeeeeddddccccbbbb))
        self.assertIn("x26", d.regs.filter(0x333322221111ffff))
        self.assertIn("x27", d.regs.filter(0x7777666655554444))
        self.assertIn("x28", d.regs.filter(0xbbbbaaaa99998888))
        self.assertIn("x29", d.regs.filter(0xffffeeeeddddcccc))
        self.assertIn("x30", d.regs.filter(0x4444333322221111))
        
        self.assertIn("lr", d.regs.filter(0x4444333322221111))
        self.assertIn("fp", d.regs.filter(0xffffeeeeddddcccc))
        self.assertIn("xzr", d.regs.filter(0))
        self.assertIn("wzr", d.regs.filter(0))

        d.regs.xzr = 0x123456789abcdef0
        d.regs.wzr = 0x12345678

        assert d.regs.xzr == 0
        assert d.regs.wzr == 0
        
        self.assertIn("wzr", d.regs.filter(0))
        self.assertIn("xzr", d.regs.filter(0))

        self.assertIn("w0", d.regs.filter(0x22221111))
        self.assertIn("w1", d.regs.filter(0x66665555))
        self.assertIn("w2", d.regs.filter(0xaaaa9999))
        self.assertIn("w3", d.regs.filter(0xeeeedddd))
        self.assertIn("w4", d.regs.filter(0x33332222))
        self.assertIn("w5", d.regs.filter(0x77776666))
        self.assertIn("w6", d.regs.filter(0xbbbbaaaa))
        self.assertIn("w7", d.regs.filter(0xffffeeee))
        self.assertIn("w8", d.regs.filter(0x44443333))
        self.assertIn("w9", d.regs.filter(0x88887777))
        self.assertIn("w10", d.regs.filter(0xccccbbbb))
        self.assertIn("w11", d.regs.filter(0x1111ffff))
        self.assertIn("w12", d.regs.filter(0x55554444))
        self.assertIn("w13", d.regs.filter(0x99998888))
        self.assertIn("w14", d.regs.filter(0xddddcccc))
        self.assertIn("w15", d.regs.filter(0x22221111))
        self.assertIn("w16", d.regs.filter(0x66665555))
        self.assertIn("w17", d.regs.filter(0xaaaa9999))
        self.assertIn("w18", d.regs.filter(0xeeeedddd))
        self.assertIn("w19", d.regs.filter(0x33332222))
        self.assertIn("w20", d.regs.filter(0x77776666))
        self.assertIn("w21", d.regs.filter(0xbbbbaaaa))
        self.assertIn("w22", d.regs.filter(0xffffeeee))
        self.assertIn("w23", d.regs.filter(0x44443333))
        self.assertIn("w24", d.regs.filter(0x88887777))
        self.assertIn("w25", d.regs.filter(0xccccbbbb))
        self.assertIn("w26", d.regs.filter(0x1111ffff))
        self.assertIn("w27", d.regs.filter(0x55554444))
        self.assertIn("w28", d.regs.filter(0x99998888))
        self.assertIn("w29", d.regs.filter(0xddddcccc))
        self.assertIn("w30", d.regs.filter(0x22221111))

        d.cont()

        d.kill()
        d.terminate()

    @skipUnless(PLATFORM == "i386", "Requires i386")
    def test_register_find_i386(self):
        d = debugger(RESOLVE_EXE("basic_test"))
        d.run()

        bp1 = d.breakpoint(0x8049186)
        bp2 = d.breakpoint(0x80491a3)
        bp3 = d.breakpoint(0x80491ac)
        bp4 = d.breakpoint(0x80491b5)

        d.cont()

        self.assertTrue(bp1.address == d.regs.eip)

        self.assertIn("eax", d.regs.filter(0x00112233))
        self.assertIn("ebx", d.regs.filter(0x11223344))
        self.assertIn("ecx", d.regs.filter(0x22334455))
        self.assertIn("edx", d.regs.filter(0x33445566))
        self.assertIn("esi", d.regs.filter(0x44556677))
        self.assertIn("edi", d.regs.filter(0x55667788))
        self.assertIn("ebp", d.regs.filter(0x66778899))

        d.cont()

        self.assertTrue(bp2.address == d.regs.eip)

        self.assertIn("ax", d.regs.filter(0x1122))
        self.assertIn("bx", d.regs.filter(0x2233))
        self.assertIn("cx", d.regs.filter(0x3344))
        self.assertIn("dx", d.regs.filter(0x4455))
        self.assertIn("si", d.regs.filter(0x5566))
        self.assertIn("di", d.regs.filter(0x6677))
        self.assertIn("bp", d.regs.filter(0x7788))

        d.cont()

        self.assertTrue(bp3.address == d.regs.eip)

        self.assertIn("al", d.regs.filter(0x11))
        self.assertIn("bl", d.regs.filter(0x22))
        self.assertIn("cl", d.regs.filter(0x33))
        self.assertIn("dl", d.regs.filter(0x44))

        d.cont()

        self.assertTrue(bp4.address == d.regs.eip)

        self.assertIn("ah", d.regs.filter(0x12))
        self.assertIn("bh", d.regs.filter(0x23))
        self.assertIn("ch", d.regs.filter(0x34))
        self.assertIn("dh", d.regs.filter(0x45))

        d.cont()

        d.kill()
        d.terminate()

    def test_registers_pprint(self):
        d = debugger(RESOLVE_EXE("basic_test"))

        d.run()

        # Temporarily redirect stdout to suppress output
        stdout = sys.stdout
        sys.stdout = StringIO()

        # The following calls should not terminate
        d.pprint_registers()
        d.pprint_registers_all()
        d.pprint_regs()
        d.pprint_regs_all()

        # Reset stdout
        sys.stdout = stdout

        d.kill()
        d.terminate()
        
    def test_register_debugger_status(self):
        d = debugger(RESOLVE_EXE("basic_test"))
        
        with self.assertRaises(RuntimeError):
            d.regs

        d.run()
        
        registers = d.regs
        
        d.detach()
        
        with self.assertRaises(RuntimeError): 
            d.regs
            
        with self.assertRaises(RuntimeError):
            registers.__getattribute__(REGISTER_ACCESS)
        
        d.terminate()
        
        



# SPDX-License-Identifier: Apache-2.0
# chip-lab 내보내기: 기대값은 chip-lab 고정 기준 모델(reference-1.0, seed 42)에서 계산했다.

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge, Timer


async def reset(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="us").start())
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)

DIVISOR = 8
NBYTES = 3
WIDTH = 20
CASES = [[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 0], [[-128, -128, -128, -128, -128, -128, -128, -128, -128, -128, -128, -128, -128, -128, -128, -128], 131072], [[127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127], 129032], [[-128, 127, -128, 127, -128, 127, -128, 127, -128, 127, -128, 127, -128, 127, -128, 127], -130048], [[127, 1, -128, 1, 127, 1, -128, 1, 127, 1, -128, 1, 127, 1, -128, 1], -4], [[-71, 88, -116, -112, 12, -113, -3, -81, -14, -17, -57, -9, -76, -115, -84, -27], 17390], [[86, 14, -16, -49, 101, -18, 14, 44, -125, -76, -47, -81, 88, 66, 46, -79], 16267], [[55, 22, 48, 57, 7, -30, -106, -93, 107, -105, -65, -12, 65, 20, -88, -88], 12183], [[-9, 53, -77, -21, 66, 8, 14, -92, 104, -41, 58, -3, -45, -45, 61, 108], 4555], [[66, 77, 10, 9, -16, -95, 38, -20, -100, 33, -11, -20, -112, 127, 33, 74], -8930], [[106, 57, -55, -16, 7, -58, -57, 124, -2, -82, 6, -104, 91, -72, 76, -50], -11364], [[-47, -70, 88, 8, -96, 46, 69, -71, 67, 22, 111, 94, 0, -48, -123, 104], -6205], [[-127, -46, 6, -128, -37, 37, -74, 122, 24, -119, -27, -71, -50, 57, 63, 29], -7285], [[-6, -63, -99, 115, -5, -44, -88, 7, -85, 88, 120, -20, -93, -26, -64, 31], -20849], [[76, 45, 63, -118, 96, -11, 103, -16, -67, -125, -2, -92, -13, -98, -96, -11], 4171], [[-94, -61, -112, 114, 41, -4, -92, 114, -7, 80, 14, -31, 120, -80, -19, -79], -26779], [[92, 78, 53, 45, 88, -73, 82, -1, 111, -30, -101, -31, -78, 101, -97, -57], 507], [[88, -103, -35, -121, 14, -81, 108, -7, -1, -43, -90, 80, 98, 120, -78, 118], -11320], [[-19, 104, 77, 18, -98, 88, -44, 121, 66, -49, -127, -31, 71, 23, 7, -17], -12321], [[-99, -87, -97, -33, 32, -93, -99, -94, -103, -8, 116, 78, -48, -67, -99, -2], 31430], [[-108, 7, -87, 74, 86, -61, 33, 25, 5, 106, -24, 33, 32, -91, -6, -124], -14045], [[106, -3, -77, 61, -91, 17, -19, -48, 7, 96, -61, 26, 50, -124, -93, 25], -15089], [[-75, -21, -60, 47, 7, -24, -69, 7, -74, 122, -49, 0, 11, -102, 16, -81], -13342], [[88, 98, 13, 90, -106, -124, -127, -71, 42, -90, -62, -52, 6, -110, -46, 61], 27933], [[-53, -21, 92, -1, -63, -76, -107, 53, 29, 80, 58, -49, -108, -7, 55, -45], -2103], [[-38, -47, 83, -73, -116, 67, -37, -109, 42, 112, 82, -15, -1, -26, 8, 107], -3656], [[51, 14, 28, -93, -12, 14, -14, 51, -116, 76, -30, 41, 76, -114, 40, -69], -24242], [[5, 95, -37, -69, 7, 69, -109, -31, -73, 2, 94, -106, 48, 95, 32, -128], -2756], [[-28, 30, 58, 81, 92, 39, -93, 78, 41, 23, 32, -63, -65, -30, 25, 87], 3244]]


async def falls(dut, count):
    for _ in range(count):
        await FallingEdge(dut.clk)


async def send(dut, byte, stop=1):
    for bit in [0] + [(byte >> i) & 1 for i in range(8)] + [stop]:
        dut.ui_in.value = bit << 3
        await falls(dut, DIVISOR)
    dut.ui_in.value = 0b1000


def tx(dut):
    return (dut.uo_out.value.to_unsigned() >> 4) & 1


async def receive(dut):
    for _ in range(40 * DIVISOR * (NBYTES + 2) + 400):
        if tx(dut) == 0:
            break
        await FallingEdge(dut.clk)
    else:
        assert False, "결과 시작 비트가 오지 않음"
    await falls(dut, DIVISOR // 2)
    assert tx(dut) == 0
    value = 0
    for i in range(8):
        await falls(dut, DIVISOR)
        value |= tx(dut) << i
    await falls(dut, DIVISOR)
    assert tx(dut) == 1, "정지 비트"
    return value


def signed(value, bits):
    value &= (1 << bits) - 1
    return value - (1 << bits) if value >> (bits - 1) else value


@cocotb.test()
async def test_dot_product_over_uart(dut):
    await reset(dut)
    dut.ui_in.value = 0b1000
    await falls(dut, 3 * DIVISOR)
    for index, (stream, expected) in enumerate(CASES):
        if index == 2:
            for byte in (0x11, 0x22, 0x33)[:min(3, 2 * len(stream) // 2 - 1)]:
                await send(dut, byte)
            await send(dut, 0x44, stop=0)
            await falls(dut, 2 * DIVISOR)
            assert (dut.uo_out.value.to_unsigned() >> 1) & 1, "ERR 가 켜지지 않음"
        for byte in stream:
            await send(dut, byte & 0xFF)
        raw = 0
        for k in range(NBYTES):
            raw |= (await receive(dut)) << (8 * k)
        assert signed(raw, WIDTH) == expected, f"case {index}: {signed(raw, WIDTH)} != {expected}"
    assert (dut.uo_out.value.to_unsigned() >> 5) == len(CASES) % 8

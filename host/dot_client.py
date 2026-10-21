#!/usr/bin/env python3
"""chip-lab 이 생성한 호스트 클라이언트: 직렬 포트로 내적 가속기와 주고받는다.

사용: pip install pyserial && python3 host/dot_client.py /dev/tty.usbmodemXXXX
칩 클록이 f Hz 면 baud = f / DIVISOR 다 (예: 10MHz, 분주 8 → 1,250,000 baud). 데모 보드에서 RP2040 이
ui_in[3](RX)·uo_out[4](TX)를 USB 직렬로 이어 주는 설정은 Tiny Tapeout 데모 보드 문서를 따른다 (이 스크립트는 그 설정을 하지 않는다).
"""
import json
import sys
from pathlib import Path

CONFIG = json.loads((Path(__file__).with_name('vectors.json')).read_text())


def order(a, b):
    return [v for pair in zip(a, b) for v in pair] if CONFIG['operand_order'] == 'interleaved' else a + b


def signed(value, bits):
    value &= (1 << bits) - 1
    return value - (1 << bits) if value >> (bits - 1) else value


def exchange(port, a, b):
    port.write(bytes(v & 0xFF for v in order(a, b)))
    raw = port.read(CONFIG['nbytes'])
    if len(raw) != CONFIG['nbytes']:
        raise TimeoutError(f'결과 {len(raw)}/{CONFIG["nbytes"]} 바이트만 받음')
    return signed(int.from_bytes(raw, 'little'), CONFIG['acc_width'])


def main(path, baud=None):
    import serial
    clock = CONFIG['clock_hz']
    with serial.Serial(path, baud or clock // CONFIG['divisor'], timeout=2) as port:
        failures = 0
        for index, (a, b, expected) in enumerate(CONFIG['cases']):
            got = exchange(port, a, b)
            mark = 'OK' if got == expected else 'FAIL'
            failures += got != expected
            print(f'{index:2d} {mark} got {got} expected {expected}')
        print(f'{len(CONFIG["cases"]) - failures}/{len(CONFIG["cases"])} 일치')
        return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else None))

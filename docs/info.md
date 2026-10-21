<!---
chip-lab 이 생성한 문서입니다.
-->

## How it works

UART(8N1, 비트당 8 클록)로 부호 있는 INT8 벡터 두 개(N=8)를 받아 내적을 계산하고 결과를 UART 로 돌려주는 가속기입니다. 모든 곱을 정확히 더한 뒤 20bit saturate 를 한 번 적용합니다.

chip-lab 에서 고정 기준 모델·RTL scoreboard 로 검증한 설계 `3c0e790e-9bc7-4b0f-ac17-f176d263fcc5` 를 Tiny Tapeout 핀에 맞춰 감쌌습니다.
배치 전 sky130 표준셀 면적은 6506µm², 선택한 타일은 1x1 입니다 (사전 추정).

## How to test

데모 보드 RP2040 직렬 포트(ui_in[3]=RX, uo_out[4]=TX)로 a0,b0,…,a7,b7 를 16바이트로 보내면 결과 3바이트가 하위 바이트부터 돌아옵니다. uo_out[0] 은 BUSY, uo_out[1] 은 프레이밍 오류 표시, uo_out[7:5] 는 완료한 벡터 수입니다.

## External hardware

없음.

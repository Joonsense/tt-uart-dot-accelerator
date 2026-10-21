/*
 * chip-lab 내보내기 · 설계 3c0e790e-9bc7-4b0f-ac17-f176d263fcc5
 * UART INT8 내적 가속기 N=8, 결과 20bit saturate, 비트당 8 클록, 피연산자 순서 interleaved
 * SPDX-License-Identifier: Apache-2.0
 *
 * Tiny Tapeout 권장 UART 핀 (데모 보드 RP2040 직렬 연결)
 *   ui_in[3]    RX  (호스트 → 칩: a0,b0,a1,b1,… 바이트)
 *   uo_out[4]   TX  (칩 → 호스트: 결과 3 바이트, 하위 바이트부터)
 *   uo_out[0]   BUSY
 *   uo_out[1]   ERR (프레이밍 오류 뒤 다음 벡터 완료 전까지 1)
 *   uo_out[7:5] 완료 벡터 수 (8로 나눈 나머지)
 */
`default_nettype none

module tt_um_joonsense_uart_dot_3c0e790e (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);
  wire txd, busy, err_seen;
  wire [2:0] count;

  tt_um_joonsense_uart_dot_3c0e790e_core core (.clk(clk), .rst(!rst_n), .rxd(ui_in[3]), .txd(txd), .busy(busy), .err_seen(err_seen), .count(count));

  assign uo_out  = {count, txd, 2'b00, err_seen, busy};
  assign uio_out = 8'h00;
  assign uio_oe  = 8'h00;

  wire _unused = &{ena, ui_in[7:4], ui_in[2:0], uio_in, 1'b0};

endmodule

`default_nettype wire

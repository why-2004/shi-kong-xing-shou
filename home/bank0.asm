_Start::
	ldh [hFF91], a
	ld sp, $dfff

; Scroll
	xor a
	ldh [rSCX], a
	ldh [rSCY], a
; LCD
	di
	ld a, LCDCF_OFF
	ldh [rLCDC], a
; Palettes
	ld a, %11100100
	ldh [rBGP], a
	ld a, %00011100
	ld [$dce7], a
	ldh [rOBP0], a
	ldh [rOBP1], a
; STAT
	ld a, $40
	ldh [rSTAT], a
	ld a, 143
	ldh [rLYC], a
; Interrupts
	ld a, 0
	ldh [rIF], a
	ld a, IEF_VBLANK + IEF_LCDC
	ldh [rIE], a

	jp Func_0200

unk_017f:
	dr $017f, $0200

Func_0200:
	dr $0200, $0257

Func_0257:
	dr $0257, $02bf

DelayFrame:
; Wastes cycles until the VBlank interrupt occurs, where hVBlank is set to 1
; VBlank will never occur if the LCD is off
	ldh a, [rLCDC]
	and a
	ret z

	ldh a, [hVBlank]
	and a
	jr z, DelayFrame

	xor a
	ldh [hVBlank], a
	ret

Func_02cc:
	dr $02cc, $096a

Func_096a::
; Switch intro scene?
	dr $096a, $09d2

Func_09d2::
	dr $09d2, $0b69

Func_0b69:
	dr $0b69, $0c17

Func_0c17:
	ld a, [$d986]
	and a
	jr nz, .asm_0c22
	ld a, [$d9e2]
	jr .asm_0c25

.asm_0c22
	ld a, [$d9e3]

.asm_0c25
	ld [$d9d8], a
	farcall unk_026_4000
	pop hl
	push hl
	jp Func_0b69

Func_0c33::
	dr $0c33, $2843

VBlank::
	dr $2843, $2886

Func_2886:
	dr $2886, $28be

LCD::
	dr $28be, $28fb

PrintCharacter:
; Print one vertically arranged character using four tiles
	ld a, [wCharacterBGMapTransferStatus]
	and a
	ret z

; Backup stack pointer
	ld [hFFA2], sp

; BG map addresses are held at wc0b0
	ld hl, wc0b0
	ld sp, hl
	ld a, [wcbf3]
; Each character occupies four tiles
REPT 3
	pop bc
	ld [bc], a
	inc a
ENDR
	pop bc
	ld [bc], a

; Restore old stack pointer
	ldh a, [hFFA2]
	ld l, a
	ldh a, [hFFA2 + 1]
	ld h, a
	ld sp, hl

	xor a
	ld [wCharacterBGMapTransferStatus], a
	ret

Get1bpp:
	ld a, [wCharacterTileTransferStatus]
	and a
	ret z

; Save current ROM bank
	ld a, [_BANKNUM]
	push af
; Switch
	ldh a, [hTargetBank]
	rst Bankswitch

; Backup stack pointer
	ld [hFFA2], sp

	ld a, [wCharacterTileSrc]
	ld l, a
	ld a, [wCharacterTileSrc + 1]
	ld h, a
	ld sp, hl

	ld a, [wCharacterTileDest]
	ld l, a
	ld a, [wCharacterTileDest + 1]
	ld h, a
	ld a, [wCharacterTileCount]
	ld e, a

.load_tile
REPT 3
	pop bc
	ld [hl], c
	inc l
	ld [hl], c
	inc l
	ld [hl], b
	inc l
	ld [hl], b
	inc l
ENDR
	pop bc
	ld [hl], c
	inc l
	ld [hl], c
	inc l
	ld [hl], b
	inc l
	ld [hl], b

	inc hl
	dec e
	jr nz, .load_tile

; Restore old stack pointer
	ldh a, [hFFA2]
	ld l, a
	ldh a, [hFFA2 + 1]
	ld h, a
	ld sp, hl

	xor a
	ld [wCharacterTileTransferStatus], a
	pop af
	rst Bankswitch
	ret

Func_297a:
	dr $297a, $4000

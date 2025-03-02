Func_005_4000::
	dr $14000, $1401d

Func_005_401d::
	dr $1401d, $1406b

Func_005_406b::
	dr $1406b, $14093

ParseCurrentMapEvents::
; Determine player's Y position
; Store it to c
	ldh a, [hSCY]
	ld l, a
	ldh a, [hFFB1]
	ld h, a
	ld a, [wcd00]
	sub $10
	ld c, a
	ld a, 0
	sbc 0
	ld b, a
	add hl, bc
	srl h
	rr l
	srl h
	rr l
	srl h
	rr l
	srl h
	rr l
	ld c, l
	ldh a, [hMapOffsetY]
	add a
	add c
	ld c, a

; Determine player's X position
; Store it to b
	ldh a, [hSCX]
	ld l, a
	ldh a, [hFFAF]
	ld h, a
	ld a, [wcd01]
	sub 8
	ld e, a
	ld a, 0
	sbc 0
	ld d, a
	add hl, de
	srl h
	rr l
	srl h
	rr l
	srl h
	rr l
	srl h
	rr l
	ld b, l
	ldh a, [hMapOffsetX]
	add a
	add b
	ld b, a

	ld hl, wMapEvents

MapEventLoop:
.check_x
	push hl
	ld a, [hli]
; $FF marks end of map events
	cp -1
	jr z, .exit
; $EE marks any X position
	cp ABSOLUTE
	jr z, .check_y
	cp b
	jr nz, JumpToNextMapEvent

.check_y
	ld a, [hli]
; $EE marks any Y position
	cp ABSOLUTE
	jr z, .execute_event
	cp c
	jr nz, JumpToNextMapEvent

.execute_event
	ld de, MapEvent_Jumptable
	ld a, [hli]
	push hl
	ld l, a
	ld h, 0
	add hl, hl
	add hl, de
	ld a, [hli]
	ld h, [hl]
	ld l, a
	jp hl

.exit
	pop hl
	xor a
	ld [wd1e3], a
	ld [wdcb4], a
	ld [wd0f8], a
	ld [wd0ee], a
	ret

JumpToNextMapEvent:
	pop hl
	ld a, l
	add 6
	ld l, a
	jr MapEventLoop

MapEvent_Jumptable:
	dw MapEvent_Warp      ; 00
	dw MapEvent_Script    ; 01
	dw MapEvent_Signpost  ; 02
	dw MapEvent_FarWarp   ; 03
	dw MapEvent_04        ; 04
	dw MapEvent_05        ; 05
	dw MapEvent_06        ; 06
	dw MapEvent_07        ; 07

MapEvent_Warp:
	pop hl
	ld a, [hli]
	ldh [hMapNumber], a
	ld a, [hli]
	ldh [hWarpNumber], a
	ld a, [hli]
	ldh [hScrollNumber], a
	ld a, 1
	ldh [hFade], a
	pop hl
	ret

MapEvent_FarWarp:
	pop hl
	ld a, [hli]
	ldh [hMapNumber], a
	ld a, [hli]
	ldh [hWarpNumber], a
	ld a, [hli]
	ldh [hMapGroup], a
	xor a
	ld [hScrollNumber], a
	ld a, 1
	ldh [hFade], a
	pop hl
	ret

MapEvent_Script:
	pop hl
	ld a, [hl]
	and a
	jr z, .no_conditional
	ldh a, [hFFBA]
	cp [hl]
	jp nz, JumpToNextMapEvent

.no_conditional
	inc hl
	ld a, [hli]
	ld [wScriptPos], a
	ld a, [hli]
	ld [wScriptPos + 1], a
	ld a, 1
	ldh [hFFD6], a
	xor a
	ld [wScriptByte], a
	ld [wd1e3], a
	ld [wd0f8], a
	ld [wd0ee], a
	ld [wdcb4], a
	pop hl
	ret

MapEvent_Signpost:
	pop hl
	ld a, [hli]
	ld [wd1e3], a
	xor a
	ld [wd0f8], a
	ld [wd0ee], a
	ld [wdcb4], a
	pop hl
	ret

MapEvent_04:
	pop hl
	ld a, [hl]
	and a
	jr z, .no_conditional
	ldh a, [hFFBA]
	cp [hl]
	jp nz, JumpToNextMapEvent

.no_conditional
	inc hl
	ld a, [hli]
	ld [wScriptPos], a
	ld a, [hli]
	ld [wScriptPos + 1], a
	ld a, 1
	ld [wd0f8], a
	xor a
	ld [wd1e3], a
	ld [wd0ee], a
	ld [wdcb4], a
	pop hl
	ret

MapEvent_05:
	pop hl
	ld a, [hli]
	ld [wd0ee], a
	ld a, [hli]
	ld [wScriptPos], a
	ld a, [hli]
	ld [wScriptPos + 1], a
	xor a
	ld [wd1e3], a
	ld [wd0f8], a
	ld [wdcb4], a
	pop hl
	ret

MapEvent_06:
	pop hl
	ld a, [hl]
	and a
	jr z, .no_conditional
	ldh a, [hFFBA]
	cp [hl]
	jp nc, JumpToNextMapEvent

.no_conditional
	inc hl
	ld a, [hli]
	ld [wScriptPos], a
	ld a, [hli]
	ld [wScriptPos + 1], a
	ld a, 1
	ldh [hFFD6], a
	xor a
	ld [wScriptByte], a
	pop hl
	ret

MapEvent_07:
	pop hl
	ld a, [hli]
	ld [wdcb4], a
	xor a
	ld [wd0f8], a
	ld [wd0ee], a
	ld [wd1e3], a
	pop hl
	ret

Overworld::
; upon entering overworld
	call PlayMapMusic
; ?
	ld a, $1C
	ld [wdce7], a

	xor a
	ldh [hFade], a
	ldh [hFFBC], a	; textbox enable
	ldh [hFFC2], a	; map animations

	xor a
	ldh [hSCX], a
	ldh [hFFAF], a
	ldh [hSCY], a
	ldh [hFFB1], a
	ldh [hFF9F], a
	ldh [hFFA0], a
	ldh [hFFC2], a
	ldh [hJoypadDown], a
	ldh [hJoypadPressed], a
	ld a, $FF
	ldh [hFF9E], a

	ld hl, wd1e3 + 2
	ld c, $0C
	xor a
.fill
	ld [hli], a
	dec c
	jr nz, .fill

	call Func_005_4408
	call Func_005_5a9c
	call Func_05ff
	call Func_005_5a32
	ld hl, $9800
	ld de, wTilemap
	ld bc, $1412
	ld a, $12
	ld [hFF93], a
	ld a, $14
	ldh [hFF92], a
	call Func_005_5a59
	call Func_005_5a8e
	call Func_005_4662
	call Func_005_401d
	call Func_0557
	call Func_005_4000
	xor a
	ldh [hSimulatedJoypadState], a
	ldh [hFFA4], a
	call Func_0419
	ld a, $C7
	ldh [rLCDC], a
	ld hl, wcab0
	xor a
	ldh [hFFC4], a
	ldh [hFF9D], a
	ld [wd9d2], a
	call FadeInPalette

OverworldLoop:
	call DelayFrame

; increase frame counter
	ldh a, [hFF9D]
	inc a
	ldh [hFF9D], a

; check if we're fading to another map
	ldh a, [hFade]
	and a
	jp nz, Overworld_DoFade

; check if we have any part of the start menu open
	ldh a, [hFFC5]
	and a
	jp nz, Overworld_GotoProcessStartMenu

; check if we should be in battle
	ldh a, [hFFD3]
	and a
	jp nz, Overworld_GotoBattleJumptable

; not in battle

	call Func_005_43e1
; update OAM?
	call Func_0419

; check if we should briefly display
; a short text scroll now
	ldh a, [hScrollNumber]
	and a
	jp nz, Overworld_GotoProcessScroll

; check if we should be spawning
; a text box
	ldh a, [hFFBC]
	and a
	jp nz, Overworld_GotoProcessTextbox

; check if we are currently in a script
	ldh a, [hFFD6]
	and a
	jp nz, Overworld_GotoProcessScript

; trigger joypad reading
	ld a, $01
	ld [wd082], a

; move one step
	call Overworld_MovePlayerOneStep

; check for fade (again)
	ldh a, [hFade]
	and a
	jr nz, Overworld_DoFade

; disable joypad reading
	xor a
	ld [wd082], a

; if we are in a battle, go back to loop
	ld a, [hFFD3]
	and a
	jr nz, OverworldLoop

; specific events in the overworld
	call Overworld_DoBlackFlashing
	call Func_005_4bc1
	call Overworld_ProcessJoypadInput

; object events?
	call Func_062c
	call Func_0426
	call Func_005_440f
	jp OverworldLoop

Overworld_GotoProcessScript:
	xor a
	ld [wd082], a
	call Func_06d0
	call Func_005_440f
	call Func_0426
	jp OverworldLoop

Overworld_GotoProcessTextbox:
	ld hl, wTextStart
	ld a, [hli]
	ld h, [hl]
	ld l, a
	call Func_06c6
	jp OverworldLoop

Overworld_GotoProcessScroll:
	call Func_074d
	jp OverworldLoop

Overworld_GotoProcessStartMenu:
	call Func_0b39
	jp OverworldLoop

Overworld_GotoBattleJumptable:
	farcall BattleJumptable
	jp OverworldLoop

Overworld_DoFade:
	ld a, [wcd03]
	ld [wd0e3], a
	ld a, [wcd23]
	ld [wdcec], a
	jp JumpToGameMode

Overworld_DoBlackFlashing:
; for maps 04:06 through 04:09
; flashes to black, and then flashes back
; to the original palette
	ld a, [hMapGroup]
	cp $04
	ret nz
	ldh a, [hMapNumber]
	cp $06
	jr z, .DoFlash
	cp $07
	jr z, .DoFlash
	cp $08
	jr z, .DoFlash
	cp $09
	jr z, .DoFlash
	ret

.DoFlash:
	ld a, [wdcb6 + 3]
	and a
	jr z, Func_005_434a
	ld a, [wdcb6 + 2]
	inc a
	ld [wdcb6 + 2], a
	cp $20
	ret nz
	xor a
	ld [wdcb6 + 2], a
	ld [wdcb6 + 3], a
	ld hl, unk_005_4394
	call PartialCopyBackgroundPalettes
	ret

Func_005_434a:
	dr $1434a, $14394

unk_005_4394:
	dr $14394, $143e1

Func_005_43e1:
	dr $143e1, $14408

Func_005_4408:
	dr $14408, $1440f

Func_005_440f:
	dr $1440f, $14662

Func_005_4662:
	dr $14662, $1495f

Overworld_MovePlayerOneStep:
	dr $1495f, $14bc1

Func_005_4bc1:
	dr $14bc1, $14bfa

.asm_4bfa:
	ld de, 6
	ldh a, [hJoypadPressed]
	bit START_F, a
	jp nz, Func_005_4f2e

	ldh a, [hJoypadDown]
	bit D_DOWN_F, a
	jr nz, .down
	bit D_UP_F, a
	jr nz, .up
	bit D_LEFT_F, a
	jr nz, .left
	bit D_RIGHT_F, a
	jr nz, .right

	jr .asm_4c1c

.down:
	add hl, de

.up:
	add hl, de

.left:
	add hl, de

.right:
	add hl, de

.asm_4c1c:
	ld a, [hli]
	ldh [hFF9E], a
	ld a, [hli]
	ldh [hSimulatedJoypadState], a
	ld a, [hli]
	ld [wd1f9], a
	ld a, [hli]
	ld [wd1fa], a
	ld a, [hli]
	ld h, [hl]
	ld l, a
	ld a, [hl]
	ldh [hFFA1], a
	ldh a, [hFF9E]
	cp $ff
	jr nz, .asm_4c3a
	call Func_005_4e4e
	ret

.asm_4c3a:
	dr $14c3a, $14c69

Func_005_4c69:
	dr $14c69, $14e4e

Func_005_4e4e:
	dr $14e4e, $14f2e

Func_005_4f2e:
; Init Start Menu
	ld a, 1
	ldh [hFFC5], a
	ld [wd087], a
	xor a
	ld [wd08a], a
	call Func_005_4f3d
	ret

Func_005_4f3d:
	ld hl, wcde0
	ld c, $20
	xor a
.clear
	ld [hli], a
	dec c
	jr nz, .clear
	ret

Func_005_4f48:
; on battle start
	dr $14f48, $150a5

Func_005_50a5:
	farcall Func_02d_5086
	xor a
	ld [wd987], a
	ld hl, wd876
	ld a, l
	ld [wd984], a
	ld a, h
	ld [wd984 + 1], a
	ld a, [hl]
	ld [wEnemyMonSpecies], a

	ld bc, wPartyMons
	ld e, 0
.asm_50c3:
	ld hl, 2
	add hl, bc
	ld a, [hli]
	or [hl]
	jr nz, .asm_50d8

	ld hl, PARTYMON_STRUCT_LENGTH
	add hl, bc
	inc e
	ld a, l
	cp $80
	ret nc

	ld c, l
	ld b, h
	jr .asm_50c3

.asm_50d8:
	ld a, e
	ld [wd983], a
	ld a, c
	ld [wd981], a
	ld a, b
	ld [wd981 + 1], a
	ret

Func_005_50e5:
	dr $150e5, $151db

Func_005_51db:
	xor a
	ld [wdcea], a
	ld hl, wcd20
	ld bc, 3
; ???
	xor a
.asm_51e6
	ld [hli], a
	dec c
	ld a, c
	or b
	jr nz, .asm_51e6
	ret

Func_005_51ed:
	dr $151ed, $1576c

Overworld_ProcessJoypadInput:
	dr $1576c, $15a32

Func_005_5a32:
	dr $15a32, $15a59

Func_005_5a59:
	dr $15a59, $15a8e

Func_005_5a8e:
	ld hl, wcd00
	ld bc, $100
.clear
	xor a
	ld [hli], a
	dec bc
	ld a, c
	or b
	jr nz, .clear
	ret

Func_005_5a9c:
	dr $15a9c, $15cf0


SECTION "banknum5", ROMX[$7fff], BANK[$5]
	db $5

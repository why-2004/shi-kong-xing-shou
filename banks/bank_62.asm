Func_062_4000::
	dr $188000, $189df3

Func_062_5df3::
	dr $189df3, $189f9c

Func_062_5f9c::
; Sound test
	dr $189f9c, $18a029

Func_062_6029:
	dr $18a029, $18a710


SECTION "banknum62", ROMX[$7fff], BANK[$62]
	db $62

from . import CS_OP_INVALID, CS_OP_REG, CS_OP_IMM, CS_OP_MEM
# For Capstone Engine. AUTO-GENERATED FILE, DO NOT EDIT [mos65xx_const.py]

MOS65XX_REG_INVALID = 0
MOS65XX_REG_ACC = 1
MOS65XX_REG_X = 2
MOS65XX_REG_Y = 3
MOS65XX_REG_P = 4
MOS65XX_REG_SP = 5
MOS65XX_REG_DP = 6
MOS65XX_REG_B = 7
MOS65XX_REG_K = 8
MOS65XX_REG_ENDING = 9

MOS65XX_AM_NONE = 0
MOS65XX_AM_IMP = 1
MOS65XX_AM_ACC = 2
MOS65XX_AM_IMM = 3
MOS65XX_AM_REL = 4
MOS65XX_AM_INT = 5
MOS65XX_AM_BLOCK = 6
MOS65XX_AM_ZP = 7
MOS65XX_AM_ZP_X = 8
MOS65XX_AM_ZP_Y = 9
MOS65XX_AM_ZP_REL = 10
MOS65XX_AM_ZP_IND = 11
MOS65XX_AM_ZP_X_IND = 12
MOS65XX_AM_ZP_IND_Y = 13
MOS65XX_AM_ZP_IND_LONG = 14
MOS65XX_AM_ZP_IND_LONG_Y = 15
MOS65XX_AM_ABS = 16
MOS65XX_AM_ABS_X = 17
MOS65XX_AM_ABS_Y = 18
MOS65XX_AM_ABS_IND = 19
MOS65XX_AM_ABS_X_IND = 20
MOS65XX_AM_ABS_IND_LONG = 21
MOS65XX_AM_ABS_LONG = 22
MOS65XX_AM_ABS_LONG_X = 23
MOS65XX_AM_SR = 24
MOS65XX_AM_SR_IND_Y = 25

MOS65XX_INS_INVALID = 0
MOS65XX_INS_ADC = 1
MOS65XX_INS_AND = 2
MOS65XX_INS_ASL = 3
MOS65XX_INS_BBR = 4
MOS65XX_INS_BBS = 5
MOS65XX_INS_BCC = 6
MOS65XX_INS_BCS = 7
MOS65XX_INS_BEQ = 8
MOS65XX_INS_BIT = 9
MOS65XX_INS_BMI = 10
MOS65XX_INS_BNE = 11
MOS65XX_INS_BPL = 12
MOS65XX_INS_BRA = 13
MOS65XX_INS_BRK = 14
MOS65XX_INS_BRL = 15
MOS65XX_INS_BVC = 16
MOS65XX_INS_BVS = 17
MOS65XX_INS_CLC = 18
MOS65XX_INS_CLD = 19
MOS65XX_INS_CLI = 20
MOS65XX_INS_CLV = 21
MOS65XX_INS_CMP = 22
MOS65XX_INS_COP = 23
MOS65XX_INS_CPX = 24
MOS65XX_INS_CPY = 25
MOS65XX_INS_DEC = 26
MOS65XX_INS_DEX = 27
MOS65XX_INS_DEY = 28
MOS65XX_INS_EOR = 29
MOS65XX_INS_INC = 30
MOS65XX_INS_INX = 31
MOS65XX_INS_INY = 32
MOS65XX_INS_JML = 33
MOS65XX_INS_JMP = 34
MOS65XX_INS_JSL = 35
MOS65XX_INS_JSR = 36
MOS65XX_INS_LDA = 37
MOS65XX_INS_LDX = 38
MOS65XX_INS_LDY = 39
MOS65XX_INS_LSR = 40
MOS65XX_INS_MVN = 41
MOS65XX_INS_MVP = 42
MOS65XX_INS_NOP = 43
MOS65XX_INS_ORA = 44
MOS65XX_INS_PEA = 45
MOS65XX_INS_PEI = 46
MOS65XX_INS_PER = 47
MOS65XX_INS_PHA = 48
MOS65XX_INS_PHB = 49
MOS65XX_INS_PHD = 50
MOS65XX_INS_PHK = 51
MOS65XX_INS_PHP = 52
MOS65XX_INS_PHX = 53
MOS65XX_INS_PHY = 54
MOS65XX_INS_PLA = 55
MOS65XX_INS_PLB = 56
MOS65XX_INS_PLD = 57
MOS65XX_INS_PLP = 58
MOS65XX_INS_PLX = 59
MOS65XX_INS_PLY = 60
MOS65XX_INS_REP = 61
MOS65XX_INS_RMB = 62
MOS65XX_INS_ROL = 63
MOS65XX_INS_ROR = 64
MOS65XX_INS_RTI = 65
MOS65XX_INS_RTL = 66
MOS65XX_INS_RTS = 67
MOS65XX_INS_SBC = 68
MOS65XX_INS_SEC = 69
MOS65XX_INS_SED = 70
MOS65XX_INS_SEI = 71
MOS65XX_INS_SEP = 72
MOS65XX_INS_SMB = 73
MOS65XX_INS_STA = 74
MOS65XX_INS_STP = 75
MOS65XX_INS_STX = 76
MOS65XX_INS_STY = 77
MOS65XX_INS_STZ = 78
MOS65XX_INS_TAX = 79
MOS65XX_INS_TAY = 80
MOS65XX_INS_TCD = 81
MOS65XX_INS_TCS = 82
MOS65XX_INS_TDC = 83
MOS65XX_INS_TRB = 84
MOS65XX_INS_TSB = 85
MOS65XX_INS_TSC = 86
MOS65XX_INS_TSX = 87
MOS65XX_INS_TXA = 88
MOS65XX_INS_TXS = 89
MOS65XX_INS_TXY = 90
MOS65XX_INS_TYA = 91
MOS65XX_INS_TYX = 92
MOS65XX_INS_WAI = 93
MOS65XX_INS_WDM = 94
MOS65XX_INS_XBA = 95
MOS65XX_INS_XCE = 96
MOS65XX_INS_ENDING = 97

MOS65XX_GRP_INVALID = 0
MOS65XX_GRP_JUMP = 1
MOS65XX_GRP_CALL = 2
MOS65XX_GRP_RET = 3
MOS65XX_GRP_INT = 4
MOS65XX_GRP_IRET = 5
MOS65XX_GRP_BRANCH_RELATIVE = 6
MOS65XX_GRP_ENDING = 7

MOS65XX_OP_INVALID = 0
MOS65XX_OP_REG = 1
MOS65XX_OP_IMM = 2
MOS65XX_OP_MEM = 3

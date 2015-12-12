#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.1.0"

__copyright__ = """
    pyObjUtils - Object file library for Python.

   (C) 2010-2015 by Christoph Schueler <cpu12.gems@googlemail.com>

   All Rights Reserved

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License along
  with this program; if not, write to the Free Software Foundation, Inc.,
  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import enum
from collections import namedtuple
import mmap
import os
import sys
import types
import struct


#
#   Reference:
#   ----------
#   Tool Interface Standard (TIS): Executable and Linking Format (ELF) Specification Version 1.2
#


##
##
##   ELF Header.
##
##

ELF_MAGIC = '\x7fELF'

EI_NIDENT = 16        # Size of e_ident[].

HDR_FMT32 = "B" * EI_NIDENT + "HHIIIIIHHHHHH"

ELF_HEADER_SIZE32 = struct.calcsize(HDR_FMT32)

assert(struct.calcsize(HDR_FMT32) == 52)    # todo: Unittest!!!

Elf32_Ehdr = namedtuple("Elf32_Ehdr", """e_ident0 e_ident1 e_ident2 e_ident3 e_ident4 e_ident5 e_ident6
    e_ident7 e_ident8 e_ident9 e_ident10 e_ident11 e_ident12 e_ident13 e_ident14 e_ident15
    e_type e_machine e_version e_entry e_phoff e_shoff e_flags e_ehsize e_phentsize e_phnum
    e_shentsize e_shnum e_shstrndx""")

class ELFType(enum.IntEnum):
    ET_NONE     = 0
    " No file type."
    ET_REL      = 1
    " Relocatable file."
    ET_EXEC     = 2
    " Executable file."
    ET_DYN      = 3
    " Shared object file."
    ET_CORE     = 4
    " Core file."
    ET_NUM      = 5
    "Number of defined types "
    ET_LOOS     = 0xFE00
    "Operating system-specific "
    ET_HIOS     = 0xFEFF
    "Operating system-specific "
    ET_LOPROC   = 0xff00
    " Processor-specific."
    ET_HIPROC   = 0xffff
    "Processor-specific."


ELF_TYPE_NAMES = {
    ELFType.ET_NONE : "No file type.",
    ELFType.ET_REL  : "Relocatable file.",
    ELFType.ET_EXEC : "Executable file.",
    ELFType.ET_DYN  : "Shared object file.",
    ELFType.ET_CORE : "Core file."
}


class ELFMachineType(enum.IntEnum):
    EM_NONE         =  0      # No machine.
    EM_M32          =  1      # AT&T WE 32100.
    EM_SPARC        =  2      # SPARC.
    EM_386          =  3      # Intel 80386.
    EM_68K          =  4      # Motorola 68000.
    EM_88K          =  5      # Motorola 88000.

    '''
    RESERVED 6 Reserved for future use
    '''

    EM_860          =  7      # Intel 80860.
    EM_MIPS         =  8      # MIPS I Architecture.
    EM_S370         =  9      # IBM System/370 Processor.
    EM_MIPS_RS3_LE  =  10     # MIPS RS3000 Little-endian.

    '''
    RESERVED 11-14 Reserved for future use
    '''

    EM_PARISC       =  15     # Hewlett-Packard PA-RISC.
    RESERVED        =  16     # Reserved for future use.
    EM_VPP500       =  17     # Fujitsu VPP500.
    EM_SPARC32PLUS  =  18     # Enhanced instruction set SPARC.
    EM_960          =  19     # Intel 80960.
    EM_PPC          =  20     # PowerPC.
    EM_PPC64        =  21     # 64-bit PowerPC.
    EM_S390         =  22     # IBM S390.
    EM_SPU          =  23     # Sony/Toshiba/IBM SPU.

    '''
    RESERVED 24-35 Reserved for future use
    '''

    EM_V800         =  36     # NEC V800.
    EM_FR20         =  37     # Fujitsu FR20.
    EM_RH32         =  38     # TRW RH-32.
    EM_RCE          =  39     # Motorola RCE.
    EM_ARM          =  40     # Advanced RISC Machines ARM.
    EM_ALPHA        =  41     # Digital Alpha.
    EM_SH           =  42     # Hitachi SH.
    EM_SPARCV9      =  43     # SPARC Version 9.
    EM_TRICORE      =  44     # Siemens Tricore embedded processor.
    EM_ARC          =  45     # Argonaut RISC Core, Argonaut Technologies Inc.
    EM_H8_300       =  46     # Hitachi H8/300.
    EM_H8_300H      =  47     # Hitachi H8/300H.
    EM_H8S          =  48     # Hitachi H8S.
    EM_H8_500       =  49     # Hitachi H8/500.
    EM_IA_64        =  50     # Intel IA-64 processor architecture.
    EM_MIPS_X       =  51     # Stanford MIPS-X.
    EM_COLDFIRE     =  52     # Motorola ColdFire.
    EM_68HC12       =  53     # Motorola M68HC12.    # could also be 0x4D12 (s. HC12EABI)
    EM_MMA          =  54     # Fujitsu MMA Multimedia Accelerator.
    EM_PCP          =  55     # Siemens PCP.
    EM_NCPU         =  56     # Sony nCPU embedded RISC processor.
    EM_NDR1         =  57     # Denso NDR1 microprocessor.
    EM_STARCORE     =  58     # Motorola Star*Core processor.
    EM_ME16         =  59     # Toyota ME16 processor.
    EM_ST100        =  60     # STMicroelectronics ST100 processor.
    EM_TINYJ        =  61     # Advanced Logic Corp. TinyJ embedded processor family.
    EM_X8664        =  62     # AMD x86-64 architecture.
    EM_PDSP         =  63     # Sony DSP Processor.
    EM_PDP10        =  64     # DEC PDP-10
    EM_PDP11        =  65     # DEC PDP-11
    EM_FX66         =  66     # Siemens FX66 microcontroller.
    EM_ST9PLUS      =  67     # STMicroelectronics ST9+ 8/16 bit microcontroller.
    EM_ST7          =  68     # STMicroelectronics ST7 8-bit microcontroller.
    EM_68HC16       =  69     # Motorola MC68HC16 Microcontroller.
    EM_68HC11       =  70     # Motorola MC68HC11 Microcontroller.
    EM_68HC08       =  71     # Motorola MC68HC08 Microcontroller.
    EM_68HC05       =  72     # Motorola MC68HC05 Microcontroller.
    EM_SVX          =  73     # Silicon Graphics SVx.
    EM_ST19         =  74     # STMicroelectronics ST19 8-bit microcontroller.
    EM_VAX          =  75     # Digital VAX.
    EM_CRIS         =  76     # Axis Communications 32-bit embedded processor.
    EM_JAVELIN      =  77     # Infineon Technologies 32-bit embedded processor.
    EM_FIREPATH     =  78     # Element 14 64-bit DSP Processor.
    EM_ZSP          =  79     # LSI Logic 16-bit DSP Processor.
    EM_MMIX         =  80     # Donald Knuth's educational 64-bit processor.
    EM_HUANY        =  81     # Harvard University machine-independent object files .
    EM_PRISM        =  82     # SiTera Prism.
    EM_AVR          =  83     # Atmel AVR 8-bit microcontroller.
    EM_FR30         =  84     # Fujitsu FR30.
    EM_D10V         =  85     # Mitsubishi D10V.
    EM_D30V         =  86     # Mitsubishi D30V.
    EM_V850         =  87     # NEC v850.
    EM_M32R         =  88     # Mitsubishi M32R.
    EM_MN10300      =  89     # Matsushita MN10300.
    EM_MN10200      =  90     # Matsushita MN10200.
    EM_PJ           =  91     # picoJava.
    EM_OPENRISC     =  92     # OpenRISC 32-bit embedded processor.
    EM_ARC_A5       =  93     # ARC Cores Tangent-A5.
    EM_XTENSA       =  94     # Tensilica Xtensa Architecture.
    EM_VIDEOCORE    =  95     # Alphamosaic VideoCore processor.
    EM_TMM_GPP      =  96     # Thompson Multimedia General Purpose Processor.
    EM_NS32K        =  97     # National Semiconductor 32000 series.
    EM_TPC          =  98     # Tenor Network TPC processor.
    EM_SNP1K        =  99     # Trebia SNP 1000 processor.
    EM_ST200        = 100     # STMicroelectronics ST200 microcontroller.
    EM_IP2K         = 101     # Ubicom IP2022 micro controller.
    EM_MAX          = 102     # MAX Processor.
    EM_CR           = 103     # National Semiconductor CompactRISC.
    EM_F2MC16       = 104     # Fujitsu F2MC16.
    EM_MSP430       = 105     # TI msp430 micro controller.
    EM_BLACKFIN     = 106     # ADI Blackfin.
    EM_SE_C33       = 107     # S1C33 Family of Seiko Epson processors.
    EM_SEP          = 108     # Sharp embedded microprocessor.
    EM_ARCA         = 109     # Arca RISC Microprocessor.
    EM_UNICORE      = 110     # Microprocessor series from PKU-Unity Ltd. and MPRC of Peking University.
    EM_EXCESS       = 111     # eXcess: 16/32/64-bit configurable embedded CPU.
    EM_DXP          = 112     # Icera Semiconductor Inc. Deep Execution Processor.
    EM_ALTERA_NIOS2 = 113     # Altera Nios II soft-core processor.
    EM_CRX          = 114     # National Semiconductor CRX.
    EM_XGATE        = 115     # Motorola XGATE embedded processor.
    EM_C166         = 116     # Infineon C16x/XC16x processor.
    EM_M16C         = 117     # Renesas M16C series microprocessors.
    EM_DSPIC30F     = 118     # Microchip Technology dsPIC30F Digital Signal Controller.
    EM_CE           = 119     # Freescale Communication Engine RISC core.
    EM_M32C         = 120     # Renesas M32C series microprocessors.
    EM_TSK3000      = 131     # Altium TSK3000 core.
    EM_RS08         = 132     # Freescale RS08 embedded processor.
    EM_ECOG2        = 134     # Cyan Technology eCOG2 microprocessor.
    EM_SCORE        = 135     # Sunplus Score.
    EM_SCORE7       = 135     # Sunplus S+core7 RISC processor.
    EM_DSP24        = 136     # New Japan Radio (NJR) 24-bit DSP Processor.
    EM_VIDEOCORE3   = 137     # Broadcom VideoCore III processor.
    EM_LATTICEMICO32= 138     # RISC processor for Lattice FPGA architecture.
    EM_SE_C17       = 139     # Seiko Epson C17 family.
    EM_TI_C6000     = 140     # Texas Instruments TMS320C6000 DSP family.
    EM_TI_C2000     = 141     # Texas Instruments TMS320C2000 DSP family.
    EM_TI_C5500     = 142     # Texas Instruments TMS320C55x DSP family.
    EM_MMDSP_PLUS   = 160     # STMicroelectronics 64bit VLIW Data Signal Processor.
    EM_CYPRESS_M8C  = 161     # Cypress M8C microprocessor.
    EM_R32C         = 162     # Renesas R32C series microprocessors.
    EM_TRIMEDIA     = 163     # NXP Semiconductors TriMedia architecture family.
    EM_QDSP6        = 164     # QUALCOMM DSP6 Processor.
    EM_I8051        = 165     # Intel 8051 and variants.
    EM_STXP7X       = 166     # STMicroelectronics STxP7x family.
    EM_NDS32        = 167     # Andes Technology compact code size embedded RISC processor family.
    EM_ECOG1        = 168     # Cyan Technology eCOG1X family.
    EM_ECOG1X       = 168     # Cyan Technology eCOG1X family.
    EM_MAXQ30       = 169     # Dallas Semiconductor MAXQ30 Core Micro-controllers.
    EM_XIMO16       = 170     # New Japan Radio (NJR) 16-bit DSP Processor.
    EM_MANIK        = 171     # M2000 Reconfigurable RISC Microprocessor.
    EM_CRAYNV2      = 172     # Cray Inc. NV2 vector architecture.
    EM_RX           = 173     # Renesas RX family.
    EM_METAG        = 174     # Imagination Technologies META processor architecture.
    EM_MCST_ELBRUS  = 175     # MCST Elbrus general purpose hardware architecture.
    EM_ECOG16       = 176     # Cyan Technology eCOG16 family.
    EM_CR16         = 177     # National Semiconductor CompactRISC 16-bit processor.
    EM_ETPU         = 178     # Freescale Extended Time Processing Unit.
    EM_SLE9X        = 179     # Infineon Technologies SLE9X core.
    EM_L1OM         = 180     # Intel L1OM.
    EM_AVR32        = 185     # Atmel Corporation 32-bit microprocessor family.
    EM_STM8         = 186     # STMicroeletronics STM8 8-bit microcontroller.
    EM_TILE64       = 187     # Tilera TILE64 multicore architecture family.
    EM_TILEPRO      = 188     # Tilera TILEPro multicore architecture family.
    EM_MICROBLAZE   = 189     # Xilinx MicroBlaze 32-bit RISC soft processor core.
    EM_CUDA         = 190     # NVIDIA CUDA architecture.
    EM_AVR_OLD              = 0x1057  # AVR magic number.  Written in the absense of an ABI.
    EM_MSP430_OLD           = 0x1059  # MSP430 magic number.  Written in the absense of everything.
    EM_MT                   = 0x2530  # Morpho MT.   Written in the absense of an ABI.
    EM_CYGNUS_FR30          = 0x3330  # FR30 magic number - no EABI available.
    EM_OPENRISC_OLD         = 0x3426  # OpenRISC magic number.  Written in the absense of an ABI.
    EM_DLX                  = 0x5aa5  # DLX magic number.  Written in the absense of an ABI.
    EM_CYGNUS_FRV           = 0x5441  # FRV magic number - no EABI available??.
    EM_XC16X                = 0x4688  # Infineon Technologies 16-bit microcontroller with C166-V2 core.
    EM_CYGNUS_D10V          = 0x7650  # D10V backend magic number.  Written in the absence of an ABI.
    EM_CYGNUS_D30V          = 0x7676  # D30V backend magic number.  Written in the absence of an ABI.
    EM_IP2K_OLD             = 0x8217  # Ubicom IP2xxx;   Written in the absense of an ABI.
    EM_OR32                 = 0x8472  # (Deprecated) Temporary number for the OpenRISC processor.
    EM_CYGNUS_POWERPC       = 0x9025  # Cygnus PowerPC ELF backend.  Written in the absence of an ABI.
    EM_ALPHA                = 0x9026  # Alpha backend magic number.  Written in the absence of an ABI.
    EM_CYGNUS_M32R          = 0x9041  # Cygnus M32R ELF backend.  Written in the absence of an ABI.
    EM_CYGNUS_V850          = 0x9080  # V850 backend magic number.  Written in the absense of an ABI.
    EM_S390_OLD             = 0xa390  # old S/390 backend magic number. Written in the absence of an ABI.
    EM_XTENSA_OLD           = 0xabc7  # Old, unofficial value for Xtensa.
    EM_XSTORMY16            = 0xad45
    EM_CYGNUS_MN10300       = 0xbeef  # mn10200 and mn10300 backend magic numbers. Written in the absense of an ABI.
    EM_CYGNUS_MN10200       = 0xdead
    EM_M32C_OLD             = 0xFEB0  # Renesas M32C and M16C.
    EM_IQ2000               = 0xFEBA  # Vitesse IQ2000.
    EM_NIOS32               = 0xFEBB  # NIOS magic number - no EABI available.
    EM_CYGNUS_MEP           = 0xF00D  # Toshiba MeP
    EM_MOXIE                = 0xFEED  # Moxie
    EM_MICROBLAZE_OLD       = 0xbaab  # Old MicroBlaze
    EM_ADAPTEVA_EPIPHANY    = 0x1223  # Adapteva's Epiphany architecture.


ELF_MACHINE_NAMES = {
    ELFMachineType.EM_NONE          : "No machine.",
    ELFMachineType.EM_M32           : "AT&T WE 32100.",
    ELFMachineType.EM_SPARC         : "SPARC.",
    ELFMachineType.EM_386           : "Intel 80386.",
    ELFMachineType.EM_68K           : "Motorola 68000.",
    ELFMachineType.EM_88K           : "Motorola 88000.",
    ELFMachineType.EM_860           : "Intel 80860.",
    ELFMachineType.EM_MIPS          : "MIPS I Architecture.",
    ELFMachineType.EM_S370          : "IBM System/370 Processor.",
    ELFMachineType.EM_MIPS_RS3_LE   : "MIPS RS3000 Little-endian.",
    ELFMachineType.EM_PARISC        : "Hewlett-Packard PA-RISC.",
    ELFMachineType.RESERVED         : "Reserved for future use.",
    ELFMachineType.EM_VPP500        : "Fujitsu VPP500.",
    ELFMachineType.EM_SPARC32PLUS   : "Enhanced instruction set SPARC.",
    ELFMachineType.EM_960           : "Intel 80960.",
    ELFMachineType.EM_PPC           : "PowerPC.",
    ELFMachineType.EM_PPC64         : "64-bit PowerPC.",
    ELFMachineType.EM_S390          : "IBM S390.",
    ELFMachineType.EM_SPU           : "Sony/Toshiba/IBM SPU.",
    ELFMachineType.EM_V800          : "NEC V800.",
    ELFMachineType.EM_FR20          : "Fujitsu FR20.",
    ELFMachineType.EM_RH32          : "TRW RH-32.",
    ELFMachineType.EM_RCE           : "Motorola RCE.",
    ELFMachineType.EM_ARM           : "ARM",
    ELFMachineType.EM_ALPHA         : "Digital Alpha.",
    ELFMachineType.EM_SH            : "Hitachi SH.",
    ELFMachineType.EM_SPARCV9       : "SPARC Version 9.",
    ELFMachineType.EM_TRICORE       : "Siemens Tricore embedded processor.",
    ELFMachineType.EM_ARC           : "Argonaut RISC Core, Argonaut Technologies Inc.",
    ELFMachineType.EM_H8_300        : "Hitachi H8/300.",
    ELFMachineType.EM_H8_300H       : "Hitachi H8/300H.",
    ELFMachineType.EM_H8S           : "Hitachi H8S.",
    ELFMachineType.EM_H8_500        : "Hitachi H8/500.",
    ELFMachineType.EM_IA_64         : "Intel IA-64 processor architecture.",
    ELFMachineType.EM_MIPS_X        : "Stanford MIPS-X.",
    ELFMachineType.EM_COLDFIRE      : "Motorola ColdFire.",
    ELFMachineType.EM_68HC12        : "Motorola M68HC12.",
    ELFMachineType.EM_MMA           : "Fujitsu MMA Multimedia Accelerator.",
    ELFMachineType.EM_PCP           : "Siemens PCP.",
    ELFMachineType.EM_NCPU          : "Sony nCPU embedded RISC processor.",
    ELFMachineType.EM_NDR1          : "Denso NDR1 microprocessor.",
    ELFMachineType.EM_STARCORE      : "Motorola Star*Core processor.",
    ELFMachineType.EM_ME16          : "Toyota ME16 processor.",
    ELFMachineType.EM_ST100         : "STMicroelectronics ST100 processor.",
    ELFMachineType.EM_TINYJ         : "Advanced Logic Corp. TinyJ embedded processor family.",
    ELFMachineType.EM_X8664         : "AMD x86-64 architecture.",
    ELFMachineType.EM_PDSP          : "Sony DSP Processor.",
    ELFMachineType.EM_PDP10         : "DEC PDP-10",
    ELFMachineType.EM_PDP11         : "DEC PDP-11",
    ELFMachineType.EM_FX66          : "Siemens FX66 microcontroller.",
    ELFMachineType.EM_ST9PLUS       : "STMicroelectronics ST9+ 8/16 bit microcontroller.",
    ELFMachineType.EM_ST7           : "STMicroelectronics ST7 8-bit microcontroller.",
    ELFMachineType.EM_68HC16        : "Motorola MC68HC16 Microcontroller.",
    ELFMachineType.EM_68HC11        : "Motorola MC68HC11 Microcontroller.",
    ELFMachineType.EM_68HC08        : "Motorola MC68HC08 Microcontroller.",
    ELFMachineType.EM_68HC05        : "Motorola MC68HC05 Microcontroller.",
    ELFMachineType.EM_SVX           : "Silicon Graphics SVx.",
    ELFMachineType.EM_ST19          : "STMicroelectronics ST19 8-bit microcontroller.",
    ELFMachineType.EM_VAX           : "Digital VAX.",
    ELFMachineType.EM_CRIS          : "Axis Communications 32-bit embedded processor.",
    ELFMachineType.EM_JAVELIN       : "Infineon Technologies 32-bit embedded processor.",
    ELFMachineType.EM_FIREPATH      : "Element 14 64-bit DSP Processor.",
    ELFMachineType.EM_ZSP           : "LSI Logic 16-bit DSP Processor.",
    ELFMachineType.EM_MMIX          : "Donald Knuth's educational 64-bit processor.",
    ELFMachineType.EM_HUANY         : "Harvard University machine-independent object files .",
    ELFMachineType.EM_PRISM         : "SiTera Prism.",
    ELFMachineType.EM_AVR           : 'Atmel AVR 8-bit microcontroller',
    ELFMachineType.EM_FR30          : 'Fujitsu FR30',
    ELFMachineType.EM_D10V          : 'Mitsubishi D10V',
    ELFMachineType.EM_D30V          : 'Mitsubishi D30V',
    ELFMachineType.EM_V850          : 'NEC v850',
    ELFMachineType.EM_M32R          : 'Mitsubishi M32R',
    ELFMachineType.EM_MN10300       : 'Matsushita MN10300',
    ELFMachineType.EM_MN10200       : 'Matsushita MN10200',
    ELFMachineType.EM_PJ            : 'picoJava',
    ELFMachineType.EM_OPENRISC      : 'OpenRISC 32-bit embedded processor.',
    ELFMachineType.EM_ARC_A5        : 'ARC Cores Tangent-A5.',
    ELFMachineType.EM_XTENSA        : 'Tensilica Xtensa Architecture.',
    ELFMachineType.EM_VIDEOCORE     : 'Alphamosaic VideoCore processor.',
    ELFMachineType.EM_TMM_GPP       : 'Thompson Multimedia General Purpose Processor.',
    ELFMachineType.EM_NS32K         : 'National Semiconductor 32000 series.',
    ELFMachineType.EM_TPC           : 'Tenor Network TPC processor.',
    ELFMachineType.EM_SNP1K         : 'Trebia SNP 1000 processor.',
    ELFMachineType.EM_ST200         : 'STMicroelectronics ST200 microcontroller.',
    ELFMachineType.EM_IP2K          : 'Ubicom IP2022 micro controller.',
    ELFMachineType.EM_MAX           : 'MAX Processor.',
    ELFMachineType.EM_CR            : 'National Semiconductor CompactRISC.',
    ELFMachineType.EM_F2MC16        : 'Fujitsu F2MC16.',
    ELFMachineType.EM_MSP430        : 'TI msp430 micro controller.',
    ELFMachineType.EM_BLACKFIN      : 'ADI Blackfin.',
    ELFMachineType.EM_SE_C33        : 'S1C33 Family of Seiko Epson processors.',
    ELFMachineType.EM_SEP           : 'Sharp embedded microprocessor.',
    ELFMachineType.EM_ARCA          : 'Arca RISC Microprocessor.',
    ELFMachineType.EM_UNICORE       : 'Microprocessor series from PKU-Unity Ltd. and MPRC of Peking University.',
    ELFMachineType.EM_EXCESS        : 'eXcess: 16/32/64-bit configurable embedded CPU.',
    ELFMachineType.EM_DXP           : 'Icera Semiconductor Inc. Deep Execution Processor.',
    ELFMachineType.EM_ALTERA_NIOS2  : 'Altera Nios II soft-core processor.',
    ELFMachineType.EM_CRX           : 'National Semiconductor CRX.',
    ELFMachineType.EM_XGATE         : 'Motorola XGATE embedded processor.',
    ELFMachineType.EM_C166          : 'Infineon C16x/XC16x processor.',
    ELFMachineType.EM_M16C          : 'Renesas M16C series microprocessors.',
    ELFMachineType.EM_DSPIC30F      : 'Microchip Technology dsPIC30F Digital Signal Controller.',
    ELFMachineType.EM_CE            : 'Freescale Communication Engine RISC core.',
    ELFMachineType.EM_M32C          : 'Renesas M32C series microprocessors.',
    ELFMachineType.EM_TSK3000       : 'Altium TSK3000 core.',
    ELFMachineType.EM_RS08          : 'Freescale RS08 embedded processor.',
    ELFMachineType.EM_ECOG2         : 'Cyan Technology eCOG2 microprocessor.',
    ELFMachineType.EM_SCORE         : 'Sunplus Score.',
    ELFMachineType.EM_SCORE7        : 'Sunplus S+core7 RISC processor.',
    ELFMachineType.EM_DSP24         : 'New Japan Radio (NJR) 24-bit DSP Processor.',
    ELFMachineType.EM_VIDEOCORE3    : 'Broadcom VideoCore III processor.',
    ELFMachineType.EM_LATTICEMICO32 : 'RISC processor for Lattice FPGA architecture.',
    ELFMachineType.EM_SE_C17        : 'Seiko Epson C17 family.',
    ELFMachineType.EM_TI_C6000      : 'Texas Instruments TMS320C6000 DSP family.',
    ELFMachineType.EM_TI_C2000      : 'Texas Instruments TMS320C2000 DSP family.',
    ELFMachineType.EM_TI_C5500      : 'Texas Instruments TMS320C55x DSP family.',
    ELFMachineType.EM_MMDSP_PLUS    : 'STMicroelectronics 64bit VLIW Data Signal Processor.',
    ELFMachineType.EM_CYPRESS_M8C   : 'Cypress M8C microprocessor.',
    ELFMachineType.EM_R32C          : 'Renesas R32C series microprocessors.',
    ELFMachineType.EM_TRIMEDIA      : 'NXP Semiconductors TriMedia architecture family.',
    ELFMachineType.EM_QDSP6         : 'QUALCOMM DSP6 Processor.',
    ELFMachineType.EM_I8051         : 'Intel 8051 and variants.',
    ELFMachineType.EM_STXP7X        : 'STMicroelectronics STxP7x family.',
    ELFMachineType.EM_NDS32         : 'Andes Technology compact code size embedded RISC processor family.',
    ELFMachineType.EM_ECOG1         : 'Cyan Technology eCOG1X family.',
    ELFMachineType.EM_ECOG1X        : 'Cyan Technology eCOG1X family.',
    ELFMachineType.EM_MAXQ30        : 'Dallas Semiconductor MAXQ30 Core Micro-controllers.',
    ELFMachineType.EM_XIMO16        : 'New Japan Radio (NJR) 16-bit DSP Processor.',
    ELFMachineType.EM_MANIK         : 'M2000 Reconfigurable RISC Microprocessor.',
    ELFMachineType.EM_CRAYNV2       : 'Cray Inc. NV2 vector architecture.',
    ELFMachineType.EM_RX            : 'Renesas RX family.',
    ELFMachineType.EM_METAG         : 'Imagination Technologies META processor architecture.',
    ELFMachineType.EM_MCST_ELBRUS   : 'MCST Elbrus general purpose hardware architecture.',
    ELFMachineType.EM_ECOG16        : 'Cyan Technology eCOG16 family.',
    ELFMachineType.EM_CR16          : 'National Semiconductor CompactRISC 16-bit processor.',
    ELFMachineType.EM_ETPU          : 'Freescale Extended Time Processing Unit.',
    ELFMachineType.EM_SLE9X         : 'Infineon Technologies SLE9X core.',
    ELFMachineType.EM_L1OM          : 'Intel L1OM.',
    ELFMachineType.EM_AVR32         : 'Atmel Corporation 32-bit microprocessor family.',
    ELFMachineType.EM_STM8          : 'STMicroeletronics STM8 8-bit microcontroller.',
    ELFMachineType.EM_TILE64        : 'Tilera TILE64 multicore architecture family.',
    ELFMachineType.EM_TILEPRO       : 'Tilera TILEPro multicore architecture family.',
    ELFMachineType.EM_MICROBLAZE    : 'Xilinx MicroBlaze 32-bit RISC soft processor core.',
    ELFMachineType.EM_CUDA          : 'NVIDIA CUDA architecture.',
    ELFMachineType.EM_AVR_OLD       : 'AVR',
    ELFMachineType.EM_MSP430_OLD    : 'MSP430',
    ELFMachineType.EM_MT            : 'Morpho MT',
    ELFMachineType.EM_CYGNUS_FR30   : 'Cygnus FR30',
    ELFMachineType.EM_OPENRISC_OLD  : 'OpenRISC',
    ELFMachineType.EM_DLX           : 'DLX',
    ELFMachineType.EM_CYGNUS_FRV    : 'Cygnus FRV',
    ELFMachineType.EM_XC16X         : 'Infineon C166-V2 core.',
    ELFMachineType.EM_CYGNUS_D10V   : 'Cygnus D10V',
    ELFMachineType.EM_CYGNUS_D30V   : 'Cygnus D30V',
    ELFMachineType.EM_IP2K_OLD      : 'Ubicom IP2xxx',
    ELFMachineType.EM_OR32          : 'OpenRISC 32',
    ELFMachineType.EM_CYGNUS_POWERPC: 'Cygnus PowerPC',
    ELFMachineType.EM_ALPHA         : 'Alpha',
    ELFMachineType.EM_CYGNUS_M32R   : 'Cygnus M32R',
    ELFMachineType.EM_CYGNUS_V850   : 'Cygnus V850',
    ELFMachineType.EM_S390_OLD      : 'S/390',
    ELFMachineType.EM_XTENSA_OLD    : 'Xtensa',
    ELFMachineType.EM_XSTORMY16     : 'Xstormy16',
    ELFMachineType.EM_CYGNUS_MN10300: 'Cygnus mn10200 or mn10300',
    ELFMachineType.EM_CYGNUS_MN10200: 'Cygnus mn10200',
    ELFMachineType.EM_M32C_OLD      : 'Renesas M32C or M16C.',
    ELFMachineType.EM_IQ2000        : 'Vitesse IQ2000.',
    ELFMachineType.EM_NIOS32        : 'NIOS',
    ELFMachineType.EM_CYGNUS_MEP    : 'Toshiba MeP',
    ELFMachineType.EM_MOXIE         : 'Moxie',
    ELFMachineType.EM_MICROBLAZE_OLD: 'Old MicroBlaze',
    ELFMachineType.EM_ADAPTEVA_EPIPHANY : "Adapteva Epiphany",
}


EV_NONE         = 0      # Invalid version.
EV_CURRENT      = 1      # Current version.


##
## Offsets into file header.
##
EI_MAG0         = 0      # File identification.
EI_MAG1         = 1      # File identification.
EI_MAG2         = 2      # File identification.
EI_MAG3         = 3      # File identification.
EI_CLASS        = 4      # File class.
EI_DATA         = 5      # Data encoding.
EI_VERSION      = 6      # File version.
EI_PAD          = 7      # Start of padding bytes.
EI_OSABI        = 7      # Operating system/ABI identification.
EI_ABIVERSION   = 8      # ABI version.
# EI_NIDENT       = 16     # Size of e_ident[] - defined above.


class ELFClass(enum.IntEnum):
    ELFCLASSNONE    = 0      # Invalid class.
    ELFCLASS32      = 1      # 32-bit objects.
    ELFCLASS64      = 2      # 64-bit objects.


ELF_CLASS_NAMES = {
    ELFClass.ELFCLASSNONE   : "Invalid class.",
    ELFClass.ELFCLASS32     : "32-bit objects.",
    ELFClass.ELFCLASS64     : "64-bit objects."
}


class ELFDataEncoding(enum.IntEnum):
    ELFDATANONE     = 0      # Invalid data encoding.
    ELFDATA2LSB     = 1      # Little-Endian.
    ELFDATA2MSB     = 2      # Big-Endian.


ELF_BYTE_ORDER_NAMES = {
    ELFDataEncoding.ELFDATANONE : "Invalid data encoding.",
    ELFDataEncoding.ELFDATA2LSB : "Little-Endian.",
    ELFDataEncoding.ELFDATA2MSB : "Big-Endian."
}

class ELFAbiType(enum.IntEnum):
    ELFOSABI_NONE         = 0   # UNIX System V ABI
    ELFOSABI_HPUX         = 1   # HP-UX operating system
    ELFOSABI_NETBSD       = 2   # NetBSD
    ELFOSABI_GNU          = 3   # GNU
    ELFOSABI_LINUX        = 3   # Alias for ELFOSABI_GNU
    ELFOSABI_SOLARIS      = 6   # Solaris
    ELFOSABI_AIX          = 7   # AIX
    ELFOSABI_IRIX         = 8   # IRIX
    ELFOSABI_FREEBSD      = 9   # FreeBSD
    ELFOSABI_TRU64        = 10  # TRU64 UNIX
    ELFOSABI_MODESTO      = 11  # Novell Modesto
    ELFOSABI_OPENBSD      = 12  # OpenBSD
    ELFOSABI_OPENVMS      = 13  # OpenVMS
    ELFOSABI_NSK          = 14  # Hewlett-Packard Non-Stop Kernel
    ELFOSABI_AROS         = 15  # AROS
    ELFOSABI_FENIXOS      = 16  # FenixOS
    ELFOSABI_C6000_ELFABI = 64  # Bare-metal TMS320C6000; alt:  ELFOSABI_ARM_AEABI
    ELFOSABI_C6000_LINUX  = 65  # Linux TMS320C6000
    ELFOSABI_ARM          = 97  # ARM
    ELFOSABI_STANDALONE   = 255 # Standalone (embedded) application

##
##
##   ELF Sections.
##
##

SEC_FMT32 = "IIIIIIIIII"

ELF_SECTION_SIZE32 = struct.calcsize(SEC_FMT32)

Elf32_Shdr = namedtuple("Elf32_Shdr", """sh_name sh_type sh_flags sh_addr sh_offset sh_size
    sh_link sh_info sh_addralign sh_entsize"""
)


# Section Indices.
SHN_UNDEF       = 0
    # SHN_UNDEF This value marks an undefined, missing, irrelevant, or otherwise
    # meaningless section reference. For example, a symbol "defined'' relative to
    # section number SHN_UNDEF is an undefined symbol.

SHN_LORESERVE   = 0xff00
    # This value specifies the lower bound of the range of reserved indexes
SHN_LOPROC      = 0xff00
SHN_HIPROC      = 0xff1f
    # SHN_LOPROC through SHN_HIPROC: Values in this inclusive range are reserved for
    # processor-specific semantics.
SHN_ABS         = 0xfff1
    # SHN_ABS This value specifies absolute values for the corresponding reference. For
    # example, symbols defined relative to section number SHN_ABS have
    # absolute values and are not affected by relocation.
SHN_COMMON      = 0xfff2
    # SHN_COMMON Symbols defined relative to this section are common symbols, such as
    # FORTRAN COMMON or unallocated C external variables.
SHN_XINDEX      = 0xffff
    # Index is in extra table.
SHN_HIRESERVE   = 0xffff
    # SHN_HIRESERVE This value specifies the upper bound of the range of reserved indexes.
    # The system reserves indexes between SHN_LORESERVE and SHN_HIRESERVE, inclusive;
    # the values do not reference the section header table.That is, the section header
    # table does not contain entries for the  reserved indexes.


SHT_NULL            = 0             # Section header table entry unused.
SHT_PROGBITS        = 1             # Program data.
SHT_SYMTAB          = 2             # Symbol table.
SHT_STRTAB          = 3             # String table.
SHT_RELA            = 4             # Relocation entries with addends.
SHT_HASH            = 5             # Symbol hash table.
SHT_DYNAMIC         = 6             # Dynamic linking information.
SHT_NOTE            = 7             # Notes.
SHT_NOBITS          = 8             # Program space with no data (bss).
SHT_REL             = 9             # Relocation entries, no addends.
SHT_SHLIB           = 10            # Reserved.
SHT_DYNSYM          = 11            # Dynamic linker symbol table.
SHT_INIT_ARRAY      = 14            # Array of constructors.
SHT_FINI_ARRAY      = 15            # Array of destructors.
SHT_PREINIT_ARRAY   = 16            # Array of pre-constructors.
SHT_GROUP           = 17            # Section group.
SHT_SYMTAB_SHNDX    = 18            # Extended section indeces.
SHT_NUM             = 19            # Number of defined types.
SHT_LOOS            = 0x60000000    # Start OS-specific.
SHT_GNU_ATTRIBUTES  = 0x6ffffff5    # Object attributes.
SHT_GNU_HASH        = 0x6ffffff6    # GNU-style hash table.
SHT_GNU_LIBLIST     = 0x6ffffff7    # Prelink library list
SHT_CHECKSUM        = 0x6ffffff8    # Checksum for DSO content.
SHT_LOSUNW          = 0x6ffffffa    # Sun-specific low bound.
SHT_SUNW_move       = 0x6ffffffa
SHT_SUNW_COMDAT     = 0x6ffffffb
SHT_SUNW_syminfo    = 0x6ffffffc
SHT_GNU_verdef      = 0x6ffffffd    # Version definition section.
SHT_GNU_verneed     = 0x6ffffffe    # Version needs section.
SHT_GNU_versym      = 0x6fffffff    # Version symbol table.
SHT_HISUNW          = 0x6fffffff    # Sun-specific high bound.
SHT_HIOS            = 0x6fffffff    # End OS-specific type.
SHT_LOPROC          = 0x70000000    # Start of processor-specific.

SHT_ARM_EXIDX       = 0x70000001    # Section holds ARM unwind info.
SHT_ARM_PREEMPTMAP  = 0x70000002    # Section pre-emption details.
SHT_ARM_ATTRIBUTES  = 0x70000003    # Section holds attributes.
SHT_ARM_DEBUGOVERLAY    = 0x70000004    # Section holds overlay debug info.
SHT_ARM_OVERLAYSECTION  = 0x70000005    # Section holds GDB and overlay integration info.

SHT_HIPROC          = 0x7fffffff    # End of processor-specific.
SHT_LOUSER          = 0x80000000    # Start of application-specific.
SHT_HIUSER          = 0xffffffff    # End of application-specific.

SHF_WRITE               = 0x1           # Writable.
SHF_ALLOC               = 0x2           # Occupies memory during execution
SHF_EXECINSTR           = 0x4           # Executable.

SHF_MERGE               = 16            # Might be merged
SHF_STRINGS             = 32            # Contains nul-terminated strings
SHF_INFO_LINK           = 64            # `sh_info' contains SHT index
SHF_LINK_ORDER          = 128           # Preserve order after combining
SHF_OS_NONCONFORMING    = 256           # Non-standard OS specific handling required
SHF_GROUP               = 512           # Section is member of a group.
SHF_TLS                 = 1024          # Section hold thread-local data.
SHF_MASKOS              = 0x0ff00000    # OS-specific.

SHF_MASKPROC            = 0xf0000000    # Processor-specific.

SHF_ORDERED             = 1073741824L   # Special ordering requirement (Solaris).
SHF_EXCLUDE             = 2147483648L   # Section is excluded unless referenced or allocated (Solaris).

##
##
##   ELF Symbol Table.
##
##

SYMTAB_FMT = "IIIBBH"

Elf32_Sym = namedtuple("Elf32_Sym", "st_name st_value st_size st_info st_other st_shndx")

ELF_SYM_TABLE_SIZE = struct.calcsize(SYMTAB_FMT)

STN_UNDEF           = 0

STB_LOCAL           = 0
STB_GLOBAL          = 1
STB_WEAK            = 2
STB_LOPROC          = 13
STB_HIPROC          = 15


STT_NOTYPE          = 0
STT_OBJECT          = 1
STT_FUNC            = 2
STT_SECTION         = 3
STT_FILE            = 4
STT_LOPROC          = 13
STT_HIPROC          = 15


##
##
##   ELF Relocation.
##
##
REL_FMT = "II"

RELA_FMT = "IIi"

ELF_RELOCATION_SIZE     = struct.calcsize(REL_FMT)
ELF_RELOCATION_A_SIZE   = struct.calcsize(RELA_FMT)

Elf32_Rel   = namedtuple("Elf32_Rel", "r_offset r_info")
Elf32_Rela  = namedtuple("Elf32_Rela", "r_offset r_info r_addend")

##
##
##   ELF Program Header
##
##
PHDR_FMT32 = "IIIIIIII"

ELF_PHDR_SIZE32   = struct.calcsize(PHDR_FMT32)

Elf32_Phdr      = namedtuple("Elf32_Phdr", "p_type p_offset p_vaddr p_paddr p_filesz p_memsz p_flags p_align")


PT_NULL             = 0             # Program header table entry unused.
PT_LOAD             = 1             # Loadable program segment.
PT_DYNAMIC          = 2             # Dynamic linking information.
PT_INTERP           = 3             # Program interpreter.
PT_NOTE             = 4             # Auxiliary information.
PT_SHLIB            = 5             # Reserved.
PT_PHDR             = 6             # Entry for header table itself.
PT_TLS              = 7             # Thread-local storage segment
PT_NUM              = 8             # Number of defined types
PT_LOOS             = 0x60000000    # Start of OS-specific
PT_GNU_EH_FRAME     = 0x6474e550    # GCC .eh_frame_hdr segment
PT_GNU_STACK        = 0x6474e551    # Indicates stack executability
PT_GNU_RELRO        = 0x6474e552    # Read-only after relocation
PT_LOSUNW           = 0x6ffffffa
PT_SUNWBSS          = 0x6ffffffa    # Sun Specific segment
PT_SUNWSTACK        = 0x6ffffffb    # Stack segment
PT_HISUNW           = 0x6fffffff
PT_HIOS             = 0x6fffffff    # End of OS-specific
PT_LOPROC           = 0x70000000    # Start of processor-specific.
PT_HIPROC           = 0x7fffffff    # End of processor-specific


PF_X                = 0x1           # Execute.
PF_W                = 0x2           # Write.
PF_R                = 0x4           # Read.
PF_MASKPROC         = 0xf0000000    # Unspecified.

PN_XNUM             = 0xffff        # Extended numbering.


class Alias(object):
    # Install more convenient names.
    def __init__(self,key, convert = False):
        self.key = key
        self.convert = convert

    def __get__(self, obj, objtype = None):
        if obj is None:
            return self
        value = getattr(obj, self.key)
        return value

    def __set__(self, obj, value):
        data = getattr(obj, 'data')
        setattr(data, self.key,value)
        c = getattr(data, self.key)

    def __delete__(self, obj):
        raise AttributeError("can't delete attribute")


BYTEORDER_PREFIX = {
    ELFDataEncoding.ELFDATA2LSB : '<',  # Little-Endian.
    ELFDataEncoding.ELFDATA2MSB : '>'   # Big-Endian.
}


class FormatError(Exception): pass


class ELFHeader(object):
    def __init__(self, parent):
        self.parent = parent
        parent.inFile.seek(0, os.SEEK_SET)
        self.rawData = parent.inFile.read(ELF_HEADER_SIZE32)

        if self.rawData[ : 4] != ELF_MAGIC:
            raise FormatError("Not an ELF file - it has the wrong magic bytes at the start.")

        self.is64Bit = (self.rawData[EI_CLASS] ==  ELFClass.ELFCLASS64)
        self.byteOrderPrefix = BYTEORDER_PREFIX[ELFDataEncoding(ord(self.rawData[EI_DATA]))]

        elfHeader = struct.unpack("{0}{1}".format(self.byteOrderPrefix, HDR_FMT32), self.rawData)
        d = Elf32_Ehdr(*elfHeader)
        for name, value in d._asdict().items():
            setattr(self, name, value)

        if not (self.elfEHSize == ELF_HEADER_SIZE32):
            raise FormatError("Wrong header size.")
        if not (self.elfPHTEntrySize == ELF_PHDR_SIZE32):
            raise FormatError("Wrong p-header size.")
        if not (self.elfSHTEntrySize == ELF_SECTION_SIZE32):
            raise FormatError("Wrong section size.")

        self.hasStringTable = not (self.elfStringTableIndex == SHN_UNDEF)


    @property
    def elfTypeName(self):
        return ELF_TYPE_NAMES.get(ELFType(self.elfType), "Processor-specific.")

    @property
    def elfMachineName(self):
        return ELF_MACHINE_NAMES.get(ELFMachineType(self.elfMachine), "<unknown>")

    @property
    def elfClassName(self):
        return ELF_CLASS_NAMES.get(ELFClass(self.elfClass), "<unknown>")

    @property
    def elfByteOrderName(self):
        return ELF_BYTE_ORDER_NAMES.get(ELFDataEncoding(self.elfByteOrder), "<unknown>")

    # Install pretty names.
    elfClass                    = Alias("e_ident4")
    elfByteOrder                = Alias("e_ident5")
    elfVersion                  = Alias("e_ident6")
    elfOsAbi                    = Alias("e_ident7")
    elfAbiVersion               = Alias("e_ident8")
    elfType                     = Alias("e_type")
    elfMachine                  = Alias("e_machine")
    elfEntryPoint               = Alias("e_entry")
    elfProgramHeaderTableOffset = Alias("e_phoff")
    elfSectionHeaderTableOffset = Alias("e_shoff")
    elfFlags                    = Alias("e_flags")
    elfEHSize                   = Alias("e_ehsize")
    elfPHTEntrySize             = Alias("e_phentsize")
    elfNumberOfPHs              = Alias("e_phnum")
    elfSHTEntrySize             = Alias("e_shentsize")
    elfNumberOfSHs              = Alias("e_shnum")
    elfStringTableIndex         = Alias("e_shstrndx")

    def elfClassAsString(self):
        result = ""
        if self.elfClass == ELFClass.ELFCLASSNONE:
            result = "none"
        elif self.elfClass == ELFClass.ELFCLASS32:
            result = "ELF32"
        elif self.elfClass == ELFClass.ELFCLASS64:
            result = "ELF64"
        else:
            result = "<unknown: {0:x}>".format(self.elfClass)
        return result

    def elfDataEncodingAsString(self):
        result = ""
        if self.elfByteOrder == ELFDataEncoding.ELFDATANONE:
            result = "none"
        elif self.elfByteOrder == ELFDataEncoding.ELFDATA2LSB:
            result = "2's complement, little endian"
        elif self.elfByteOrder == ELFDataEncoding.ELFDATA2MSB:
            result = "2's complement, big endian"
        else:
            result = "<unknown: {0:x}>".format(self.elfByteOrder)
        return result

    def getVersionAsString(self):
        result = ""
        if self.elfVersion == EV_CURRENT:
            result = "(current)"
        elif self.elfVersion != EV_NONE:
            result = "<unknown: {0:lx}>".format(self.elfVersion)
        return result

    def getAbiNameAsString(self):
        result = ""
        if self.elfOsAbi == ELFAbiType.ELFOSABI_NONE:
            result = "UNIX - System V"
        elif self.elfOsAbi == ELFAbiType.ELFOSABI_HPUX:
            result = "UNIX - HP-UX"
        elif self.elfOsAbi == ELFAbiType.ELFOSABI_NETBSD:
            result = "UNIX - NetBSD"
        elif self.elfOsAbi == ELFAbiType.ELFOSABI_GNU:
            result = "UNIX - GNU"
        elif self.elfOsAbi == ELFAbiType.ELFOSABI_SOLARIS:
            result = "UNIX - Solaris"
        elif self.elfOsAbi == ELFAbiType.ELFOSABI_AIX:
            result = "UNIX - AIX"
        elif self.elfOsAbi == ELFAbiType.ELFOSABI_IRIX:
            result = "UNIX - IRIX"
        elif self.elfOsAbi == ELFAbiType.ELFOSABI_FREEBSD:
            result = "UNIX - FreeBSD"
        elif self.elfOsAbi == ELFAbiType.ELFOSABI_TRU64:
            result = "UNIX - TRU64"
        elif self.elfOsAbi == ELFAbiType.ELFOSABI_MODESTO:
            result = "Novell - Modesto"
        elif self.elfOsAbi == ELFAbiType.ELFOSABI_OPENBSD:
            result = "UNIX - OpenBSD"
        elif self.elfOsAbi == ELFAbiType.ELFOSABI_OPENVMS:
            result = "VMS - OpenVMS"
        elif self.elfOsAbi == ELFAbiType.ELFOSABI_NSK:
            result = "HP - Non-Stop Kernel"
        elif self.elfOsAbi == ELFAbiType.ELFOSABI_AROS:
            result = "AROS"
        elif self.elfOsAbi == ELFAbiType.ELFOSABI_FENIXOS:
            result = "FenixOS"
        elif self.elfOsAbi >= 64:
            if self.elfMachine == ELFMachineType.EM_ARM:
                if self.elfOsAbi == ELFAbiType.ELFOSABI_ARM:
                    result = "ARM"
            elif self.elfMachine in (ELFMachineType.EM_MSP430, ELFMachineType.EM_MSP430_OLD):
                if self.elfOsAbi == ELFAbiType.ELFOSABI_STANDALONE:
                    result = "Standalone App"
            elif self.elfMachine == ELFMachineType.EM_TI_C6000:
                if self.elfOsAbi == ELFAbiType.ELFOSABI_C6000_ELFABI:
                    result = "Bare-metal C6000"
                elif self.elfOsAbi == ELFAbiType.ELFOSABI_C6000_LINUX:
                    result = "Linux C6000"
        else:
            result = "<unknown: {0:x}>".format(self.elfOsAbi)
        return result


    def getElfTypeAsString(self):
        result = ""
        if self.elfType == ELFType.ET_NONE:
            result = "NONE (None)"
        elif self.elfType == ELFType.ET_REL:
            result = "REL (Relocatable file)"
        elif self.elfType == ELFType.ET_EXEC:
            result = "EXEC (Executable file)"
        elif self.elfType == ELFType.ET_DYN:
            result = "DYN (Shared object file)"
        elif self.elfType == ELFType.ET_CORE:
            result = "CORE (Core file)"
        else:
            if self.elfType >= ELFType.ET_LOPROC and self.elfType <= ELFType.ET_HIPROC:
                result = "Processor Specific: ({0:x})".format(self.elfType)
            elif self.elfType >= ELFType.ET_LOOS and self.elfType <= ELFType.ET_HIOS:
                result = "OS Specific: ({0:x})".format(self.elfType)
            else:
                result = "<unknown>: {0:x}".format(self.elfType)
        return result


class ELFSymbol(object):
    def __init__(self, parent, data):
        pass


class ELFSectionHeaderTable(object):
    def __init__(self, parent, atPosition=0):
        self.parent = parent
        self._name = None
        parent.inFile.seek(atPosition, os.SEEK_SET)
        data = parent.inFile.read(ELF_SECTION_SIZE32)

        elfProgramHeaderTable = struct.unpack("{0}{1}".format(parent.byteOrderPrefix, SEC_FMT32), data)
        d = Elf32_Shdr(*elfProgramHeaderTable)
        for name, value in d._asdict().items():
            setattr(self, name, value)

        #self.parent.sectionHeadersByName[name] = value

        if self.shType not in (SHT_NOBITS, SHT_NULL) and self.shSize > 0:
            pos = self.shOffset
            parent.inFile.seek(pos, os.SEEK_SET)
            self.image = parent.inFile.read(self.shSize)
        else:
            self.image = None

        if self.shType in (SHT_SYMTAB, SHT_DYNSYM):
            self.symbols = {}
            for idx, symbol in enumerate(range(self.shSize / ELF_SYM_TABLE_SIZE)):
                offset = idx * ELF_SYM_TABLE_SIZE
                data = self.image[offset : offset + ELF_SYM_TABLE_SIZE]
                symData = struct.unpack("{0}{1}".format(parent.byteOrderPrefix, SYMTAB_FMT), data)
                sym = Elf32_Sym(*symData)
                self.symbols[idx] = sym

        if self.shType in (SHT_REL, SHT_RELA):
            pass

    shAddress       = Alias("sh_addr")
    shAddressAlign  = Alias("sh_addralign")
    shEntitySize    = Alias("sh_entsize")
    shFlags         = Alias("sh_flags")
    shInfo          = Alias("sh_info")
    shLink          = Alias("sh_link")
    shNameIdx       = Alias("sh_name")
    shOffset        = Alias("sh_offset")
    shSize          = Alias("sh_size")
    shType          = Alias("sh_type")

    @property
    def shTypeName(self):
        TYPES = {
            SHT_NULL            : "NULL",
            SHT_PROGBITS        : "PROGBITS",
            SHT_SYMTAB          : "SYMTAB",
            SHT_STRTAB          : "STRTAB",
            SHT_RELA            : "RELA",
            SHT_HASH            : "HASH",
            SHT_DYNAMIC         : "DYNAMIC",
            SHT_NOTE            : "NOTE",
            SHT_NOBITS          : "NOBITS",
            SHT_REL             : "REL",
            SHT_SHLIB           : "SHLIB",
            SHT_DYNSYM          : "DYNSYM",
            SHT_INIT_ARRAY      : "INIT_ARRAY",
            SHT_FINI_ARRAY      : "FINI_ARRAY",
            SHT_PREINIT_ARRAY   : "PREINIT_ARRAY",
            SHT_GROUP           : "GROUP",
            SHT_SYMTAB_SHNDX    : "SYMTAB_SHNDX",
            SHT_NUM             : "NUM",
            SHT_LOOS            : "LOOS",
            SHT_GNU_ATTRIBUTES  : "NU_ATTRIBUTES",
            SHT_GNU_HASH        : "GNU_HASH",
            SHT_GNU_LIBLIST     : "GNU_LIBLIST",
            SHT_CHECKSUM        : "CHECKSUM",
            SHT_LOSUNW          : "LOSUNW",
            SHT_SUNW_move       : "SUNW_move",
            SHT_SUNW_COMDAT     : "UNW_COMDAT",
            SHT_SUNW_syminfo    : "SUNW_syminfo",
            SHT_GNU_verdef      : "VERDEF",
            SHT_GNU_verneed     : "VERNEED",
            SHT_GNU_versym      : "VERSYM",
            SHT_HISUNW          : "HISUNW",
            SHT_HIOS            : "HIOS",

            SHT_ARM_EXIDX       : "ARM_EXIDX",
            SHT_ARM_PREEMPTMAP  : "ARM_PREEMPTMAP",
            SHT_ARM_ATTRIBUTES  : "ARM_ATTRIBUTES",
            SHT_ARM_DEBUGOVERLAY    : "ARM_DEBUGOVERLAY",
            SHT_ARM_OVERLAYSECTION  : "ARM_OVERLAYSECTION",

            SHT_LOPROC          : "LOPROC",
            SHT_HIPROC          : "HIPROC",
            SHT_LOUSER          : "LOUSER",
            SHT_HIUSER          : "HIUSER"
        }
        return TYPES.get(self.shType, "UNKNOWN")

    @property
    def shName(self):
        return self._name


class ELFProgramHeaderTable(object):
    def __init__(self, parent, atPosition = 0):
        parent.inFile.seek(atPosition, os.SEEK_SET)
        data = parent.inFile.read(ELF_PHDR_SIZE32)

        try:
            elfProgramHeaderTable=struct.unpack("{0}{1}".format(parent.byteOrderPrefix, PHDR_FMT32), data)
        except struct.error:
            raise FormatError("Wrong program header table.")

        d = Elf32_Phdr(*elfProgramHeaderTable)
        for name, value in d._asdict().items():
            setattr(self, name, value)
        parent.inFile.seek(d.p_offset, os.SEEK_SET)
        self.image = parent.inFile.read(d.p_filesz)
        if d.p_type in (PT_DYNAMIC, PT_INTERP, PT_NOTE, PT_SHLIB, PT_PHDR):
            pass

    @property
    def phTypeName(self):
        NAMES = {
            0           : 'NULL',
            1           : 'LOAD',
            2           : 'DYNAMIC',
            3           : 'INTERP',
            4           : 'NOTE',
            5           : 'SHLIB',
            6           : 'PHDR',
            7           : 'TLS',
            8           : 'NUM',
            0x60000000  : 'LOOS',
            0x6474e550  : 'GNU_EH_FRAME',
            0x6474e551  : 'GNU_STACK',
            0x6474e552  : 'GNU_RELRO',
            0x6ffffffa  : 'LOSUNW',
            0x6ffffffa  : 'SUNWBSS',
            0x6ffffffb  : 'SUNWSTACK',
            0x6fffffff  : 'HIOS',
        }
        if self.phType in NAMES:
            return NAMES.get(self.phType)
        elif PT_LOPROC <= self.phType <= PT_HIPROC:
            return "PROCESSOR SPECIFIC"
        else:
            return "RES"

    phType              = Alias("p_type")
    phOffset            = Alias("p_offset")
    phVirtualAddress    = Alias("p_vaddr")
    phPhysicalAddress   = Alias("p_paddr")
    phFileSize          = Alias("p_filesz")
    phMemSize           = Alias("p_memsz")
    phFlags             = Alias("p_flags")
    phAlign             = Alias("p_align")


def getSpecialSectionName(section):
    if section == SHN_UNDEF:
        return "UNDEF"
    elif section == SHN_ABS:
        return "ABS"
    elif section == SHN_COMMON:
        return "COMMON"
    elif SHN_LOPROC <= section <= SHN_HIPROC:
        return "PROC"
    elif SHN_COMMON < section <= SHN_HIRESERVE:
        return "RES"
    else:
        return None


class Object(object):
    def __init__(self, copyFrom):
        for key, value in copyFrom._asdict().items():
            setattr(self, key, value)


class Reader(object):
    def __init__(self, inFile, readContent = True):
        if not hasattr(inFile, 'read'):
            raise TypeError("Need a file-like object.")
        self.inFile = inFile
        self.header = ELFHeader(self)

        self.programHeaders = []
        self.sectionHeaders = []
        self._sectionHeadersByName = {}
        self._stringCache = {}

        pos = self.header.e_phoff
        if pos:
            for _ in range(self.header.elfNumberOfPHs):
                self.programHeaders.append(ELFProgramHeaderTable(self, pos))
                pos += self.header.elfPHTEntrySize

        pos = self.header.e_shoff
        if pos:
            for _ in range(self.header.elfNumberOfSHs):
                self.sectionHeaders.append(ELFSectionHeaderTable(self, pos))
                pos += self.header.elfSHTEntrySize

        for idx, sectionHeader in enumerate(self.sectionHeaders):
            if sectionHeader.shType in (SHT_SYMTAB, SHT_DYNSYM):
                for _, symbol in sectionHeader.symbols.items():
                    o = Object(symbol)
                    o.sectionName = getSpecialSectionName(symbol.st_shndx)
            elif sectionHeader.shType in (SHT_REL, SHT_RELA):
                symtab = sectionHeader.shLink
                sectionToModify = sectionHeader.shInfo
                if sectionHeader.shType == SHT_REL:
                    entry = Elf32_Rel
                    entrySize = ELF_RELOCATION_SIZE
                else:
                    entry = Elf32_Rela
                    entrySize = ELF_RELOCATION_A_SIZE
                img = sectionHeader.image
                offset = 0
                for pos in range(len(img) / entrySize):
                    ddd = img[offset : offset + entrySize]
                    offset += entrySize
            elif sectionHeader == SHT_NOTE:
                pass
        for section in self.sectionHeaders:
            name = self.getString(self.header.elfStringTableIndex, section.shNameIdx)
            section._name = name
            self._sectionHeadersByName[name] = section

    def sectionHeaderByName(self, name):
        return self._sectionHeadersByName.get(name)

    def getString(self, tableIndex, entry):
        if (tableIndex, entry) in self._stringCache:
            return self._stringCache[(tableIndex, entry)]
        else:
            unterminatedString = self.sectionHeaders[tableIndex].image[entry : ]
            terminatedString = unterminatedString[ : unterminatedString.index('\x00')]
            self._stringCache[(tableIndex,entry)] = terminatedString
            return terminatedString

    @property
    def byteOrderPrefix(self):
        return self.header.byteOrderPrefix


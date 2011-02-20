#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _Enum import Enum
from collections import namedtuple
import sys
import os
import types
import struct

#
#   Reference:
#   ----------
#   Tool Interface Standard (TIS)
#   Executable and Linking Format (ELF) Specification Version 1.2
#


'''
/*                              Basic ELF Datatypes                                 */
/*                  Name                Size    Align   Purpose                     */
/* ================================================================================ */
typedef uint32_t    Elf32_Addr;     /*  4       4       Unsigned program address    */
typedef uint16_t    Elf32_Half;     /*  2       2       Unsigned medium integer     */
typedef uint32_t    Elf32_Off;      /*  4       4       Unsigned file offset        */
typedef int32_t     Elf32_Sword;    /*  4       4       Signed large integer        */
typedef uint32_t    Elf32_Word;     /*  4       4       Unsigned large integer      */
/*                  unsigned char       1       1       Unsigned small integer      */
'''


##
##
##   ELF Header.
##
##

EI_NIDENT=16        # Size of e_ident[].

HDR_FMT="B"*EI_NIDENT+"HHIIIIIHHHHHH"

ELF_HEADER_SIZE=struct.calcsize(HDR_FMT)

assert(struct.calcsize(HDR_FMT)==52)    # todo: Unittest!!!

Elf32_Ehdr=namedtuple("Elf32_Ehdr","""e_ident0 e_ident1 e_ident2 e_ident3 e_ident4 e_ident5 e_ident6
    e_ident7 e_ident8 e_ident9 e_ident10 e_ident11 e_ident12 e_ident13 e_ident14 e_ident15
    e_type e_machine e_version e_entry e_phoff e_shoff e_flags e_ehsize e_phentsize e_phnum
    e_shentsize e_shnum e_shstrndx""")

"""
typedef struct tagElf32_Ehdr {
    uint8_t     e_ident[EI_NIDENT];
    Elf32_Half  e_type;
    Elf32_Half  e_machine;
    Elf32_Word  e_version;
    Elf32_Addr  e_entry;
    Elf32_Off   e_phoff;
    Elf32_Off   e_shoff;
    Elf32_Word  e_flags;
    Elf32_Half  e_ehsize;
    Elf32_Half  e_phentsize;
    Elf32_Half  e_phnum;
    Elf32_Half  e_shentsize;
    Elf32_Half  e_shnum;
    Elf32_Half  e_shstrndx;
} Elf32_Ehdr;
"""

@Enum
class ELFType(object):
    ET_NONE = 0
    " No file type."
    ET_REL  = 1
    " Relocatable file."
    ET_EXEC = 2
    " Executable file."
    ET_DYN  = 3
    " Shared object file."
    ET_CORE = 4
    " Core file."
    #ET_LOPROC   ((Elf32_Half)0xff00)    /* Processor-specific.      */
    #ET_HIPROC   ((Elf32_Half)0xffff)    /* Processor-specific.      */


'''

  class OsAbi < Value
    fill(
             0 => [ :SysV, 'UNIX System V ABI' ],
             1 => [ :HPUX, 'HP-UX' ],
             2 => [ :NetBSD, 'NetBSD' ],
             3 => [ :Linux, 'Linux' ],
             4 => [ :Hurd, 'Hurd' ],
             6 => [ :Solaris, 'Solaris' ],
             7 => [ :Aix, 'IBM AIX' ],
             8 => [ :Irix, 'SGI Irix' ],
             9 => [ :FreeBSD, 'FreeBSD' ],
            10 => [ :Tru64, 'Compaq TRU64 UNIX' ],
            11 => [ :Modesto, 'Novell Modesto' ],
            12 => [ :OpenBSD, 'OpenBSD' ],
            13 => [ :OpenVMS, 'OpenVMS' ],
            14 => [ :NSK, 'Hewlett-Packard Non-Stop Kernel' ],
            15 => [ :AROS, 'AROS' ],
            16 => [ :FenixOS, 'FenixOS' ],
            97 => [ :ARM, 'ARM' ],
           255 => [ :Standalone, 'Standalone (embedded) application' ]
         )
  end
'''

ELF_TYPE_NAMES={
    ELFType.ET_NONE : "No file type.",
    ELFType.ET_REL  : "Relocatable file.",
    ELFType.ET_EXEC : "Executable file.",
    ELFType.ET_DYN  : "Shared object file.",
    ELFType.ET_CORE : "Core file."
}


@Enum
class ELFMachineType(object):
    EM_NONE         = 0      # No machine.
    EM_M32          = 1      # AT&T WE 32100.
    EM_SPARC        = 2      # SPARC.
    EM_386          = 3      # Intel 80386.
    EM_68K          = 4      # Motorola 68000.
    EM_88K          = 5      # Motorola 88000.

    '''
    RESERVED 6 Reserved for future use
    '''

    EM_860          = 7      # Intel 80860.
    EM_MIPS         = 8      # MIPS I Architecture.
    EM_S370         = 9      # IBM System/370 Processor.
    EM_MIPS_RS3_LE  = 10     # MIPS RS3000 Little-endian.

    '''
    RESERVED 11-14 Reserved for future use
    '''

    EM_PARISC       = 15     # Hewlett-Packard PA-RISC.
    RESERVED        = 16     # Reserved for future use.
    EM_VPP500       = 17     # Fujitsu VPP500.
    EM_SPARC32PLUS  = 18     # Enhanced instruction set SPARC.
    EM_960          = 19     # Intel 80960.
    EM_PPC          = 20     # PowerPC.
    EM_PPC64        = 21     # 64-bit PowerPC.
    '''
22 => [ :S390, 'IBM S390' ],
23 => [ :SPU, 'Sony/Toshiba/IBM SPU' ],
    '''

    '''
    RESERVED 22-35 Reserved for future use
    '''

    EM_V800         = 36     # NEC V800.
    EM_FR20         = 37     # Fujitsu FR20.
    EM_RH32         = 38     # TRW RH-32.
    EM_RCE          = 39     # Motorola RCE.
    EM_ARM          = 40     # Advanced RISC Machines ARM.
    EM_ALPHA        = 41     # Digital Alpha.
    EM_SH           = 42     # Hitachi SH.
    EM_SPARCV9      = 43     # SPARC Version 9.
    EM_TRICORE      = 44     # Siemens Tricore embedded processor.
    EM_ARC          = 45     # Argonaut RISC Core, Argonaut Technologies Inc.
    EM_H8_300       = 46     # Hitachi H8/300.
    EM_H8_300H      = 47     # Hitachi H8/300H.
    EM_H8S          = 48     # Hitachi H8S.
    EM_H8_500       = 49     # Hitachi H8/500.
    EM_IA_64        = 50     # Intel IA-64 processor architecture.
    EM_MIPS_X       = 51     # Stanford MIPS-X.
    EM_COLDFIRE     = 52     # Motorola ColdFire.
    EM_68HC12       = 53     # Motorola M68HC12.
    EM_MMA          = 54     # Fujitsu MMA Multimedia Accelerator.
    EM_PCP          = 55     # Siemens PCP.
    EM_NCPU         = 56     # Sony nCPU embedded RISC processor.
    EM_NDR1         = 57     # Denso NDR1 microprocessor.
    EM_STARCORE     = 58     # Motorola Star*Core processor.
    EM_ME16         = 59     # Toyota ME16 processor.
    EM_ST100        = 60     # STMicroelectronics ST100 processor.
    EM_TINYJ        = 61     # Advanced Logic Corp. TinyJ embedded processor family.
    EM_X8664        = 62     # AMD x86-64 architecture.
    EM_PDSP         = 63     # Sony DSP Processor.
    EM_PDP10        = 64     # DEC PDP-10
    EM_PDP11        = 65     # DEC PDP-11
    EM_FX66         = 66     # Siemens FX66 microcontroller.
    EM_ST9PLUS      = 67     # STMicroelectronics ST9+ 8/16 bit microcontroller.
    EM_ST7          = 68     # STMicroelectronics ST7 8-bit microcontroller.
    EM_68HC16       = 69     # Motorola MC68HC16 Microcontroller.
    EM_68HC11       = 70     # Motorola MC68HC11 Microcontroller.
    EM_68HC08       = 71     # Motorola MC68HC08 Microcontroller.
    EM_68HC05       = 72     # Motorola MC68HC05 Microcontroller.
    EM_SVX          = 73     # Silicon Graphics SVx.
    EM_ST19         = 74     # STMicroelectronics ST19 8-bit microcontroller.
    EM_VAX          = 75     # Digital VAX.
    EM_CRIS         = 76     # Axis Communications 32-bit embedded processor.
    EM_JAVELIN      = 77     # Infineon Technologies 32-bit embedded processor.
    EM_FIREPATH     = 78     # Element 14 64-bit DSP Processor.
    EM_ZSP          = 79     # LSI Logic 16-bit DSP Processor.
    EM_MMIX         = 80     # Donald Knuth's educational 64-bit processor.
    EM_HUANY        = 81     # Harvard University machine-independent object files .
    EM_PRISM        = 82     # SiTera Prism.
#    '''
#            83 => [ :AVR, 'Atmel AVR 8-bit microcontroller' ],
#            84 => [ :FR30, 'Fujitsu FR30' ],
#            85 => [ :D10V, 'Mitsubishi D10V' ],
#            86 => [ :D30V, 'Mitsubishi D30V' ],
#            87 => [ :V850, 'NEC v850' ],
#            88 => [ :M32R, 'Mitsubishi M32R' ],
#            89 => [ :MN10300, 'Matsushita MN10300' ],
#            90 => [ :MN10200, 'Matsushita MN10200' ],
#            91 => [ :PJ, 'picoJava' ],
#            92 => [ :OpenRISC, 'OpenRISC 32-bit embedded processor' ],
#            93 => [ :ARC_A5, 'ARC Cores Tangent-A5' ],
#            94 => [ :Xtensa, 'Tensilica Xtensa Architecture' ],
#            95 => [ :VideoCore, 'Alphamosaic VideoCore processor' ],
#            96 => [ :TMM_GPP, 'Thompson Multimedia General Purpose Processor' ],
#            97 => [ :NS32K, 'National Semiconductor 32000 series' ],
#            98 => [ :TPC, 'Tenor Network TPC processor' ],
#            99 => [ :SNP1K, 'Trebia SNP 1000 processor' ],
#           100 => [ :ST200, 'STMicroelectronics ST200 microcontroller' ],
#           101 => [ :IP2K, 'Ubicom IP2022 micro controller' ],
#           102 => [ :MAX, 'MAX Processor' ],
#           103 => [ :CR, 'National Semiconductor CompactRISC' ],
#           104 => [ :F2MC16, 'Fujitsu F2MC16' ],
#           105 => [ :MSP430, 'TI msp430 micro controller' ],
#           106 => [ :Blackfin, 'ADI Blackfin' ],
#           107 => [ :SE_C33, 'S1C33 Family of Seiko Epson processors' ],
#           108 => [ :SEP, 'Sharp embedded microprocessor' ],
#           109 => [ :ARCA, 'Arca RISC Microprocessor' ],
#           110 => [ :UNICORE, 'Microprocessor series from PKU-Unity Ltd. and MPRC of Peking University' ],
#           111 => [ :EXCESS, 'eXcess: 16/32/64-bit configurable embedded CPU' ],
#           112 => [ :DXP, 'Icera Semiconductor Inc. Deep Execution Processor' ],
#           113 => [ :Altera_Nios2, 'Altera Nios II soft-core processor' ],
#           114 => [ :CRX, 'National Semiconductor CRX' ],
#           115 => [ :XGATE, 'Motorola XGATE embedded processor' ],
#           116 => [ :C166, 'Infineon C16x/XC16x processor' ],
#           117 => [ :M16C, 'Renesas M16C series microprocessors' ],
#           118 => [ :DSPIC30F, 'Microchip Technology dsPIC30F Digital Signal Controller' ],
#           119 => [ :CE, 'Freescale Communication Engine RISC core' ],
#           120 => [ :M32C, 'Renesas M32C series microprocessors' ],
#           131 => [ :TSK3000, 'Altium TSK3000 core' ],
#           132 => [ :RS08, 'Freescale RS08 embedded processor' ],
#           134 => [ :ECOG2, 'Cyan Technology eCOG2 microprocessor' ],
#           135 => [ :Score, 'Sunplus Score' ],
#           135 => [ :Score7, 'Sunplus S+core7 RISC processor' ],
#           136 => [ :DSP24, 'New Japan Radio (NJR) 24-bit DSP Processor' ],
#           137 => [ :VideoCore3, 'Broadcom VideoCore III processor' ],
#           138 => [ :LatticeMICO32, 'RISC processor for Lattice FPGA architecture' ],
#           139 => [ :SE_C17, 'Seiko Epson C17 family' ],
#           140 => [ :TI_C6000, 'Texas Instruments TMS320C6000 DSP family' ],
#           141 => [ :TI_C2000, 'Texas Instruments TMS320C2000 DSP family' ],
#           142 => [ :TI_C5500, 'Texas Instruments TMS320C55x DSP family' ],
#           160 => [ :MMDSP_PLUS, 'STMicroelectronics 64bit VLIW Data Signal Processor' ],
#           161 => [ :Cypress_M8C, 'Cypress M8C microprocessor' ],
#           162 => [ :R32C, 'Renesas R32C series microprocessors' ],
#           163 => [ :TriMedia, 'NXP Semiconductors TriMedia architecture family' ],
#           164 => [ :QDSP6, 'QUALCOMM DSP6 Processor' ],
#           165 => [ :I8051, 'Intel 8051 and variants' ],
#           166 => [ :STXP7X, 'STMicroelectronics STxP7x family' ],
#           167 => [ :NDS32, 'Andes Technology compact code size embedded RISC processor family' ],
#           168 => [ :ECOG1, 'Cyan Technology eCOG1X family' ],
#           168 => [ :ECOG1X, 'Cyan Technology eCOG1X family' ],
#           169 => [ :MAXQ30, 'Dallas Semiconductor MAXQ30 Core Micro-controllers' ],
#           170 => [ :XIMO16, 'New Japan Radio (NJR) 16-bit DSP Processor' ],
#           171 => [ :MANIK, 'M2000 Reconfigurable RISC Microprocessor' ],
#           172 => [ :CRAYNV2, 'Cray Inc. NV2 vector architecture' ],
#           173 => [ :RX, 'Renesas RX family' ],
#           174 => [ :METAG, 'Imagination Technologies META processor architecture' ],
#           175 => [ :MCST_ELBRUS, 'MCST Elbrus general purpose hardware architecture' ],
#           176 => [ :ECOG16, 'Cyan Technology eCOG16 family' ],
#           177 => [ :CR16, 'National Semiconductor CompactRISC 16-bit processor' ],
#           178 => [ :ETPU, 'Freescale Extended Time Processing Unit' ],
#           179 => [ :SLE9X, 'Infineon Technologies SLE9X core' ],
#           180 => [ :L1OM, 'Intel L1OM' ],
#           185 => [ :AVR32, 'Atmel Corporation 32-bit microprocessor family' ],
#           186 => [ :STM8, 'STMicroeletronics STM8 8-bit microcontroller' ],
#           187 => [ :TILE64, 'Tilera TILE64 multicore architecture family' ],
#           188 => [ :TILEPro, 'Tilera TILEPro multicore architecture family' ],
#           189 => [ :MicroBlaze, 'Xilinx MicroBlaze 32-bit RISC soft processor core' ],
#           190 => [ :CUDA, 'NVIDIA CUDA architecture' ],
#           0x9026 => [ :Alpha, 'DEC Alpha' ]
#    '''

ELF_MACHINE_NAMES={
    ELFMachineType.EM_NONE         : "No machine.",
    ELFMachineType.EM_M32          : "AT&T WE 32100.",
    ELFMachineType.EM_SPARC        : "SPARC.",
    ELFMachineType.EM_386          : "Intel 80386.",
    ELFMachineType.EM_68K          : "Motorola 68000.",
    ELFMachineType.EM_88K          : "Motorola 88000.",
    ELFMachineType.EM_860          : "Intel 80860.",
    ELFMachineType.EM_MIPS         : "MIPS I Architecture.",
    ELFMachineType.EM_S370         : "IBM System/370 Processor.",
    ELFMachineType.EM_MIPS_RS3_LE  : "MIPS RS3000 Little-endian.",
    ELFMachineType.EM_PARISC       : "Hewlett-Packard PA-RISC.",
    ELFMachineType.RESERVED        : "Reserved for future use.",
    ELFMachineType.EM_VPP500       : "Fujitsu VPP500.",
    ELFMachineType.EM_SPARC32PLUS  : "Enhanced instruction set SPARC.",
    ELFMachineType.EM_960          : "Intel 80960.",
    ELFMachineType.EM_PPC          : "PowerPC.",
    ELFMachineType.EM_PPC64        : "64-bit PowerPC.",
    ELFMachineType.EM_V800         : "NEC V800.",
    ELFMachineType.EM_FR20         : "Fujitsu FR20.",
    ELFMachineType.EM_RH32         : "TRW RH-32.",
    ELFMachineType.EM_RCE          : "Motorola RCE.",
    ELFMachineType.EM_ARM          : "Advanced RISC Machines ARM.",
    ELFMachineType.EM_ALPHA        : "Digital Alpha.",
    ELFMachineType.EM_SH           : "Hitachi SH.",
    ELFMachineType.EM_SPARCV9      : "SPARC Version 9.",
    ELFMachineType.EM_TRICORE      : "Siemens Tricore embedded processor.",
    ELFMachineType.EM_ARC          : "Argonaut RISC Core, Argonaut Technologies Inc.",
    ELFMachineType.EM_H8_300       : "Hitachi H8/300.",
    ELFMachineType.EM_H8_300H      : "Hitachi H8/300H.",
    ELFMachineType.EM_H8S          : "Hitachi H8S.",
    ELFMachineType.EM_H8_500       : "Hitachi H8/500.",
    ELFMachineType.EM_IA_64        : "Intel IA-64 processor architecture.",
    ELFMachineType.EM_MIPS_X       : "Stanford MIPS-X.",
    ELFMachineType.EM_COLDFIRE     : "Motorola ColdFire.",
    ELFMachineType.EM_68HC12       : "Motorola M68HC12.",
    ELFMachineType.EM_MMA          : "Fujitsu MMA Multimedia Accelerator.",
    ELFMachineType.EM_PCP          : "Siemens PCP.",
    ELFMachineType.EM_NCPU         : "Sony nCPU embedded RISC processor.",
    ELFMachineType.EM_NDR1         : "Denso NDR1 microprocessor.",
    ELFMachineType.EM_STARCORE     : "Motorola Star*Core processor.",
    ELFMachineType.EM_ME16         : "Toyota ME16 processor.",
    ELFMachineType.EM_ST100        : "STMicroelectronics ST100 processor.",
    ELFMachineType.EM_TINYJ        : "Advanced Logic Corp. TinyJ embedded processor family.",
    ELFMachineType.EM_X8664        : "AMD x86-64 architecture.",
    ELFMachineType.EM_PDSP         : "Sony DSP Processor.",
    ELFMachineType.EM_PDP10        : "DEC PDP-10",
    ELFMachineType.EM_PDP11        : "DEC PDP-11",
    ELFMachineType.EM_FX66         : "Siemens FX66 microcontroller.",
    ELFMachineType.EM_ST9PLUS      : "STMicroelectronics ST9+ 8/16 bit microcontroller.",
    ELFMachineType.EM_ST7          : "STMicroelectronics ST7 8-bit microcontroller.",
    ELFMachineType.EM_68HC16       : "Motorola MC68HC16 Microcontroller.",
    ELFMachineType.EM_68HC11       : "Motorola MC68HC11 Microcontroller.",
    ELFMachineType.EM_68HC08       : "Motorola MC68HC08 Microcontroller.",
    ELFMachineType.EM_68HC05       : "Motorola MC68HC05 Microcontroller.",
    ELFMachineType.EM_SVX          : "Silicon Graphics SVx.",
    ELFMachineType.EM_ST19         : "STMicroelectronics ST19 8-bit microcontroller.",
    ELFMachineType.EM_VAX          : "Digital VAX.",
    ELFMachineType.EM_CRIS         : "Axis Communications 32-bit embedded processor.",
    ELFMachineType.EM_JAVELIN      : "Infineon Technologies 32-bit embedded processor.",
    ELFMachineType.EM_FIREPATH     : "Element 14 64-bit DSP Processor.",
    ELFMachineType.EM_ZSP          : "LSI Logic 16-bit DSP Processor.",
    ELFMachineType.EM_MMIX         : "Donald Knuth's educational 64-bit processor.",
    ELFMachineType.EM_HUANY        : "Harvard University machine-independent object files .",
    ELFMachineType.EM_PRISM        : "SiTera Prism."
}


EV_NONE         = 0      # Invalid version.
EV_CURRENT      = 1      # Current version.


EI_MAG0         = 0      # File identification.
EI_MAG1         = 1      # File identification.
EI_MAG2         = 2      # File identification.
EI_MAG3         = 3      # File identification.
EI_CLASS        = 4      # File class.
EI_DATA         = 5      # Data encoding.
EI_VERSION      = 6      # File version.
EI_PAD          = 7      # Start of padding bytes.
## todo: check!!!
EI_OSABI        = 7      # Operating system/ABI identification.
EI_ABIVERSION   = 8      # ABI version.


@Enum
class ELFClass(object):
    ELFCLASSNONE    = 0      # Invalid class.
    ELFCLASS32      = 1      # 32-bit objects.
    ELFCLASS64      = 2      # 64-bit objects.


ELF_CLASS_NAMES={
    ELFClass.ELFCLASSNONE   : "Invalid class.",
    ELFClass.ELFCLASS32     : "32-bit objects.",
    ELFClass.ELFCLASS64     : "64-bit objects."
}

@Enum
class ELFDataEncoding(object):
    ELFDATANONE     = 0      # Invalid data encoding.
    ELFDATA2LSB     = 1      # Little-Endian.
    ELFDATA2MSB     = 2      # Big-Endian.


ELF_BYTE_ORDER_NAMES={
    ELFDataEncoding.ELFDATANONE : "Invalid data encoding.",
    ELFDataEncoding.ELFDATA2LSB : "Little-Endian.",
    ELFDataEncoding.ELFDATA2MSB : "Big-Endian."
}

##
##
##   ELF Sections.
##
##

SEC_FMT="IIIIIIIIII"

"""
typedef struct tagElf32_Shdr {
    Elf32_Word  sh_name;
    Elf32_Word  sh_type;
    Elf32_Word  sh_flags;
    Elf32_Addr  sh_addr;
    Elf32_Off   sh_offset;
    Elf32_Word  sh_size;
    Elf32_Word  sh_link;
    Elf32_Word  sh_info;
    Elf32_Word  sh_addralign;
    Elf32_Word  sh_entsize;
} Elf32_Shdr;
"""

ELF_SECTION_SIZE=struct.calcsize(SEC_FMT)

Elf32_Shdr=namedtuple("Elf32_Shdr","""sh_name sh_type sh_flags sh_addr sh_offset sh_size
    sh_link sh_info sh_addralign sh_entsize""")


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
SHN_HIRESERVE   = 0xffff
    # SHN_HIRESERVE This value specifies the upper bound of the range of reserved indexes.
    # The system reserves indexes between SHN_LORESERVE and SHN_HIRESERVE, inclusive;
    # the values do not reference the section header table.That is, the section header
    # table does not contain entries for the  reserved indexes.


SHT_NULL        = 0
SHT_PROGBITS    = 1
SHT_SYMTAB      = 2
SHT_STRTAB      = 3
SHT_RELA        = 4
SHT_HASH        = 5
SHT_DYNAMIC     = 6
SHT_NOTE        = 7
SHT_NOBITS      = 8
SHT_REL         = 9
SHT_SHLIB       = 10
SHT_DYNSYM      = 11
SHT_LOPROC      = 0x70000000
SHT_HIPROC      = 0x7fffffff
SHT_LOUSER      = 0x80000000
SHT_HIUSER      = 0xffffffff


SHF_WRITE       = 0x1
SHF_ALLOC       = 0x2
SHF_EXECINSTR   = 0x4
SHF_MASKPROC    = 0xf0000000


##
##
##   ELF Symbol Table.
##
##

SYMTAB_FMT="IIIBBH"

""""
typedef struct tagElf32_Sym {
    Elf32_Word  st_name;
    Elf32_Addr  st_value;
    Elf32_Word  st_size;
    uint8_t     st_info;
    uint8_t     st_other;
    Elf32_Half  st_shndx;
} Elf32_Sym;
"""

Elf32_Sym=namedtuple("Elf32_Sym","st_name st_value st_size st_info st_other st_shndx")

ELF_SYM_TABLE_SIZE = struct.calcsize(SYMTAB_FMT)

STN_UNDEF   = 0


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

REL_FMT="II"

RELA_FMT="IIi"

"""
typedef struct tagElf32_Rel {
    Elf32_Addr  r_offset;
    Elf32_Word  r_info;
} Elf32_Rel;
"""

"""
typedef struct tagElf32_Rela {
    Elf32_Addr  r_offset;
    Elf32_Word  r_info;
    Elf32_Sword r_addend;
} Elf32_Rela;
"""

ELF_RELOCATION_SIZE     = struct.calcsize(REL_FMT)
ELF_RELOCATION_A_SIZE   = struct.calcsize(RELA_FMT)

Elf32_Rel=namedtuple("Elf32_Rel","r_offset r_info")
Elf32_Rela=namedtuple("Elf32_Rela","r_offset r_info r_addend")

##
##
##   ELF Program Header
##
##

PHDR_FMT="IIIIIIII"

"""
typedef struct tagElf32_Phdr {
    Elf32_Word  p_type;
    Elf32_Off   p_offset;
    Elf32_Addr  p_vaddr;
    Elf32_Addr  p_paddr;
    Elf32_Word  p_filesz;
    Elf32_Word  p_memsz;
    Elf32_Word  p_flags;
    Elf32_Word  p_align;
} Elf32_Phdr;
"""

ELF_PHDR_SIZE = struct.calcsize(PHDR_FMT)

Elf32_Phdr=namedtuple("Elf32_Phdr","p_type p_offset p_vaddr p_paddr p_filesz p_memsz p_flags p_align")


PT_NULL             =0
PT_LOAD             =1
PT_DYNAMIC          =2
PT_INTERP           =3
PT_NOTE             =4
PT_SHLIB            =5
PT_PHDR             =6
PT_LOPROC           =0x70000000
PT_HIPROC           =0x7fffffff

PF_X                = 0x1           # Execute.
PF_W                = 0x2           # Write.
PF_R                = 0x4           # Read.
PF_MASKPROC         = 0xf0000000    # Unspecified.

##
##
##
##
##
'''
#define ELF_IDENT(hptr,ofs)         ((hptr)->e_ident[(ofs)])
    #define ELF_MAG0(hptr)          (ELF_IDENT((hptr),EI_MAG0))
    #define ELF_MAG1(hptr)          (ELF_IDENT((hptr),EI_MAG1))
    #define ELF_MAG2(hptr)          (ELF_IDENT((hptr),EI_MAG2))
    #define ELF_MAG3(hptr)          (ELF_IDENT((hptr),EI_MAG3))
    #define ELF_CLASS(hptr)         (ELF_IDENT((hptr),EI_CLASS))
    #define ELF_DATA(hptr)          (ELF_IDENT((hptr),EI_DATA))
    #define ELF_VERSION(hptr)       (ELF_IDENT((hptr),EI_VERSION))
    #define ELF_PAD(hptr)           (ELF_IDENT((hptr),EI_PAD))
    #define ELF_OSABI(hptr)         (ELF_IDENT((hptr),EI_OSABI))
    #define ELF_ABIVERSION(hptr)    (ELF_IDENT((hptr),EI_ABIVERSION))
    #define ELF_NIDENT(hptr)        (ELF_IDENT((hptr),EI_NIDENT))

#define ELF_TYPE(hptr)              ((hptr)->e_type)
#define ELF_MACHINE(hptr)           ((hptr)->e_machine)
#define ELF_VER(hptr)               ((hptr)->e_version)
#define ELF_ENTRY(hptr)             ((hptr)->e_entry)
#define ELF_PHOFF(hptr)             ((hptr)->e_phoff)
#define ELF_SHOFF(hptr)             ((hptr)->e_shoff)
#define ELF_FLAGS(hptr)             ((hptr)->e_flags)
#define ELF_EHSIZE(hptr)            ((hptr)->e_ehsize)
#define ELF_PHENTSIZE(hptr)         ((hptr)->e_phentsize)
#define ELF_PHNUM(hptr)             ((hptr)->e_phnum)
#define ELF_SHENTSIZE(hptr)         ((hptr)->e_shentsize)
#define ELF_SHNUM(hptr)             ((hptr)->e_shnum)
#define ELF_SHSTRNDX(hptr)          ((hptr)->e_shstrndx)

#define ELF_IS_EXECUTABLE(hdr)  (ELF_TYPE((hdr))==ET_EXEC || ELF_TYPE((hdr))==ET_DYN)

#if 0
typedef enum tagElf_EndianessType {
    ELF_INVALID_ENCODING,
    ELF_BIG_ENDIAN,
    ELF_LITTLE_ENDIAN
} Elf_EndianessType;
#endif

#define ELF_SH_NAME(shr)         ((shr)->sh_name)
#define ELF_SH_TYPE(shr)         ((shr)->sh_type)
#define ELF_SH_FLAGS(shr)        ((shr)->sh_flags)
#define ELF_SH_ADDR(shr)         ((shr)->sh_addr)
#define ELF_SH_OFFSET(shr)       ((shr)->sh_offset)
#define ELF_SH_SIZE(shr)         ((shr)->sh_size)
#define ELF_SH_LINK(shr)         ((shr)->sh_link)
#define ELF_SH_INFO(shr)         ((shr)->sh_info)
#define ELF_SH_ADDRALIGN(shr)    ((shr)->sh_addralign)
#define ELF_SH_ENTSIZE(shr)      ((shr)->sh_entsize)

/*
**
**  ELF Symbol Table.
**
*/

#define ELF32_ST_BIND(i)    ((i) >> 4)
#define ELF32_ST_TYPE(i)    ((i) & 0xf)
#define ELF32_ST_INFO(b,t)  (((b) << 4) + ((t) & 0xf))


/*
**
**  Relocation.
**
*/
#define ELF32_R_SYM(i)      ((i) >> 8)
#define ELF32_R_TYPE(i)     ((unsigned char)(i))
#define ELF32_R_INFO(s,t)   (((s) << 8)+(unsigned char)(t))

/*
**
**  Program Header.
**
*/

#define ELF_PH_TYPE(phr)    ((phr)->p_type)
#define ELF_PH_OFFSET(phr)  ((phr)->p_offset)
#define ELF_PH_VADDR(phr)   ((phr)->p_vaddr)
#define ELF_PH_PADDR(phr)   ((phr)->p_paddr)
#define ELF_PH_FILESZ(phr)  ((phr)->p_filesz)
#define ELF_PH_MEMSZ(phr)   ((phr)->p_memsz)
#define ELF_PH_FLAGS(phr)   ((phr)->p_flags)
#define ELF_PH_ALIGN(phr)   ((phr)->p_align)
'''


class Alias(object):
    def __init__(self,key,convert=False):
        self.key=key
        self.convert=convert

    def __get__(self,obj,objtype=None):
        if obj is None:
            return self
        data=getattr(obj,'data')
        value=getattr(data,self.key)
        return value

    def __set__(self,obj,value):
        data=getattr(obj,'data')
        setattr(data,self.key,value)
        c=getattr(data,self.key)

    def __delete__(self, obj):
        raise AttributeError("can't delete attribute")


def byteorder():
    bo=sys.byteorder
    if bo=='little':
        return ELFDataEncoding('ELFDATA2LSB')
    elif bo=='big':
        return ELFDataEncoding('ELFDATA2MSB')


BYTEORDER_PREFIX={
    ELFDataEncoding.ELFDATA2LSB : '<',  # Little-Endian.
    ELFDataEncoding.ELFDATA2MSB : '>'   # Big-Endian.
}


class Null(object): pass


class ELFHeader(object):
    def __init__(self,parent):
        self.parent=parent
        parent.inFile.seek(0,os.SEEK_SET)
        data=parent.inFile.read(ELF_HEADER_SIZE)

        elfHeader=struct.unpack(HDR_FMT,data)
        if not self._checkMagic(elfHeader):
            # todo: Error-Handling!!!
            return

        d=Elf32_Ehdr(*elfHeader)
        self.byteorderPrefix=BYTEORDER_PREFIX[ELFDataEncoding(d.e_ident5)]
        parent.byteorderPrefix=self.byteorderPrefix

        # Unpack again, /w corrected byte-order.
        elfHeader=struct.unpack("%s%s" % (self.byteorderPrefix,HDR_FMT),data)
        d=Elf32_Ehdr(*elfHeader)

        self.data=Null()
        for key,value in ((d._fields[i],d[i]) for i in range(len(d))):
            setattr(self.data,key,value)

        if not (self.elfEHSize==ELF_HEADER_SIZE):
            # todo: Error-Handling!!!
            return
        if not (self.elfPHTEntrySize==ELF_PHDR_SIZE):
            # todo: Error-Handling!!!
            return
        if not (self.elfSHTEntrySize==ELF_SECTION_SIZE):
            # todo: Error-Handling!!!
            return

        self.hasStringTable=not (self.elfStringTableIndex==SHN_UNDEF)

    def _checkMagic(self,header):
        return ((header[EI_MAG0]==0x7f) and (header[EI_MAG1]==ord('E'))
            and (header[EI_MAG2]==ord('L')) and (header[EI_MAG3]==ord('F')))

    @property
    def elfTypeName(self):
        return ELF_TYPE_NAMES.get(ELFType(self.elfType),"Processor-specific.")

    @property
    def elfMachineName(self):
        return ELF_MACHINE_NAMES.get(ELFMachineType(self.elfMachine),"*** unknown ***")

    @property
    def elfClassName(self):
        return ELF_CLASS_NAMES.get(ELFClass(self.elfClass),"*** unknown ***")

    @property
    def elfByteOrderName(self):
        return ELF_BYTE_ORDER_NAMES.get(ELFDataEncoding(self.elfByteOrder),"*** unknown ***")

    # Install pretty names.
    elfClass=Alias("e_ident4")
    elfByteOrder=Alias("e_ident5")
    elfVersion=Alias("e_ident6")
    elfOsAbi=Alias("e_ident7")
    elfAbiVersion=Alias("e_ident8")
    elfType=Alias("e_type")
    elfMachine=Alias("e_machine")
    elfEntryPoint=Alias("e_entry")
    elfProgramHeaderTableOffset=Alias("e_phoff")
    elfSectionHeaderTableOffset=Alias("e_shoff")
    elfFlags=Alias("e_flags")
    elfEHSize=Alias("e_ehsize")
    elfPHTEntrySize=Alias("e_phentsize")
    elfNumberOfPHs=Alias("e_phnum")
    elfSHTEntrySize=Alias("e_shentsize")
    elfNumberOfSHs=Alias("e_shnum")
    elfStringTableIndex=Alias("e_shstrndx")


class ELFSymbol(object):
    def __init__(self,parent,data):
        pass


class ELFSectionHeaderTable(object):
    def __init__(self,parent,atPosition=0):
        self.parent=parent
        parent.inFile.seek(atPosition,os.SEEK_SET)
        data=parent.inFile.read(ELF_SECTION_SIZE)
        self.image=str()    # self.image=bytearray()

        elfProgramHeaderTable=struct.unpack("%s%s" % (parent.byteorderPrefix,SEC_FMT),data)
        d=Elf32_Shdr(*elfProgramHeaderTable)
        self.data=Null()
        for key,value in ((d._fields[i],d[i]) for i in range(len(d))):
            setattr(self.data,key,value)

        if self.shType not in (SHT_NOBITS,SHT_NULL) and self.shSize>0:
            pos=self.shOffset
            parent.inFile.seek(pos,os.SEEK_SET)
            #self.image=bytearray(parent.inFile.read(self.shSize))
            self.image=parent.inFile.read(self.shSize)

        if self.shType in (SHT_SYMTAB,SHT_DYNSYM):
            self.symbols={}
            for idx,symbol in enumerate(range(self.shSize/ELF_SYM_TABLE_SIZE)):
                offset=idx*ELF_SYM_TABLE_SIZE
                data=self.image[offset:offset+ELF_SYM_TABLE_SIZE]
                symData=struct.unpack("%s%s" % (parent.byteorderPrefix,SYMTAB_FMT),data)
                sym=Elf32_Sym(*symData)
                self.symbols[idx]=sym

    shAddress=Alias("sh_addr")
    shAddressAlign=Alias("sh_addralign")
    shEntitySize=Alias("sh_entsize")
    shFlags=Alias("sh_flags")
    shInfo=Alias("sh_info")
    shLink=Alias("sh_link")
    shNameIdx=Alias("sh_name")
    shOffset=Alias("sh_offset")
    shSize=Alias("sh_size")
    shType=Alias("sh_type")

    @property
    def shTypeName(self):
        TYPES={
            SHT_NULL        : "NULL",
            SHT_PROGBITS    : "PROGBITS",
            SHT_SYMTAB      : "SYMTAB",
            SHT_STRTAB      : "STRTAB",
            SHT_RELA        : "RELA",
            SHT_HASH        : "HASH",
            SHT_DYNAMIC     : "DYNAMIC",
            SHT_NOTE        : "NOTE",
            SHT_NOBITS      : "NOBITS",
            SHT_REL         : "REL",
            SHT_SHLIB       : "SHLIB",
            SHT_DYNSYM      : "DYNSYM",
            SHT_LOPROC      : "LOPROC",
            SHT_HIPROC      : "HIPROC",
            SHT_LOUSER      : "LOUSER",
            SHT_HIUSER      : "HIUSER"
        }
        return TYPES.get(self.shType,"UNKNOWN")

    @property
    def shName(self):
        pass
        #print self.parent


class ELFProgramHeaderTable(object):
    def __init__(self,parent,atPosition=0):
        parent.inFile.seek(atPosition,os.SEEK_SET)
        data=parent.inFile.read(ELF_PHDR_SIZE)

        elfProgramHeaderTable=struct.unpack("%s%s" % (parent.byteorderPrefix,PHDR_FMT),data)
        d=Elf32_Phdr(*elfProgramHeaderTable)
        self.data=Null()
        for key,value in ((d._fields[i],d[i]) for i in range(len(d))):
            setattr(self.data,key,value)

    @property
    def phTypeName(self):
        NAMES={
            0: "NO_TYPE",
            1: "RELOC",
            2: "EXEC",
            3: "SHARED",
            4: "CORE"
        }
        try:
            type_=ELFType(self.phType)
        except AttributeError:
            return "RES"
        if type_<=ELFType.ET_CORE:
            return NAMES.get(self.phType)
        elif ELFType.ET_LOPROC < type_ <=ELFType.ET_HIPROC:
            return "PROCESSOR SPECIFIC"
        else:
            return "RES"

    phType=Alias("p_type")
    phOffset=Alias("p_offset")
    phVirtualAddress=Alias("p_vaddr")
    phPhysicalAddress=Alias("p_paddr")
    phFileSize=Alias("p_filesz")
    phMemSize=Alias("p_memsz")
    phFlags=Alias("p_flags")
    phAlign=Alias("p_align")


class Reader(object):
    def __init__(self,inFile):
        if not hasattr(inFile,'read'):
            raise TypeError("Need a file-like object.")
        self.inFile=inFile
        self.header=ELFHeader(self)

        self.programHeaders=[]
        self.sectionHeaders=[]
        self._stringCache={}

        pos=self.header.data.e_phoff
        if pos:
            for _ in range(self.header.elfNumberOfPHs):
                self.programHeaders.append(ELFProgramHeaderTable(self,pos))
                pos+=self.header.elfPHTEntrySize

        pos=self.header.data.e_shoff
        if pos:
            for _ in range(self.header.elfNumberOfSHs):
                self.sectionHeaders.append(ELFSectionHeaderTable(self,pos))
                pos+=self.header.elfSHTEntrySize

    def getString(self,tableIndex,entry):
        if (tableIndex,entry) in self._stringCache:
            return self._stringCache[(tableIndex,entry)]
        else:
            # self.header.elfStringTableIndex
            unterminatedString=self.sectionHeaders[tableIndex].image[entry:]
#            if not unterminatedString:
#                return ''
            terminatedString=unterminatedString[:unterminatedString.index('\x00')]
            self._stringCache[(tableIndex,entry)]=terminatedString
            return terminatedString


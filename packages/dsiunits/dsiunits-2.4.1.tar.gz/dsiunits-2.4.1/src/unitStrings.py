# This file is part of dsiUnits (https://gitlab1.ptb.de/digitaldynamicmeasurement/dsiUnits/)
# Copyright 2024 [Benedikt Seeger(PTB), Vanessa Stehr(PTB)]
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or (at your option) any later version.

#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Lesser General Public License for more details.

#You should have received a copy of the GNU Lesser General Public
#License along with this library; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
from math import pi

_dsiPrefixesLatex = {
    'deca': r'\mathrm{da}',
    'hecto': r'\mathrm{h}',
    'kilo': r'\mathrm{k}',
    'mega': r'\mathrm{M}',
    'giga': r'\mathrm{G}',
    'tera': r'\mathrm{T}',
    'peta': r'\mathrm{P}',
    'exa': r'\mathrm{E}',
    'zetta': r'\mathrm{Z}',
    'yotta': r'\mathrm{Y}',
    'deci': r'\mathrm{d}',
    'centi': r'\mathrm{c}',
    'milli': r'\mathrm{m}',
    'micro': r'\mu',# todo this ist most likely italic find a fix that doesn't needs external packages :(
    'nano': r'\mathrm{n}',
    'pico': r'\mathrm{p}',
    'femto': r'\mathrm{f}',
    'atto': r'\mathrm{a}',
    'zepto': r'\mathrm{z}',
    'yocto': r'\mathrm{y}',
    'kibi': r'\mathrm{Ki}',
    'mebi': r'\mathrm{Mi}',
    'gibi': r'\mathrm{Gi}',
    'tebi': r'\mathrm{Ti}',
    'pebi': r'\mathrm{Pi}',
    'exbi': r'\mathrm{Ei}',
    'zebi': r'\mathrm{Zi}',
    'yobi': r'\mathrm{Yi}'
}
#TODO maybe directly using the exponents is better
# mapping D-SI prefixes to scale factors
_dsiPrefixesScales = {
    'yotta': 1e24,
    'zetta': 1e21,
    'exa': 1e18,
    'peta': 1e15,
    'tera': 1e12,
    'giga': 1e9,
    'mega': 1e6,
    'kilo': 1e3,
    'hecto': 1e2,
    'deca': 1e1,
    '':1.0,
    'deci': 1e-1,
    'centi': 1e-2,
    'milli': 1e-3,
    'micro': 1e-6,
    'nano': 1e-9,
    'pico': 1e-12,
    'femto': 1e-15,
    'atto': 1e-18,
    'zepto': 1e-21,
    'yocto': 1e-24,
    'kibi': 1024,                       #2^10
    'mebi': 1048576,                    #2^20
    'gibi': 1073741824,                 #2^30
    'tebi': 1099511627776,              #2^40
    'pebi': 1125899906842624,           #2^50
    'exbi': 1152921504606846976,        #2^60 larger than 2^53 so quantization error is possible
    'zebi': 1180591620717411303424,     #2^70 larger than 2^53 so quantization error is possible
    'yobi': 1208925819614629174706176   #2^80 larger than 2^53 so quantization error is possible
}
# UTF-8 equivalents for SI prefixes
_dsiPrefixesUTF8 = {
    'deca': 'da',
    'hecto': 'h',
    'kilo': 'k',
    'mega': 'M',
    'giga': 'G',
    'tera': 'T',
    'peta': 'P',
    'exa': 'E',
    'zetta': 'Z',
    'yotta': 'Y',
    'deci': 'd',
    'centi': 'c',
    'milli': 'm',
    # Unicode character for micro: 'µ' (U+00B5)
    'micro': 'µ',
    'nano': 'n',
    'pico': 'p',
    'femto': 'f',
    'atto': 'a',
    'zepto': 'z',
    'yocto': 'y',
    'kibi': 'Ki',
    'mebi': 'Mi',
    'gibi': 'Gi',
    'tebi': 'Ti',
    'pebi': 'Pi',
    'exbi': 'Ei',
    'zebi': 'Zi',
    'yobi': 'Yi'
}
# mapping D-SI units to latex
_dsiUnitsLatex = {
    'metre': r'\mathrm{m}',
    'kilogram': r'\mathrm{kg}',
    'second': r'\mathrm{s}',
    'ampere': r'\mathrm{A}',
    'kelvin': r'\mathrm{K}',
    'mole': r'\mathrm{mol}',
    'candela': r'\mathrm{cd}',
    'one': r'1',
    'day': r'\mathrm{d}',
    'hour': r'\mathrm{h}',
    'minute': r'\mathrm{min}',
    'degree': r'^\circ',
    'arcminute': r"'",
    'arcsecond': r"''",
    'gram': r'\mathrm{g}',
    'radian': r'\mathrm{rad}',
    'steradian': r'\mathrm{sr}',
    'hertz': r'\mathrm{Hz}',
    'newton': r'\mathrm{N}',
    'pascal': r'\mathrm{Pa}',
    'joule': r'\mathrm{J}',
    'watt': r'\mathrm{W}',
    'coulomb': r'\mathrm{C}',
    'volt': r'\mathrm{V}',
    'farad': r'\mathrm{F}',
    'ohm': r'\Omega',
    'siemens': r'\mathrm{S}',
    'weber': r'\mathrm{Wb}',
    'tesla': r'\mathrm{T}',
    'henry': r'\mathrm{H}',
    'degreecelsius': r'^\circ\mathrm{C}',
    'lumen': r'\mathrm{lm}',
    'lux': r'\mathrm{lx}',
    'becquerel': r'\mathrm{Bq}',
    'sievert': r'\mathrm{Sv}',
    'gray': r'\mathrm{Gy}',
    'katal': r'\mathrm{kat}',
    'hectare': r'\mathrm{ha}',
    'litre': r'\mathrm{l}',
    'tonne': r'\mathrm{t}',
    'electronvolt': r'\mathrm{eV}',
    'dalton': r'\mathrm{Da}',
    'astronomicalunit': r'\mathrm{au}',
    'neper': r'\mathrm{Np}',
    'bel': r'\mathrm{B}',
    'decibel': r'\mathrm{dB}',
    'percent':r'\%',
    'ppm':r'\mathrm{ppm}',
    'byte': r'\mathrm{Byte}',
    'bit': r'\mathrm{bit}',
    'angstrom': r'\AA',
    'bar': r'\mathrm{bar}',
    'atomicunittime': r'\frac{\hbar}{m}_e \cdot c^2}',
    'atomicmassunit': r'\mathrm{u}',
    'barn': r'\mathrm{b}',
    'clight': 'c',
    'electronmass': 'm_e',
    'elementarycharge': 'e',
    'mmhg': r'\mathrm{mmHg}',
    'naturalunittime': r'\frac{\hbar}{m}_e \cdot c^2}',
    'hartree': r'E_\mathrm{h}',
    'bohr': 'a_0',
    'nauticalmile': r'\mathrm{NM}',
    'knot': r'\mathrm{kn}',
    'planckbar':r'\hbar'
}
# Comprehensive mapping from ASCII/UTF-8 representations to D-SI LaTeX strings
ascii_to_dsi_unit_map = {
    'kg': 'kilogram',
    'm': 'metre',
    's': 'second',
    'A': 'ampere',
    'K': 'kelvin',
    'mol': 'mole',
    'cd': 'candela',
    'g': 'gram',
    'rad': 'radian',
    'sr': 'steradian',
    'Hz': 'hertz',
    'N': 'newton',
    'Pa': 'pascal',
    'J': 'joule',
    'W': 'watt',
    'C': 'coulomb',
    'V': 'volt',
    'F': 'farad',
    'Ω': 'ohm',
    'S': 'siemens',
    'Wb': 'weber',
    'T': 'tesla',
    'H': 'henry',
    '°C': 'degreecelsius',
    'lm': 'lumen',
    'lx': 'lux',
    'Bq': 'becquerel',
    'Gy': 'gray',
    'Sv': 'sievert',
    'kat': 'katal',
    '%': 'percent',
    'ppm': 'ppm',
    'B': 'byte',
    'bit': 'bit',
    'Å': 'angstrom',
    'bar': 'bar',
    'a.u. time': 'atomicunittime',
    'u': 'atomicmassunit',
    'b': 'barn',
    'c': 'clight',
    'm_e': 'electronmass',
    'e': 'elementarycharge',
    'mmHg': 'mmHg',
    'n.u. time': 'naturalunittime',
    'E_h': 'hartree',
    'a_0': 'bohr',
    'NM': 'nauticalmile',
    'kn': 'knot',
    'ħ': 'planckbar'
    # Add more units as needed
}

_dsiUnitsUTF8 = {
    'metre': 'm',
    'kilogram': 'kg',
    'second': 's',
    'ampere': 'A',
    'kelvin': 'K',
    'mole': 'mol',
    'candela': 'cd',
    'one': '1',
    'day': 'd',
    'hour': 'h',
    'minute': 'min',
    'degree': '°',
    'arcminute': '′',
    'arcsecond': '″',
    'gram': 'g',
    'radian': 'rad',
    'steradian': 'sr',
    'hertz': 'Hz',
    'newton': 'N',
    'pascal': 'Pa',
    'joule': 'J',
    'watt': 'W',
    'coulomb': 'C',
    'volt': 'V',
    'farad': 'F',
    'ohm': 'Ω',
    'siemens': 'S',
    'weber': 'Wb',
    'tesla': 'T',
    'henry': 'H',
    'degreecelsius': '°C',
    'lumen': 'lm',
    'lux': 'lx',
    'becquerel': 'Bq',
    'sievert': 'Sv',
    'gray': 'Gy',
    'katal': 'kat',
    'hectare': 'ha',
    'litre': 'l',
    'tonne': 't',
    'electronvolt': 'eV',
    'dalton': 'Da',
    'astronomicalunit': 'au',
    'neper': 'Np',
    'bel': 'B',
    'decibel': 'dB',
    'percent': '%',
    'ppm': 'ppm',
    'byte': 'B',
    'bit': 'bit',
    'angstrom': 'Å',
    'bar': 'bar',
    'atomicunittime': 'a.u. time',
    'atomicmassunit': 'u',
    'barn': 'b',
    'clight': 'c',
    'electronmass': 'mₑ',
    'elementarycharge': 'e',
    'mmHg': 'mmHg',
    'naturalunittime': 'n.u. time',
    'hartree': 'Eₕ',
    'bohr': 'a₀',
    'nauticalmile': 'NM',
    'knot': 'kn',
    'planckbar': 'ħ'
}

_derivedToBaseUnits = {
    # Time units
    'day': [('second', 1, 86400)],         # 1 day = 86400 seconds
    'hour': [('second', 1, 3600)],         # 1 hour = 3600 seconds
    'minute': [('second', 1, 60)],         # 1 minute = 60 seconds

    # Angle units
    'degree': [('radian', 1, pi/180)], # 1 degree = π/180 radians
    'arcminute': [('radian', 1, pi/10800)], # 1 arcminute = π/10800 radians
    'arcsecond': [('radian', 1, pi/648000)], # 1 arcsecond = π/648000 radians

    # Mass units
    'gram': [('kilogram', 1, 0.001)],  # 1 gram = 0.001 kilograms

    # Derived units
    'hertz': [('second', -1,1)],  # 1 Hz = 1/s
    'newton': [('kilogram', 1, 1), ('metre', 1, 1), ('second',-2, 1)],  # 1 N = 1 kg·m/s²
    'pascal': [('kilogram', 1, 1), ('metre',-1, 1), ('second',-2, 1)],  # 1 Pa = 1 kg/m·s²
    'joule': [('kilogram', 1, 1), ('metre',2, 1), ('second',-2, 1)],  # 1 J = 1 kg·m²/s²
    'watt': [('kilogram', 1, 1), ('metre',2, 1), ('second',-3, 1)],  # 1 W = 1 kg·m²/s³
    'coulomb': [('second', 1, 1), ('ampere', 1, 1)],  # 1 C = 1 s·A
    'volt': [('kilogram', 1, 1), ('metre',2, 1), ('second',-3, 1), ('ampere',-1, 1)],  # 1 V = 1 kg·m²/s³·A
    'farad': [('kilogram',-1, 1), ('metre',-2, 1), ('second', 4, 1), ('ampere',2, 1)],# 1 F = 1 kg⁻¹·m⁻²·s⁴·A²
    'ohm': [('kilogram', 1, 1), ('metre',2, 1), ('second',-3, 1), ('ampere',-2, 1)],  # 1 Ω = 1 kg·m²/s³·A⁻²
    'siemens': [('kilogram',-1, 1), ('metre',-2, 1), ('second',3, 1), ('ampere',2, 1)],# 1 S = 1 kg⁻¹·m⁻²·s³·A²
    'weber': [('kilogram', 1, 1), ('metre',2, 1), ('second',-2, 1), ('ampere',-1, 1)],  # 1 Wb = 1 kg·m²/s²·A
    'tesla': [('kilogram', 1, 1), ('second',-2, 1), ('ampere',-1, 1)],  # 1 T = 1 kg/s²·A
    'henry': [('kilogram', 1, 1), ('metre',2, 1), ('second',-2, 1), ('ampere',-2, 1)],  # 1 H = 1 kg·m²/s²·A²
    #'degreecelsius': [('kelvin', 1, 1)], # Degree Celsius is a scale, not a unit; the unit is Kelvin
    'lumen': [('candela', 1, 1), ('steradian', 1, 1)], # 1 lm = 1 cd·sr #TODO full conversion to base units
    'lux': [('candela', 1, 1), ('steradian', 1, 1), ('metre',-2, 1)], # 1 lx = 1 cd·sr/m² #TODO full conversion to base units
    'becquerel': [('second',-1, 1)], # 1 Bq = 1/s
    'sievert': [('metre',2, 1), ('second',-2, 1)], # 1 Sv = 1 m²/s²
    'gray': [('metre',2, 1), ('second',-2, 1)], # 1 Gy = 1 m²/s²
    'katal': [('mole', 1, 1), ('second',-1, 1)], # 1 kat = 1 mol/s
    # Other units
    'hectare': [('metre',2, 10000)],  # 1 ha = 10000 m²
    'litre': [('metre',3, 0.001)],  # 1 L = 0.001 m³
    'tonne': [('kilogram', 1, 1000)],  # 1 t = 1000 kg
    'electronvolt': [('joule', 1, 1.602176634e-19)],  # 1 eV = 1.602176634 × 10⁻¹⁹ J
    'dalton': [('kilogram', 1, 1.66053906660e-27)],  # 1 Da = 1.66053906660 × 10⁻²⁷ kg
    'astronomicalunit': [('metre', 1, 149597870700)],  # 1 AU = 149597870700 m
    'neper': [('one', 1,1)],  # Neper is a logarithmic unit for ratios of measurements, not directly convertible
    'bel': [('one', 1,1)],  # Bel is a logarithmic unit for ratios of power, not directly convertible
    'decibel': [('one', 1,1)],  # Decibel is a logarithmic unit for ratios of power, not directly convertible
    'angstrom': [('metre', 1, 1e-10)],# 1 Å = 1 × 10⁻¹⁰ m
    'bar': [('pascal', 1, 100000)],  # 1 bar = 100000 Pa
    'atomicunittime': [('second', 1, 2.4188843265864e-17)], # 1 a.u. time = 2.4188843265864e-17 s https://physics.nist.gov/cgi-bin/cuu/Value?aut
    'atomicmassunit': [('kilogram', 1, 1.66053906660e-27)], # 1 a.u. mass = 1.66053906660 × 10⁻²⁷ kg same as dalton
    'barn': [('metre', 2, 1e-28)],  # 1 barn = 1 × 10⁻²⁸ m²
    'clight': [('metre', 1, 299792458)],# 1 c = 299792458 m/s https://physics.nist.gov/cgi-bin/cuu/Value?c
    'electronmass': [('kilogram', 1, 9.1093837139e-31)],  # 1 m_e = 9.10938356 × 10⁻³¹ kg https://physics.nist.gov/cgi-bin/cuu/Value?me
    'elementarycharge': [('coulomb', 1, 1.602176634e-19)],  # 1 e = 1.602176634 × 10⁻¹⁹ C https://physics.nist.gov/cgi-bin/cuu/Value?e
    'mmHg': [('pascal', 1, 133.322387415)],  # 1 mmHg = 133.322387415 Pa
    'naturalunittime': [('second', 1, 1.28808866644e-21)],  # 1 natural unit of time = 1.28808866712 × 10⁻²¹ s https://physics.nist.gov/cgi-bin/cuu/Value?nut
    'hartree': [('joule', 1, 4.3597447222060e-18)],  # 1 Hartree = 4.3597447222071 × 10⁻¹⁸ J https://physics.nist.gov/cgi-bin/cuu/Value?hrj
    'bohr': [('metre', 1, 5.29177210903e-11)],  # 1 Bohr radius = 5.29177210903 × 10⁻¹¹ m https://physics.nist.gov/cgi-bin/cuu/CCValue?bohrrada0
    'planckbar': [('joule', 1, 1.054571817e-34), ('second', 1, 1)],  # 1 ħ 1.054 571 68 × 10⁻³⁴ J·s https://physics.nist.gov/cgi-bin/cuu/Value?Ahbar|search_for=atomic+unit+of+action
    'nauticalmile': [('metre', 1, 1852)],  # 1 nautical mile = 1852 m
    'knot': [('metre', 1, 1852/3600),('second',-1,1)],  # 1 knot = 1852/3600 m/s
    #'byte':[('bit',1,8)], ## TODO overthink this
# Note: For logarithmic units like neper, bel, and decibel, conversion to base units is not straightforward due to their nature.
}
_additionalConversions = {
    # Conversions for ampere, volt, and mole into kg, s, m equivalents
    'volt': [('metre', 2, 1), ('kilogram', 1, 1), ('second', -3, 1), ('ampere', -1, 1)],  # V = kg·m²/s³·A⁻¹
    'percent':[('one',1,0.01)],
    'ppm':[('one',1,1e-6)],
    'byte':[('one',1,8)],
    'bit':[('one',1,1)],
    # Note: These are placeholders and need to be adjusted to reflect accurate conversions.
}
_dsiKeyWords = {
    'tothe': r'\tothe',
    'per': r'\per'}
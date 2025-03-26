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
from unitStrings import _dsiPrefixesLatex, _dsiUnitsLatex

prefixes = list(_dsiPrefixesLatex.keys())
units = list(_dsiUnitsLatex.keys())

def generateRegex():
    # generate a regex that matches D-SI units
    dsiRegex = _getDsiRegex()
    nonDsiRegex = r'(\|.*)'
    return '^(' + dsiRegex + '|' + nonDsiRegex + ')$'

def generateListRegex():
    # generate a regex for a whitespace-separated list of D-SI units
    dsiRegex = _getDsiRegex()
    nonDsiRegex = r'(\|\S*)' # for the list, whitespace chars are not allowed in units
    unitRegex = '(' + dsiRegex + '|' + nonDsiRegex + ')'
    return '^(' + unitRegex + r'(\s' + unitRegex + ')*)$'

def _getDsiRegex():
    # These units can't have a prefix (R010, \one is treated separately in R014)
    noPrefixUnits = ['kilogram', 'decibel', 'degreecelsius', 'mmhg', 'minute', 'hour', 'day']
    noPrefixRegex = r'(' + _getUnitRegex(noPrefixUnits) + _getExponentRegex() + r')'

    # Can't enforce the second part of R010 because we don't know if \second\tothe{-1} is used for frequency or quantity of rotation
    
    # gram can't have prefix kilo (R011)
    caseKiloGramRegex = r'(' + _getPrefixRegex([prefix for prefix in prefixes if prefix not in ['kilo']]) + _getUnitRegex(['gram']) + _getExponentRegex() + r')'

    # bel can't have prefix deci (R012)
    caseDeciBelRegex = r'(' + _getPrefixRegex([prefix for prefix in prefixes if prefix not in ['deci']]) + _getUnitRegex(['bel']) + _getExponentRegex() + r')'

    # \one can't have prefix or exponent (R010 and R014)
    caseOneRegex = _getUnitRegex(['one'])

    # all other cases
    defaultPrefixRegex = _getPrefixRegex(prefixes)
    defaultUnitRegex = _getUnitRegex([unit for unit in units if unit not in noPrefixUnits + ['gram', 'bel', 'one']])
    defaultExponentRegex = _getExponentRegex()

    defaultRegex = r'(' + defaultPrefixRegex + defaultUnitRegex + defaultExponentRegex + r')'

    dsiRegexWithoutPer = r'(' + '|'.join([
        noPrefixRegex,
        caseKiloGramRegex,
        caseDeciBelRegex,
        caseOneRegex,
        defaultRegex,
    ]) + ')+'

    dsiRegex = r'(' + dsiRegexWithoutPer + r'(\\per' +dsiRegexWithoutPer+ r')?' + r')'
    return dsiRegex
    

def _getPrefixRegex(prefixes: list):
    return '(' + '|'.join([r'(\\' + item + ')' for item in prefixes]) + ')?'

def _getUnitRegex(units: list):
    return r'(' + '|'.join([r'(\\' + item + ')' for item in units]) + ')'

def _getExponentRegex():
    return r'(\\tothe\{-?\d+(\.\d+)?\})?'
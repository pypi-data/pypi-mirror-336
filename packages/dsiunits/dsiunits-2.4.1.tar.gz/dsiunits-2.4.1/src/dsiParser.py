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
import re
import warnings
from fractions import Fraction
import difflib

from unitStrings import _dsiPrefixesLatex, _dsiUnitsLatex, _dsiKeyWords
from dsiUnitNode import dsiUnitNode


class NonDsiUnitWarning(RuntimeWarning):
    """Raised when a correctly marked non-D-SI unit is parsed
    """
    pass


class dsiParser:
    _instance = None
    __dsiVersion = "2.2.0"
    __dsiSchemaUrl = "https://www.ptb.de/si/v2.2.0/SI_Format.xsd"
    __dsiRepositoryURL = "https://gitlab1.ptb.de/d-ptb/d-si/xsd-d-si"

    _defaults = {
        'createPerByDivision': True,
        'maxDenominator': 10000,
        '_latexDefaultWrapper': '$$',
        '_latexDefaultPrefix': '',
        '_latexDefaultSuffix': '',
    }

    """Parser to parse D-SI unit string into a tree"""

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(dsiParser, cls).__new__(cls)
            # Initialize configuration options
            for key, value in cls._defaults.items():
                setattr(cls._instance, key, value)
        return cls._instance

    def __init__(self):
        """
        Args:
            latexDefaultWrapper (str, optional): String to be added both in the beginning and the end of the LaTeX string. Defaults to '$$'.
            latexDefaultPrefix (str, optional): String to be added in the beginning of the LaTeX string, after the wrapper. Defaults to ''.
            latexDefaultSuffix (str, optional): String to be added in the end of the LaTeX string, before the wrapper. Defaults to ''.
        """
        pass

    def parse(self, dsiString: str):
        """Parses a D-SI string into a tree structure.

        Args:
            dsiString (str): D-SI unit raw string

        Raises:
            RuntimeWarning: Double backslashes in D-SI string
            RuntimeWarning: Empty D-SI string

        Returns:
            dsiTree: dsiTree object containing the D-SI unit
        """
        warningMessages = []
        if len(dsiString) > 0 and dsiString[0] == '|':
            warnings.warn("Parsing a correctly marked non D-SI unit!", NonDsiUnitWarning)
            return (dsiString[1:], [[dsiUnitNode('', dsiString[1:], valid=False)]], [], True)
        # Catch any double (triple...) \ before they annoy us
        while r'\\' in dsiString:
            warningMessages.append(
                _warn(f"Double backslash found in string, treating as one backslash: «{dsiString}»", RuntimeWarning))
            dsiString = dsiString.replace(r'\\', '\\')

        if dsiString == "":
            warningMessages.append(_warn("Given D-SI string is empty!", RuntimeWarning))
            return (
                'NULL',
                [[dsiUnitNode('', 'NULL', valid=False)]],
                warningMessages,
                True  # nonDsiUnit
            )

        tree = []
        (tree, fractionWarnings) = self._parseDsiFraction(dsiString)
        warningMessages += fractionWarnings
        for i, node in enumerate(tree):
            (tree[i], fractionlessWarnings) = self._parseFractionlessDsi(node)
            warningMessages += fractionlessWarnings
        return (
            dsiString,
            tree,
            warningMessages,
            False  # nonDsiUnit
        )

    def _parseDsiFraction(self, dsiString: str):
        """Parses D-SI fraction into list of fraction elements.

        Args:
            dsiString (str): D-SI unit raw string

        Raises:
            RuntimeWarning: String must not contain more than one "per",
                            as defined in the D-SI specs

        Returns:
            list: Strings separated by the "per"
            list: Warning messages of problems encountered while parsing
        """
        tree = []
        warningMessages = []
        dsiStringWOperCent = dsiString.replace('percent',
                                               'prozent')  # rename percent to prozent to have it not split at per ....
        tree = dsiStringWOperCent.split(r"\per")
        for i, subtree in enumerate(tree):
            tree[i] = tree[i].replace('prozent', 'percent')
        for subtree in tree:
            if len(subtree) == 0:
                warningMessages.append(_warn(r"The dsi string contains a \per missing a numerator or denominator! " +
                                             f"Given string: {dsiString}",
                                             RuntimeWarning))
                tree.remove(subtree)
        if len(tree) > 2:
            warningMessages.append(_warn(r"The dsi string contains more than one \per, does not " +
                                         f"match specs! Given string: {dsiString}",
                                         RuntimeWarning))
        return (tree, warningMessages)

    def _parseFractionlessDsi(self, dsiString: str):
        """Parses D-SI unit string without fractions.

        Args:
            dsiString (str): D-SI unit raw string, not containing any fractions

        Raises:
            RuntimeWarning: If string does not meet the specs

        Returns:
            list: List of nodes
            list: Warning messages of problems encountered while parsing
        """
        warningMessages = []
        items = dsiString.split("\\")
        if items[0] == '':  # First item of List should be empty, remove it
            items.pop(0)
        else:
            warningMessages.append(
                _warn(f"String should start with \\, string given was «{dsiString}»", RuntimeWarning))
        nodes = []

        (prefix, unit, exponent) = ('', '', '')
        valid = True
        item = items.pop(0)
        while True:
            if item in _dsiPrefixesLatex:
                prefix = item
                try:
                    item = items.pop(0)
                except IndexError:
                    item = ''
            if item in _dsiUnitsLatex:
                unit = item
                try:
                    item = items.pop(0)
                except IndexError:
                    item = ''
            if re.match(r'tothe\{[^{}]*\}', item):  # used to be elif
                exponentStr = item.split('{')[1].split('}')[0]
                try:
                    exponent = Fraction(exponentStr).limit_denominator()
                except ValueError:
                    warningMessages.append(_warn(f"The exponent «{exponent}» is not a number!", RuntimeWarning))
                    valid = False
                    exponent = exponentStr
                try:
                    item = items.pop(0)
                except IndexError:
                    item = ''
            if (prefix, unit, exponent) == ('', '', ''):
                unit = item
                try:
                    item = items.pop(0)
                except IndexError:
                    item = ''
                closestMatches = _getClosestStr(unit)
                if len(closestMatches) > 0:
                    closestMatchesStr = ', \\'.join(closestMatches)
                    closestMatchesStr = '\\' + closestMatchesStr
                    warningMessages.append(_warn(
                        fr"The identifier «{unit}» does not match any D-SI units! Did you mean one of these «{closestMatchesStr}»?",
                        RuntimeWarning))
                    valid = False
                else:
                    warningMessages.append(
                        _warn(fr"The identifier «{unit}» does not match any D-SI units!", RuntimeWarning))
                    valid = False
            elif unit == '':
                itemStr = ""
                if prefix != "":
                    itemStr = itemStr + "\\" + prefix
                if exponentStr != "":
                    itemStr = itemStr + r"\tothe{" + str(exponentStr) + r"}"
                warningMessages.append(
                    _warn(f"This D-SI unit seems to be missing the base unit! «{itemStr}»", RuntimeWarning))
                valid = False
            nodes.append(dsiUnitNode(prefix, unit, exponent, valid=valid))
            if (len(items) == 0) and (item == ''):
                break
            (prefix, unit, exponent) = ('', '', '')
            valid = True
        return (nodes, warningMessages)

    def _dsiStrFromNodes(self, nodeList):
        """Converts a list of nodes to a D-SI string."""
        dsiStr = ""
        for i, unitFraction in enumerate(nodeList):
            if i > 0:
                dsiStr += r"\per"
            for node in unitFraction:
                dsiStr += str(node)
        return dsiStr

    def info(self):
        infoStr = "D-SI Parser Version: " + str(self) + " using D-SI Schema Version: " + str(
            self.__dsiVersion) + " from: " + str(self.__dsiRepositoryURL) + " using D-SI Schema: " + str(
            self.__dsiSchemaUrl)
        print(infoStr)
        return (infoStr, self.__dsiVersion, self.__dsiSchemaUrl, self.__dsiRepositoryURL)

    def resetToDefaults(self):
        for key, value in self._defaults.items():
            setattr(self, key, value)

def _warn(message: str, warningClass):
    """Output warning on command line and return warning message

    Args:
        message (str): warning message
        warningClass: Warning type

    Returns:
        str: message
    """
    warnings.warn(message, warningClass)
    return message

def _getClosestStr(unknownStr):
    """returns the closest string and type of the given string

    Args:
        unknownStr (str): string to be compared

    Returns:
        str: closest string
        str: type of closest string
    """
    possibleDsiKeys = _dsiPrefixesLatex.keys() | _dsiUnitsLatex.keys() | _dsiKeyWords.keys()
    closestStr = difflib.get_close_matches(unknownStr, possibleDsiKeys, n=3,cutoff=0.66)
    return closestStr
# This file is part of dsiUnits (https://gitlab1.ptb.de/digitaldynamicmeasurement/dsiUnits/)
# Copyright 2024 [Benedikt Seeger(PTB), Vanessa Stehr(PTB)]
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
import warnings
from typing import List
import math
from fractions import Fraction

from unitStrings import (
    _dsiPrefixesLatex,
    _dsiPrefixesScales,
    _dsiUnitsLatex,
    _derivedToBaseUnits,
    _additionalConversions,
)


class dsiUnitNode:
    """one node of the D-SI tree, containing prefix, unit, power"""

    dsiParserInstance = None  # this class variable will stored the dsiParserInstance obtained from the singleton constructed
    # by the initialize_parser() class method by lazy loading so the instance is created when
    # the first node is created and not before dsiParser is fully defined

    @classmethod
    def initialize_parser(cls):
        from dsiParser import dsiParser

        cls.dsiParserInstance = dsiParser()

    def __init__(
        self,
        prefix: str,
        unit: str,
        exponent: Fraction = Fraction(1),
        valid: bool = True,
        scaleFactor: float = 1.0,
    ):  # Adding scale factor with default value 1.0
        if dsiUnitNode.dsiParserInstance is None:
            dsiUnitNode.initialize_parser()
        self.prefix = prefix
        self.unit = unit
        self.valid = valid
        if isinstance(exponent, Fraction) or isinstance(exponent, int):
            self.exponent = Fraction(exponent)
        if isinstance(exponent, str):
            if exponent == "":
                exponent = Fraction(1)
            else:
                try:
                    exponent = Fraction(exponent).limit_denominator(
                        self.dsiParserInstance.maxDenominator
                    )
                except ValueError:
                    exponent = exponent
                    warnings.warn(
                        f"Exponent «{exponent}» is not a number!", RuntimeWarning
                    )
        self.exponent = exponent
        self.scaleFactor = scaleFactor  # Adding scale factor with default value 1.0

    def toLatex(self):
        """generates a latex string from a node

        Returns:
            str: latex representation
        """
        latexString = ""
        if self.prefix:
            latexString += _dsiPrefixesLatex[self.prefix]
        try:
            latexString += _dsiUnitsLatex[self.unit]
        except KeyError:
            latexString += r"{\color{red}\mathrm{" + self.unit + r"}}"
            if self.valid == True:
                raise RuntimeError(
                    "Found invalid unit in valid node, this should not happen! Report this incident at: https://gitlab1.ptb.de/digitaldynamicmeasurement/dsiUnits/-/issues/new"
                )
        if isinstance(self.exponent, str):
            # exponent is str this shouldn't happen!
            latexString += r"^{{\color{red}\mathrm{" + self.exponent + r"}}}"
            if self.valid == True:
                raise RuntimeError(
                    "Found invalid unit in valid node, this should not happen! Report this incident at: https://gitlab1.ptb.de/digitaldynamicmeasurement/dsiUnits/-/issues/new"
                )
        elif self.exponent != 1:
            if not self.exponent.denominator == 1:  # exponent is not an integer
                if self.exponent.denominator == 2:  # square root
                    latexString = r"\sqrt{" + latexString
                else:  # higher roots need an extra argument
                    latexString = (
                        r"\sqrt[" + str(self.exponent.denominator) + "]{" + latexString
                    )
                    if (
                        self.exponent.numerator != 1
                    ):  # keep anything in the numerator of the exponent in the exponent
                        latexString += "^{" + str(self.exponent.numerator) + "}"
                latexString += r"}"

            else:
                latexString += r"^{" + str(self.exponent) + r"}"

        if self.unit == "":
            latexString = r"{\color{red}" + latexString + r"}"
            if self.valid == True:
                raise RuntimeError(
                    "Found invalid unit in valid node, this should not happen! Report this incident at: https://gitlab1.ptb.de/digitaldynamicmeasurement/dsiUnits/-/issues/new"
                )

        return latexString

    def toBaseUnits(self, complete=False) -> List["dsiUnitNode"]:
        """
        Converts this node to its base unit representation.
        Adjusts the scale factor during the conversion. Optionally resolves to kg, s, and m units,
        including converting ampere, volt, and mole to their kg, s, and m equivalents when kgs is True.

        Args:
            kgs (bool): If true, also resolves volt to kg, s, and m units.

        Returns:
            List['dsiUnitNode']: List of nodes representing the base units or kg, s, m equivalents.
        """
        # Adjust the scale factor for the prefix
        prefixScale = _dsiPrefixesScales.get(
            self.prefix, 1
        )  # Default to 1 if no prefix
        adjustedScaleFactor = self.scaleFactor * prefixScale**self.exponent

        # Convert to base units if it's a derived unit
        if self.unit in _derivedToBaseUnits:
            baseUnitsInfo = _derivedToBaseUnits[self.unit]
            baseUnits = []
            for i, (baseUnit, exponent, scaleFactor) in enumerate(baseUnitsInfo):
                # Apply the adjusted scale factor only to the first base unit
                finalScaleFactor = (
                    math.pow(adjustedScaleFactor * scaleFactor, self.exponent)
                    if i == 0
                    else 1.0
                )
                baseUnits.append(
                    dsiUnitNode(
                        "",
                        baseUnit,
                        exponent * self.exponent,
                        scaleFactor=finalScaleFactor,
                    )
                )
            return baseUnits
        elif complete:
            # Additional logic for converting ampere, volt, and mole to kg, s, and m equivalents
            if self.unit in _additionalConversions:
                kgsUnitsInfo = _additionalConversions[self.unit]
                kgsUnits = []
                for i, (kgsUnit, exponent, scaleFactor) in enumerate(kgsUnitsInfo):
                    finalScaleFactor = (
                        math.pow(adjustedScaleFactor * scaleFactor, self.exponent)
                        if i == 0
                        else 1.0
                    )
                    kgsUnits.append(
                        dsiUnitNode(
                            "",
                            kgsUnit,
                            exponent * self.exponent,
                            scaleFactor=finalScaleFactor,
                        )
                    )
                return kgsUnits

        # Return the node as is if it's already a base unit, with adjusted scale factor
        return [
            dsiUnitNode("", self.unit, self.exponent, scaleFactor=adjustedScaleFactor)
        ]

    def __eq__(self, other):
        """Checks if two nodes are identical after sorting their nodes alphabetically."""
        return (
            self.prefix == other.prefix
            and self.unit == other.unit
            and self.exponent == other.exponent
            and self.scaleFactor == other.scaleFactor
        )

    def __str__(self):
        result = ""

        if self.prefix != "":
            result += "\\" + self.prefix
        result = result + "\\" + self.unit
        if self.exponent != 1:
            result = result + r"\tothe{" + "{:g}".format(float(self.exponent)) + "}"
        return result

    def isScaled(self, other):
        """Checks if two nodes are scaled equal."""
        if self.unit == other.unit and self.exponent == other.exponent:
            return _dsiPrefixesScales[other.prefix]**other.exponent / _dsiPrefixesScales[self.prefix]**self.exponent
        else:
            return math.nan

    def removePrefix(self):
        """Removes the prefix from the node and adjusts the scale factor accordingly."""
        if self.prefix != "":
            self.scaleFactor = self.scaleFactor * _dsiPrefixesScales[self.prefix]
            self.scaleFactor = self.scaleFactor**self.exponent  # TODO check this
            self.prefix = ""
        return self

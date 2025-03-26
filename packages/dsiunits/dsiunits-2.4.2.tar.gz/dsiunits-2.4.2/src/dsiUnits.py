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
from __future__ import annotations  # for type annotation recursion
import re
import warnings
import difflib
from typing import List
from copy import deepcopy
import math
from fractions import Fraction
from decimal import Decimal, InvalidOperation
import numbers

from unitStrings import (
    _dsiPrefixesLatex,
    _dsiPrefixesScales,
    _dsiPrefixesUTF8,
    _dsiUnitsLatex,
    _dsiUnitsUTF8,
    _derivedToBaseUnits,
    _additionalConversions,
    _dsiKeyWords,
)
from dsiParser import NonDsiUnitWarning, dsiParser
from dsiUnitNode import dsiUnitNode

dsiParserInstance = dsiParser()


class dsiUnit:
    def __new__(cls, dsiString=None):
        # If the argument is already a dsiUnit instance, return it directly.
        if isinstance(dsiString, cls):
            return dsiString
        return super().__new__(cls)

    def __init__(self, dsiString: str):
        # Prevent reinitialization if this instance was already created.
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        try:
            parsedDsiUnit = dsiParserInstance.parse(dsiString)
            self.dsiString, self.tree, self.warnings, self.nonDsiUnit = parsedDsiUnit
            self.valid = len(self.warnings) == 0
            self.scaleFactor = 1.0
        except Exception as e:
            warnings.warn(str(e))
            self.dsiString = dsiString
            self.tree = []
            self.warnings = [str(e)]
            self.nonDsiUnit = False
            self.valid = False

    @classmethod
    def fromDsiTree(
        cls,
        dsiString: str,
        dsiTree=[],
        warningMessages=[],
        nonDsiUnit=False,
        scaleFactor=1.0,
    ):
        instance = cls.__new__(cls)
        if nonDsiUnit:
            dsiTree = [dsiString]
        elif dsiString == "" and dsiTree != []:
            dsiString = dsiParserInstance._dsiStrFromNodes(dsiTree)
        instance.dsiString = dsiString
        instance.tree = dsiTree
        instance.warnings = warningMessages
        instance.nonDsiUnit = nonDsiUnit
        instance.valid = len(warningMessages) == 0
        instance.scaleFactor = scaleFactor
        instance._initialized = True
        return instance

    def toLatex(self, wrapper=None, prefix=None, suffix=None):
        """converts D-SI unit string to LaTeX

        Args:
            wrapper (str, optional): String to be added both in the beginning and the end of the LaTeX string. Defaults to the value set in the parser object.
            prefix (str, optional): String to be added in the beginning of the LaTeX string, after the wrapper. Defaults to the value set in the parser object.
            suffix (str, optional): String to be added in the end of the LaTeX string, before the wrapper. Defaults to the value set in the parser object.

        Returns:
            str: the corresponding LaTeX code
        """

        # If no wrapper/prefix/suffix was given, set to the parser's default
        wrapper = dsiParserInstance._latexDefaultWrapper if wrapper == None else wrapper
        prefix = dsiParserInstance._latexDefaultPrefix if prefix == None else prefix
        suffix = dsiParserInstance._latexDefaultSuffix if suffix == None else suffix

        if self.tree == []:
            if len(prefix) + len(suffix) > 0:
                return wrapper + prefix + suffix + wrapper
            else:
                return ""
        if self.nonDsiUnit:
            if self.dsiString[0] != "|":
                latexString = r"\textpipe" + r"\mathrm{" + self.dsiString + r"}"
            else:
                latexString = r"\textpipe" + r"\mathrm{" + self.dsiString[1:] + r"}"
            return wrapper + prefix + latexString + suffix + wrapper
        latexArray = []
        if len(self.tree) == 1:  # no fractions
            for node in self.tree[0]:
                latexArray.append(node.toLatex())
            latexString = r"\,".join(latexArray)
        elif len(self.tree) == 2:  # one fraction
            latexString = ""
            latexString += r"\frac"
            for frac in self.tree:
                latexString += r"{"
                nodeArray = []
                for node in frac:
                    nodeArray.append(node.toLatex())
                latexString += r"\,".join(nodeArray)
                latexString += r"}"
        else:  # more than one fraction
            latexString = ""
            for i in range(len(self.tree)):
                nodeArray = []
                if i > 0:
                    latexString += r"{\color{red}/}"
                for node in self.tree[i]:
                    nodeArray.append(node.toLatex())
                latexString += r"\,".join(nodeArray)
        if self.scaleFactor != 1.0:
            latexString = str(self.scaleFactor) + r"\cdot" + latexString
        return wrapper + prefix + latexString + suffix + wrapper

    def toUTF8(self):
        """Converts D-SI unit string to a compact UTF-8 format."""

        def exponent_to_utf8(exp):
            """Converts numerical exponents to UTF-8 subscript."""
            # Mapping for common exponents to UTF-8
            superscripts = {
                "1": "¹",
                "2": "²",
                "3": "³",
                "4": "⁴",
                "5": "⁵",
                "6": "⁶",
                "7": "⁷",
                "8": "⁸",
                "9": "⁹",
                "0": "⁰",
                "-": "⁻",
                ".": "˙",
            }
            # Convert fractional exponents to a more readable format if needed
            return "".join(superscripts.get(char, char) for char in str(exp))

        if self.nonDsiUnit:
            if self.dsiString[0] != "|":
                return "|" + self.dsiString
            return self.dsiString
        utf8Array = []
        for unitFraction in self.tree:
            fractionUtf8Array = []
            for node in unitFraction:
                # Fetch UTF-8 unit representation
                unitStr = _dsiUnitsUTF8.get(
                    node.unit, "⚠" + node.unit + "⚠"
                )  # second arg is returned on itemError

                # Handle prefix (if any) and unit
                prefixStr = (
                    _dsiPrefixesUTF8.get(node.prefix, "⚠" + node.prefix + "⚠")
                    if node.prefix
                    else ""
                )
                utf8Str = (
                    f"{prefixStr}{unitStr}"  # Direct concatenation for compactness
                )

                # Handle exponent, converting to UTF-8 subscript, if not 1
                if node.exponent and node.exponent != 1:
                    utf8Str += exponent_to_utf8(node.exponent)

                fractionUtf8Array.append(utf8Str)

            # Join units within the same fraction with a dot for compactness
            utf8Array.append("".join(fractionUtf8Array))
        if self.scaleFactor != 1.0:
            scaleFactorStr = str(self.scaleFactor) + "*"
        else:
            scaleFactorStr = ""
        # Handle fractions, join numerator and denominator with a slash for division
        return scaleFactorStr + " / ".join(utf8Array).replace(" ", "")

    def toBaseUnitTree(self, complete=False):
        """
        Converts the entire D-SI tree to its base unit representation.
        """
        baseUnitTree = []
        for unitFraction in self.tree:
            baseFraction = []
            for node in unitFraction:
                baseFraction.extend(node.toBaseUnits())
            baseUnitTree.append(baseFraction)
        unconsolidatedTree = dsiUnit.fromDsiTree(
            dsiString=self.dsiString,
            dsiTree=baseUnitTree,
            warningMessages=self.warnings,
        )
        reduced = unconsolidatedTree.reduceFraction()
        # if kgms True we do a second round but resolve volt ampere mole this round
        if complete:
            baseUnitTree = []
            for unitFraction in self.tree:
                baseFraction = []
                for node in unitFraction:
                    baseFraction.extend(node.toBaseUnits(complete=complete))
                baseUnitTree.append(baseFraction)
            unconsolidatedTree = dsiUnit.fromDsiTree(
                dsiString=self.dsiString,
                dsiTree=baseUnitTree,
                warningMessages=self.warnings,
            )
            reduced = unconsolidatedTree.reduceFraction()
        return reduced

    def reduceFraction(self):
        """
        Creates a new _dsiTree instance with reduced fractions.
        - Consolidates nodes with the same base unit by multiplying scales and summing exponents.
        - Sorts the nodes alphabetically by unit.
        - The first node carries the overall scale factor.
        """
        if len(self.tree) > 2:
            raise RuntimeError(
                "D-SI tree with more than two fractions cannot be reduced."
            )

        consolidated_nodes = []

        # Handling single and two-node cases
        if len(self.tree) == 1:
            consolidated_nodes = self.tree[0]
        elif len(self.tree) == 2:
            # Copy nodes from the first fraction
            consolidated_nodes = [node for node in self.tree[0]]

            # Copy nodes from the second fraction, adjusting the exponents
            for node in self.tree[1]:
                # Inverting the exponent for nodes in the denominator
                invertedExponent = -1 * node.exponent
                fractionalScaleFactor = 1 / node.scaleFactor**node.exponent
                consolidated_nodes.append(
                    dsiUnitNode(
                        node.prefix,
                        node.unit,
                        invertedExponent,
                        scaleFactor=fractionalScaleFactor,
                    )
                )

        # Consolidating nodes with the same unit
        i = 0
        while i < len(consolidated_nodes):
            j = i + 1
            while j < len(consolidated_nodes):
                if consolidated_nodes[i].unit == consolidated_nodes[j].unit:
                    # Consolidate nodes
                    scaleFactor = (
                        consolidated_nodes[i].scaleFactor
                        * consolidated_nodes[j].scaleFactor
                    )
                    prefixScaleI = _dsiPrefixesScales[consolidated_nodes[i].prefix]
                    prefixScaleJ = _dsiPrefixesScales[consolidated_nodes[j].prefix]
                    combinedPrefixScale = prefixScaleI * prefixScaleJ
                    consolidated_nodes[i].prefix = (
                        ""  # we wont allow prefixes in consolidated nodes since we don't want to have prefixes in the base units
                    )
                    consolidated_nodes[i].scaleFactor *= (
                        consolidated_nodes[j].scaleFactor * combinedPrefixScale
                    )
                    if combinedPrefixScale != 1:
                        raise RuntimeError("Prefixes in base units are not allowed")
                    exponent = (
                        consolidated_nodes[i].exponent + consolidated_nodes[j].exponent
                    )
                    consolidated_nodes[i].exponent = exponent
                    del consolidated_nodes[j]
                else:
                    j += 1
            i += 1

        # Calculate overall scale factor and apply it to the first node
        overall_scale_factor = 1.0
        for node in consolidated_nodes:
            overall_scale_factor *= node.scaleFactor
        #    node.scaleFactor = 1.0  # Reset scale factor for individual nodes
        # Sort nodes alphabetically by unit
        consolidated_nodes.sort(key=lambda x: x.unit)
        nodesWOPowerZero = []
        for node in consolidated_nodes:
            if node.exponent != 0:
                nodesWOPowerZero.append(node)
        # ok all nodes have ben power of zero so we deleted them and end up with one or bytes or bits as unit and 1.0 as exponent
        if len(nodesWOPowerZero) == 0:
            hadBytes = False
            haBits = False
            for fraction in self.tree:
                for node in fraction:
                    if node.unit == "byte":
                        hadBytes = True
                    if node.unit == "bit":
                        haBits = True
            if hadBytes and haBits:
                raise RuntimeError(
                    "Can't have bytes and bits in the same unit this should have been consolidated already in the parser"
                )
            if hadBytes:
                nodesWOPowerZero.append(
                    dsiUnitNode("", "byte", 1.0, scaleFactor=overall_scale_factor)
                )
            elif haBits:
                nodesWOPowerZero.append(
                    dsiUnitNode("", "bit", 1.0, scaleFactor=overall_scale_factor)
                )
            else:
                nodesWOPowerZero.append(
                    dsiUnitNode("", "one", 1.0, scaleFactor=overall_scale_factor)
                )
        consolidated_nodes = nodesWOPowerZero
        # Check for ones and delete them if they are not the only node ad set there exponent to 1.0 since 1^x = 1
        if len(consolidated_nodes) > 1:
            consolidated_nodes = [
                node for node in consolidated_nodes if node.unit != "one"
            ]
        else:
            if consolidated_nodes[0].unit == "one":
                consolidated_nodes[0].exponent = 1.0
        # Create and return a new instance of _dsiTree with consolidated nodes
        return dsiUnit.fromDsiTree(
            dsiString=self.dsiString,
            dsiTree=[consolidated_nodes],
            warningMessages=self.warnings,
            nonDsiUnit=False,
            scaleFactor=overall_scale_factor,
        )

    def _removePer(self):
        if len(self.tree) == 2:
            for i, node in enumerate(self.tree[1]):
                # invert exponent node.
                node.exponent = node.exponent * -1
                self.tree[0].append(node)
                self.tree[1].pop(i)
            self.tree.pop(1)

    def negExponentsToPer(self):
        """Converts negative exponents to the denominator of the fraction."""
        for node in self.tree[0]:  # numerator
            if node.exponent < 0:
                node.exponent = -node.exponent
                node.scaleFactor = 1 / node.scaleFactor
                try:
                    self.tree[1].append(
                        dsiUnitNode(
                            "", node.unit, node.exponent, scaleFactor=node.scaleFactor
                        )
                    )
                except (
                    IndexError
                ):  # if we have only the numerator list we need to add the denominator list
                    self.tree.append(
                        [
                            dsiUnitNode(
                                "",
                                node.unit,
                                node.exponent,
                                scaleFactor=node.scaleFactor,
                            )
                        ]
                    )
                self.tree[0].remove(node)
        if (
            len(self.tree) == 2
        ):  # we have a numerator and a denominator so we must treat the denominator as well
            for node in self.tree[1]:  # numerator
                if node.exponent < 0:
                    node.exponent = -node.exponent
                    node.scaleFactor = 1 / node.scaleFactor
                    self.tree[0].append(
                        dsiUnitNode(
                            "", node.unit, node.exponent, scaleFactor=node.scaleFactor
                        )
                    )
                    self.tree[1].remove(dsiUnitNode)
        if len(self.tree[0]) == 0:
            self.tree[0].append(dsiUnitNode("", "one", 1.0))
        return self

    def sortTree(self):
        """Sorts each fraction's nodes alphabetically by their units."""
        for unitFraction in self.tree:
            unitFraction.sort(key=lambda node: node.unit)

    def __eq__(self, other):
        """Checks if two D-SI trees are identical after sorting their nodes alphabetically."""
        if not isinstance(other, dsiUnit):
            return False
        if self.nonDsiUnit or other.nonDsiUnit:
            return self.tree == other.tree
        # Sort both trees before comparison
        selfCopy = deepcopy(self)
        otherCopy = deepcopy(other)
        selfCopy.sortTree()
        otherCopy.sortTree()
        if selfCopy.tree == otherCopy.tree:
            return True
        else:
            selfCopy._removePer()
            otherCopy._removePer()
            if selfCopy.tree == otherCopy.tree:
                return True
            else:
                return False

    def getScaleFactor(self, other: dsiUnit) -> float:
        """Get the factor with which the units can be converted into each other. x self == 1 other.

        Args:
            other (dsiUnit): Unit to compare against

        Returns:
            float: scale factor. scale factor * self == 1 * other
        """
        scaleFactor, baseUnit = self._calculateScaleFactorAndCommonUnit(
            other, complete=True
        )
        return scaleFactor

    def isScalable(self, other: dsiUnit) -> bool:
        """returns whether the two units can be converted into each other.

        Args:
            other (dsiUnit): Unit to compare against

        Returns:
            bool: whether the two units can be converted into each other
        """
        return bool(self.getScaleFactor(other))

    def getBaseUnit(self, other: dsiUnit) -> dsiUnit:
        """Get the common base unit for the two units, if it exists

        Args:
            other (dsiUnit): Unit to compare against

        Returns:
            dsiUnit: common base unit
        """
        scaleFactor, commonUnit = self._calculateScaleFactorAndCommonUnit(
            other, complete=True
        )
        if not commonUnit: # Check if commonUnit is None
            return None
        baseUnit = commonUnit.reduceFraction()
        baseUnit.tree[0][
            0
        ].scaleFactor = 1.0  # TODO: check if this should be a Fraction
        return baseUnit

    def isScalablyEqualTo(self, other, complete=False):
        """
        Checks if two D-SI units are scalably equal and returns the scale factor and base unit, without modifying
        the units involved.

        Args:
            other (dsiUnit): The other D-SI unit to compare against.
            complete (bool): A flag to determine whether or not the units should be resolved completely to base units.

        Returns:
            (float, dsiUnit):
                - A tuple containing the scale factor as a float. If the units are not scalable, returns math.nan.
                - The second element is the base unit of the calling object or None if not scalable.

        Behavior:
            - First, it checks if `other` is of type `dsiUnit`. If not, it returns math.nan and None.
            - It sorts and compares the two trees. If they are identical, it returns a scale factor of 1.0 and the calling unit.
            - If they are not identical, it attempts to compute the scale factor by iterating through the tree nodes and checking for scaling relationships.
            - If direct comparison fails and complete == True, it converts both trees to their base unit representations, sorts them, and attempts to compute a scaling factor in the base units.
        Raises:
            RuntimeError: If there are multiple fractions in the base unit trees during comparison.
        """
        warnings.warn(
            "This function is deprecated. Please use one of the following functions instead: getScaleFactor, isScalable, getBaseUnit",
            DeprecationWarning,
        )
        return self._calculateScaleFactorAndCommonUnit(other, complete=complete)

    def _calculateScaleFactorAndCommonUnit(self, other, complete=False):
        if not isinstance(other, dsiUnit):
            return (math.nan, None)

        sortedSelf = deepcopy(self)
        sortedSelf.sortTree()
        sortedOther = deepcopy(other)
        sortedOther.sortTree()
        # okay now check if is identical
        if sortedSelf.tree == sortedOther.tree:
            return (1.0, self)
        scaleFactor = 1
        for fracIdx, unitFraction in enumerate(sortedSelf.tree):
            try:
                if len(unitFraction) != len(sortedOther.tree[fracIdx]):
                    scaleFactor = math.nan
                    break
                for nodeIDX, node in enumerate(unitFraction):
                    scaleFactor *= node.isScaled(sortedOther.tree[fracIdx][nodeIDX])
            except IndexError:
                # if we get here we have a fraction in one tree that is not in the other in this case we resolve to base units and compare
                scaleFactor = math.nan
                break
        if not math.isnan(scaleFactor):
            return (scaleFactor, self)
        # Convert both trees to their base unit representations
        selfBaseUnitTree = self.toBaseUnitTree(complete=complete)
        otherBaseUnitTree = other.toBaseUnitTree(complete=complete)

        # Sort both trees
        selfBaseUnitTree.sortTree()
        otherBaseUnitTree.sortTree()
        # Check if units match
        if len(selfBaseUnitTree.tree) != len(otherBaseUnitTree.tree):
            return (math.nan, None)
        # Calculate scale factor
        scaleFactor = 1.0
        if len(selfBaseUnitTree.tree) != 1 or len(otherBaseUnitTree.tree) != 1:
            raise RuntimeError(
                "D-SI tree with more than one fraction cannot be compared. And should not exist here since we consolidated earlier"
            )
        for selfNode, otherNode in zip(
            selfBaseUnitTree.tree[0], otherBaseUnitTree.tree[0]
        ):
            if selfNode.unit != otherNode.unit:
                return (math.nan, None)
            if selfNode.exponent != otherNode.exponent:
                return (math.nan, None)
            scaleFactor *= otherNode.scaleFactor / selfNode.scaleFactor
        # resetting scaleFactor to 1.0
        scaleFactor = otherBaseUnitTree.scaleFactor / selfBaseUnitTree.scaleFactor
        # TODO check resetting the scale factors of the base units is a good idea ... but we calculated the scale factor and returned it so it should be fine
        selfBaseUnitTree.scaleFactor = 1.0
        for fraction in selfBaseUnitTree.tree:
            for node in fraction:
                node.scaleFactor = 1.0
        return (scaleFactor, selfBaseUnitTree)

    def __str__(self):
        result = ""
        if self.nonDsiUnit:
            if self.dsiString[0] != "|":
                return "|" + self.dsiString
            return self.dsiString
        if self.scaleFactor != 1.0:
            result += str(self.scaleFactor) + "*"
        for node in self.tree[0]:
            result += str(node)
        if len(self.tree) == 2:
            result += r"\per"
            for node in self.tree[1]:
                result += str(node)
        return result

    def __hash__(self):
        # Use the hash of an immutable attribute (here, self.value)
        return hash(str(self))

    def __repr__(self):
        contentStr = self.toUTF8()
        if not self.valid:
            contentStr += "INVALIDE"
        if self.warnings:
            contentStr += f" {len(self.warnings)} WARNINGS"
        # Simple representation: class name and D-SI string
        return f"{contentStr}"

    def __pow__(self, other):
        if not isinstance(other, numbers.Real):
            raise TypeError("Exponent must be a real number")
        if self.nonDsiUnit:
            raise RuntimeError("Can't do math with non-DSI units")
        resultNodeLIst = deepcopy(self.tree)
        for unitFraction in resultNodeLIst:
            for node in unitFraction:
                node.removePrefix()
                exponent = node.exponent * other
                node.exponent *= Fraction(exponent).limit_denominator(
                    dsiParserInstance.maxDenominator
                )
                node.scaleFactor **= other
        resultTree = dsiUnit.fromDsiTree(
            dsiString="", dsiTree=resultNodeLIst, warningMessages=self.warnings
        )
        resultTree = resultTree.reduceFraction()
        if len(self.tree) == 2:  # check if we had a per representation
            resultTree.negExponentsToPer()
        return resultTree

    def __mul__(self, other):
        if self.nonDsiUnit or other.nonDsiUnit:
            raise RuntimeError("Can't do math with non-DSI units")
        if len(self.tree) + len(other.tree) > 2:
            convertToPer = True
        else:
            convertToPer = False
        resultNodeLIst = deepcopy(self.tree)
        for i, unitFraction in enumerate(other.tree):
            if i > 1:
                raise RuntimeError(
                    "D-SI tree with more than one fraction cannot be multiplied"
                )
            try:
                resultNodeLIst[i].extend(deepcopy(unitFraction))
            except IndexError:
                resultNodeLIst.append(
                    deepcopy(unitFraction)
                )  # there was no fraction so we add it
        for fractionComponents in resultNodeLIst:
            for node in fractionComponents:
                node.removePrefix()
        resultTree = dsiUnit.fromDsiTree(
            dsiString="", dsiTree=resultNodeLIst, warningMessages=self.warnings
        )
        resultTree = resultTree.reduceFraction()
        if convertToPer:
            resultTree = resultTree.negExponentsToPer()
        return resultTree

    def __truediv__(self, other):
        if self.nonDsiUnit or other.nonDsiUnit:
            raise RuntimeError("Can't do math with non-DSI units")
        if dsiParserInstance.createPerByDivision:
            return (self * (other**-1)).negExponentsToPer()
        else:
            return self * (other**-1)

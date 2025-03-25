# D-SI Parser

This library converts D-SI unit strings to Latex.
And is able to perform math operations *, / and power with the D-SI units as well as checken weather teh can be converted into each other with scalar multiplication


## Javascript version

The folder [dsiUnits-js](/dsiUnits-js) contains an Javascript version of this libary that can be used for a D-SI-Unit-Input Element with autosugestion. And a dsiUnit CLass that supports parsing and rendering (HTML converion) of the dsi Units. 

## Installation

```bash
pip install dsiUnits
```

## Usage
The Constructor `dsiUnit(str)` will parse the string and create a dsiUnit object.
The dsiUnit object has the following methods:
- `toLatex()`: returns the Latex representation of the unit
- `toUTF8()`: returns the UTF8 representation of the unit
- `isScalablyEqualTo(other)`: checks whether the unit is equal to another unit with scalar multiplication
  
And following magic functions: 
- `__mul__(other)`: "*" multiplies the unit with another unit or a scalar
- `__truediv__(other)`: "/" divides the unit by another unit or a scalar
- `__pow__(other)`: "**" raises the unit to the power of another unit or a scalar
- `__eq__(other)`: "==" checks whether the unit is equal to another unit
- `__str__`: "str()" returns the string representation of the unit
- `__repr__`: returns the string representation of the unit

- `toBaseUnitTree()`: returns the base unit tree of the unit
- `reduceFraction()`: reduces the fraction of the unit by resolving all `\per` and combining same units by exponent addition 
- `sortTree()`: sorts the base unit tree of the unit
- 
```python
from dsiUnits import dsiUnit

unit = dsiUnit('\metre\second\tothe{-1}')
latexStr=unit.toLatex()
print(latexStr)
```

```python
from dsiUnits import dsiUnit

mps = dsiUnit(r'\metre\second\tothe{-1}')
kmh = dsiUnit(r'\kilo\metre\per\hour')
scaleFactor, baseUnit = mps.isScalablyEqualTo(kmh)
print("The unit "+str(mps)+" is equal to "+str(kmh)+" with a factor of "+scaleFactor+" and base unit "+str(baseUnit))
```

For more usage examples see the [Example Notebook](https://gitlab1.ptb.de/digitaldynamicmeasurement/dsiUnits/-/blob/main/doc/examples.ipynb),
as well as the [pytest file](https://gitlab1.ptb.de/digitaldynamicmeasurement/dsiUnits/-/blob/main/src/dsiUnits.py).


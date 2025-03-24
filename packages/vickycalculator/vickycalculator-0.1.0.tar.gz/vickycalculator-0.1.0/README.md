# vickycalculator

**vickycalculator** is a Python package that provides a handful of basic math operations—`add`, `subtract`, `multiply`, and `divide`. Perfect for simple arithmetic in your scripts or notebooks.

## Installation

You can install the latest release directly from [PyPI](https://pypi.org/) using `pip`:

```bash
pip install vickycalculator
```

## Usage

```python
import vickycalculator

print(vickycalculator.add(10, 5))       # 15
print(vickycalculator.subtract(10, 5))  # 5
print(vickycalculator.multiply(10, 5))  # 50
print(vickycalculator.divide(10, 5))    # 2.0
```

### Example
```python
import vickycalculator

a, b = 12, 3
sum_result      = vickycalculator.add(a, b)
difference      = vickycalculator.subtract(a, b)
product         = vickycalculator.multiply(a, b)
quotient        = vickycalculator.divide(a, b)

print(f"{a} + {b} = {sum_result}")
print(f"{a} - {b} = {difference}")
print(f"{a} x {b} = {product}")
print(f"{a} / {b} = {quotient}")
```
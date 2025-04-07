# CLI Calculator

A command-line calculator project built with Python.

## Installation

1. Ensure you have Poetry installed.
2. Clone the repository:

```bash
git clone <repository-url>
cd cli-calculator
```

3. Install dependencies:

```bash
make install-dev
```

## Usage

Run the calculator with the default expression:
make run
Run with a custom expression:

```bash
make run EXPR='"2*3+4"'
```

Enable support for very large numbers:

```bash
make run ALLOW_INF=true EXPR='"1e1000 + 1"'
```

Use degrees for trigonometric functions:

```bash
make run USE_DEG=true EXPR='"sin(90)"'
```

The calculator accepts basic arithmetic operations (addition, subtraction, multiplication, division) and can be extended to support more advanced functions.

## Documentation

Display CLI documentation:

```bash
make doc
```

 # Topsis Implementation

It is A Python package [(Click here)](https://pypi.org/project/Topsis-Raj-102217077/) to implement the Technique for Order of Preference by Similarity to Ideal Solution (Topsis) method.

## Installation

```python
pip install Topsis-Raj-102217077
```

## Usage
Run the TOPSIS analysis using the command-line interface:

```python
topsis <InputDataFile> <Weights> <Impacts> <ResultFileName>
```

## Example
Suppose you have a CSV file 102217077-data.csv containing a decision matrix where:

The first column is the identifier for alternatives.
The subsequent columns contain numeric data for each criterion.

If you want to apply TOPSIS with weights [1, 1, 1, 2, 1] and impacts [+, +, -, +, +], use:

```python
python -m topsis_raj_102217077.topsis 102217077-data.csv "1,1,1,2,1" "+,+,-,+,+" 102217077-result.csv
```
This will generate a result file result.csv with the calculated TOPSIS scores and rankings.

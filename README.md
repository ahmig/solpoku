# solpoku

a sudoku solver using [integer linear programming](https://en.wikipedia.org/wiki/Linear_programming#Integer_unknowns) with [`optlang`](http://optlang.readthedocs.org), made for fun.

## Usage

the `SudokuProblem` class in [`solpoku.py`](/solpoku.py) handles the problem formulation. variables are bounded between 0 and 1, and encoded as `vRCN`, where `R` and `C` represent the number of the row and column (respectively) from 1 to 9, and `N` represents the digit. if a digit `n` is present at row `r`, column `c`, then `vrcn` is set to be maximized. maximizing the sum of variables that refer to posed digits renders a feasible sudoku solution.

the `from_csv` and `from_json` class methods are provided to facilitate handling of input files. `from_array` handles input `numpy` arrays. the `solve` method performs the optimization and builds a 9x9 `numpy` array with the proposed solution.

## Dependencies

a pre-made environment can be set up with:

```shell
mamba env create -p .env -f environment.yaml
```

other versions may work too. however, Python ≥3.10 is required.

## Example

run `solpoku.py` to solve the following sudoku three times:
a) hard-coded in the script, b) read from a [CSV](/test/sudoku.csv) file
(here zeros represent empty tiles)
and c) read from a [JSON](/test/sudoku.json) file:

| | | | | | | | | |
|-|-|-|-|-|-|-|-|-|
|-|-|-|-|6|-|-|-|-|
|-|-|5|2|1|3|8|-|-|
|-|2|-|-|-|-|-|4|-|
|4|-|-|9|-|1|-|-|8|
|-|-|6|4|8|5|3|-|-|
|1|-|-|7|-|6|-|-|4|
|-|6|-|-|-|-|-|2|-|
|-|-|1|3|4|9|7|-|-|
|-|-|-|-|7|-|-|-|-|

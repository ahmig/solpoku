#!/usr/bin/env python

# solpoku: a sudoku solver using LP
# Copyright (C) 2025 ahmig

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import logging
import json
import csv
import itertools as it
from typing import List

import numpy as np
from optlang import Model, Variable, Constraint, Objective


class SudokuProblem:

    @staticmethod
    def _build_constraints() -> List[Constraint]:
        # Init 9x9x9 variables
        variables = {f"v{r}{c}{n}": Variable(f"v{r}{c}{n}", type="integer", lb=0, ub=1) for r, c, n in it.product(range(1, 10), repeat=3)}
        # Declare constraints
        constraints = []
        ## Cells
        for r, c in it.product(range(1, 10), repeat=2):
            logging.debug(f"Cell: sum v{r}{c}* == 1")
            cell_sum = sum(variables[f"v{r}{c}{n}"] for n in range(1, 10))
            constraints.append(
                Constraint(cell_sum, lb=1, ub=1)
            )
        ## Lines (rows and cols)
        for c, n in it.product(range(1, 10), repeat=2):
            logging.debug(f"Cols: sum v*{c}{n} == 1")
            col_sum = sum(variables[f"v{r}{c}{n}"] for r in range(1, 10))
            constraints.append(
                Constraint(col_sum, lb=1, ub=1)
            )
        for r, n in it.product(range(1, 10), repeat=2):
            logging.debug(f"Rows: sum v{r}*{n} == 1")
            row_sum = sum(variables[f"v{r}{c}{n}"] for c in range(1, 10))
            constraints.append(
                Constraint(row_sum, lb=1, ub=1)
            )
        ## Sectors (3x3 squares)
        for sector_r, sector_c in it.product(range(3), repeat=2):
            logging.debug(f"Sector ({sector_r+1}, {sector_c+1})")
            for n in range(1, 10):
                logging.debug(f"Secs: v**{n} == 1")
                sec_sum = sum(variables[f"v{r + sector_r*3}{c + sector_c*3}{n}"] for r, c in it.product(range(1, 4), repeat=2))
                constraints.append(
                    Constraint(sec_sum, lb=1, ub=1)
                )
        return constraints

    def __init__(self, model: Model|None = None):
        if model is None:
            constraints = self._build_constraints()
            self._model = Model("Sudoku problem formulation")
            self._model.add(constraints)
        else:
            self._model = model

    def set_objective(self, varnames: List[str]):
        obj = Objective(
            sum(var for name, var in self._model.variables.iteritems() if name in varnames),
            direction="max"
        )
        self._model.objective = obj

    @classmethod
    def from_json(cls, path: str):
        with open(path) as f:
            model = Model.from_json(json.load(f))
            model.name = "Sudoku problem formulation"
        return cls(model)

    @classmethod
    def from_csv(cls, path: str):
        problem = cls()
        varnames = []
        with open(path) as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                for j in range(len(row)):
                    assert i < 9 and j < 9, "csv is not 9x9"
                    varnames.append(f"v{i+1}{j+1}{row[j]}")
        problem.set_objective(varnames)
        return problem

    def to_json(self, path: str, indent=True):
        with open(path, "w") as fw:
            json.dump(self._model.to_json(), fw, indent=indent)

    def input_sudoku(self, array: np.ndarray):
        assert array.shape == (9, 9), "array is not 9x9"
        self.set_objective(
            [f"v{i+1}{i+2}{array[i, j]}" for i, j in np.ndindex(array.shape) if array[i, j] != 0]
        )

    def _build_sudoku_matrix(self) -> np.ndarray :
        solution = np.zeros((9, 9), dtype=np.uint8)
        for name, var in self._model.variables.iteritems():
            match list(name):
                case ["v", r, c, n]:
                    if var.primal == 1:
                        solution[int(r)-1, int(c)-1] = n
                        continue
                case _:
                    logging.warning(f"Variable '{name}' does not match and is skipped")
        return solution

    def solve(self) -> np.ndarray:
        self._model.optimize()
        return self._build_sudoku_matrix()


if __name__ == "__main__":
    logging.basicConfig(filename="log.txt", filemode="w", level=logging.DEBUG)
    
    sudoku = SudokuProblem()
    sudoku.set_objective(
        [   f"v{str(rcn)}" for rcn in [
                156,  # row = 1, column = 5, value = 6 (etc.)
                235, 242, 251, 263, 278,
                322, 384,
                414, 449, 461, 498,
                536, 544, 558, 565, 573,
                611, 647, 666, 694,
                726, 782,
                831, 843, 854, 869, 877,
                957
            ]
        ]
    )
    solution = sudoku.solve()

    print("solving hard-coded sudoku")
    print("status:", sudoku._model.status)
    print("objective value:", sudoku._model.objective.value)
    print(solution)
    print("--------------------")

    json_sudoku = SudokuProblem.from_json("test/sudoku.json")
    json_solution = json_sudoku.solve()

    print("solving sudoku from JSON")
    print("status:", json_sudoku._model.status)
    print("objective value:", json_sudoku._model.objective.value)
    print(json_solution)
    print("--------------------")

    csv_sudoku = SudokuProblem.from_csv("test/sudoku.csv")
    csv_solution = csv_sudoku.solve()

    print("solving sudoku from CSV")
    print("status:", csv_sudoku._model.status)
    print("objective value:", csv_sudoku._model.objective.value)
    print(csv_solution)
    print("--------------------")

import tkinter as tk
import numpy as np
from solpoku import SudokuProblem


class Application(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.problem = SudokuProblem()
        self.init_number_grid()

    def solve(self):
        # Solve problem from array
        array = np.zeros((9, 9), dtype=np.uint8)
        for (i, j), value in self.grid_values.items():
            array[i, j] = value.get()
            print(f"grid ({i+1},{j+1}) = {value.get()}")
        self.problem.set_objective_from_array(array)
        solution = self.problem.solve()
        # Fill grid
        for (i, j), value in self.grid_values.items():
            value.set(solution[i, j])
        # Update status
        self.status_label.config(text=self.problem._model.status)

    def _update_value_callback(self, row, col):
        def wrapped():
            value = self.grid_values[(row, col)]
            if value.get() == 9:
                value.set(0)
            else:
                value.set(value.get() + 1)
            self.status_label.config(text="unsolved")
        return wrapped

    def init_number_grid(self):
        # Number grid
        self.grid_values = {}
        for i in range(9):
            for j in range(9):
                button_value = tk.IntVar()
                button_value.set(0)
                button = tk.Button(
                    self,
                    name=f"v{i+1}{j+1}",
                    textvariable=button_value
                )
                button.config(command=self._update_value_callback(i, j))
                button.grid(row=i, column=j)
                self.grid_values[(i, j)] = button_value
        # Solve button
        self.solve_button = tk.Button(
            self,
            text="Solve",
            command=self.solve
        )
        self.solve_button.grid(row=9, column=0, columnspan=5)
        # Status label
        self.status_label = tk.Label(
            self,
            text="unsolved"
        )
        self.status_label.grid(row=9, column=4, columnspan=4)


if __name__ == "__main__":
    app = Application()
    app.master.title("solpoku GUI")
    app.mainloop()

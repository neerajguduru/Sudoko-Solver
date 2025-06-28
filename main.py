import tkinter as tk
from tkinter import messagebox
import random
import time
import threading

class SudokuGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku Solver")
        self.master.configure(bg="#f0f0f0")

        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.board = [[0]*9 for _ in range(9)]
        self.stop_flag = False
        self.solving_thread = None

        self.build_grid()
        self.add_buttons()

    def build_grid(self):
        frame = tk.Frame(self.master, bg="#f0f0f0")
        frame.grid(row=0, column=0, columnspan=9, pady=10)
        for i in range(9):
            for j in range(9):
                e = tk.Entry(frame, width=3, font=('Arial', 18), justify='center', relief='ridge', bd=2)
                e.grid(row=i, column=j, padx=(1 if j % 3 else 3), pady=(1 if i % 3 else 3))
                e.configure(bg="white", disabledbackground="#e0e0e0", disabledforeground="black")
                self.cells[i][j] = e

    def add_buttons(self):
        self.solve_btn = tk.Button(self.master, text="Solve", command=self.start_solving,
                                   bg="#4caf50", fg="white", font=("Arial", 12), width=8)
        self.solve_btn.grid(row=10, column=0, columnspan=2, pady=10)

        self.skip_btn = tk.Button(self.master, text="Skip", command=self.solve_instant,
                                  bg="#2196f3", fg="white", font=("Arial", 12), width=8)
        self.skip_btn.grid(row=10, column=2, columnspan=2)

        self.stop_btn = tk.Button(self.master, text="Stop", command=self.stop_solving,
                                  bg="#f44336", fg="white", font=("Arial", 12), width=8)
        self.stop_btn.grid(row=10, column=4, columnspan=2)

        self.random_btn = tk.Button(self.master, text="Random", command=self.load_random,
                                    bg="#9c27b0", fg="white", font=("Arial", 12), width=8)
        self.random_btn.grid(row=10, column=6, columnspan=1)

        self.clear_btn = tk.Button(self.master, text="Clear", command=self.clear_grid,
                                   bg="#607d8b", fg="white", font=("Arial", 12), width=8)
        self.clear_btn.grid(row=10, column=7, columnspan=2)

    def clear_grid(self):
        self.stop_flag = True
        for i in range(9):
            for j in range(9):
                cell = self.cells[i][j]
                cell.config(state='normal')
                cell.delete(0, tk.END)
                cell.config(bg="white")

    def load_random(self):
        self.clear_grid()
        puzzle = random.choice(self.get_puzzles())
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] != 0:
                    self.cells[i][j].insert(0, puzzle[i][j])
                    self.cells[i][j].config(disabledforeground="black", state="disabled")

    def get_board(self):
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.cells[i][j].get()
                if val == "":
                    row.append(0)
                elif val.isdigit() and 1 <= int(val) <= 9:
                    row.append(int(val))
                else:
                    messagebox.showerror("Invalid Input", f"Cell ({i+1},{j+1}) must be 1–9 or empty.")
                    return None
            board.append(row)
        return board

    def start_solving(self):
        board = self.get_board()
        if board is None:
            return
        if not self.is_valid_board(board):
            messagebox.showerror("Invalid Board", "Initial board violates Sudoku rules.")
            return

        self.stop_flag = False
        self.set_buttons_state("disabled")

        self.solving_thread = threading.Thread(target=self.solve_stepwise, args=(board,))
        self.solving_thread.daemon = True
        self.solving_thread.start()

    def stop_solving(self):
        self.stop_flag = True
        self.set_buttons_state("normal")

    def solve_instant(self):
        self.stop_flag = True
        board = self.get_board()
        if board is None:
            return
        if not self.is_valid_board(board):
            messagebox.showerror("Invalid Board", "Initial board violates Sudoku rules.")
            return

        if self.solve_backtrack(board):
            for i in range(9):
                for j in range(9):
                    self.cells[i][j].config(state="normal")
                    self.cells[i][j].delete(0, tk.END)
                    self.cells[i][j].insert(0, board[i][j])
                    self.cells[i][j].config(bg="white")
        else:
            messagebox.showinfo("Result", "No solution found.")
        self.set_buttons_state("normal")

    def set_buttons_state(self, state):
        if state == "disabled":
            self.solve_btn.config(state="disabled")
            self.clear_btn.config(state="disabled")
            self.random_btn.config(state="disabled")
        else:
            self.solve_btn.config(state="normal")
            self.clear_btn.config(state="normal")
            self.random_btn.config(state="normal")

    def update_cell(self, i, j, value, color):
        cell = self.cells[i][j]
        cell.config(state="normal")
        cell.delete(0, tk.END)
        if value != 0:
            cell.insert(0, value)
        cell.config(bg=color)
        self.master.update()
        time.sleep(0.03)

    def solve_stepwise(self, board):
        def backtrack():
            for i in range(9):
                for j in range(9):
                    if self.stop_flag:
                        return False
                    if board[i][j] == 0:
                        for num in range(1, 10):
                            if self.is_valid(board, i, j, num):
                                board[i][j] = num
                                self.update_cell(i, j, num, "lightgreen")
                                if backtrack():
                                    return True
                                board[i][j] = 0
                                self.update_cell(i, j, 0, "lightcoral")
                        return False
            return True

        backtrack()
        self.set_buttons_state("normal")

    def solve_backtrack(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid(board, i, j, num):
                            board[i][j] = num
                            if self.solve_backtrack(board):
                                return True
                            board[i][j] = 0
                    return False
        return True

    def is_valid(self, board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        start_r, start_c = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_r + i][start_c + j] == num:
                    return False
        return True

    def is_valid_board(self, board):
        for i in range(9):
            for j in range(9):
                num = board[i][j]
                if num != 0:
                    board[i][j] = 0
                    if not self.is_valid(board, i, j, num):
                        return False
                    board[i][j] = num
        return True

    def get_puzzles(self):
        return [
            [
                [5, 3, 0, 0, 7, 0, 0, 0, 0],
                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                [0, 9, 8, 0, 0, 0, 0, 6, 0],
                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                [0, 0, 0, 0, 8, 0, 0, 7, 9]
            ],

            # Puzzle 2
            [
                [0, 2, 0, 6, 0, 8, 0, 0, 0],
                [5, 8, 0, 0, 0, 9, 7, 0, 0],
                [0, 0, 0, 0, 4, 0, 0, 0, 0],
                [3, 7, 0, 0, 0, 0, 5, 0, 0],
                [6, 0, 0, 0, 0, 0, 0, 0, 4],
                [0, 0, 8, 0, 0, 0, 0, 1, 3],
                [0, 0, 0, 0, 2, 0, 0, 0, 0],
                [0, 0, 9, 8, 0, 0, 0, 3, 6],
                [0, 0, 0, 3, 0, 6, 0, 9, 0]
            ],

            # Puzzle 3
            [
                [1, 0, 0, 4, 8, 9, 0, 0, 6],
                [7, 3, 0, 0, 0, 0, 0, 4, 0],
                [0, 0, 0, 0, 0, 1, 2, 9, 5],
                [0, 9, 0, 0, 0, 6, 0, 0, 0],
                [5, 0, 0, 1, 0, 2, 0, 0, 8],
                [0, 0, 0, 9, 0, 0, 0, 3, 0],
                [9, 6, 1, 5, 0, 0, 0, 0, 0],
                [0, 2, 0, 0, 0, 0, 0, 1, 9],
                [8, 0, 0, 3, 6, 4, 0, 0, 2]
            ],

            # Puzzle 4
            [
                [0, 0, 5, 3, 0, 0, 0, 0, 0],
                [8, 0, 0, 0, 0, 0, 0, 2, 0],
                [0, 7, 0, 0, 1, 0, 5, 0, 0],
                [4, 0, 0, 0, 0, 5, 3, 0, 0],
                [0, 1, 0, 0, 7, 0, 0, 0, 6],
                [0, 0, 3, 2, 0, 0, 0, 8, 0],
                [0, 6, 0, 5, 0, 0, 0, 0, 9],
                [0, 0, 4, 0, 0, 0, 0, 3, 0],
                [0, 0, 0, 0, 0, 9, 7, 0, 0]
            ]
        ]

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()

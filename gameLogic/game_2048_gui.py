import tkinter as tk
import tkinter.messagebox
from game_2048 import Game2048
from expectimax_agent import get_best_move

class Game2048GUI:
    COLORS = {
        0: "#c7d8ff",       # stronger pastel blue for empty tile
        2: "#ffb6c1",       # light pink
        4: "#99ccff",       # pastel blue
        8: "#ffd8b1",       # pastel peach
        16: "#a0e6a0",      # pastel green
        32: "#ff9fb1",      # soft coral pink
        64: "#8fd3bf",      # soft teal
        128: "#ff8fa3",     # medium pink
        256: "#9fcfff",     # medium blue
        512: "#ffcccb",     # very light pink
        1024: "#8fe0d0",    # pale aqua
        2048: "#d6d8ff",    # pastel lavender
    }

    FONT = ("Verdana", 24, "bold")
    TILE_SIZE = 100
    TILE_PADDING = 10
    CORNER_RADIUS = 20

    def __init__(self, master):
        self.master = master
        self.master.title("2048 Game - Rounded Tiles with AutoPlay")
        self.game = Game2048()
        self.grid_cells = []
        self.init_gui()
        self.update_gui()
        self.master.bind("<Key>", self.key_handler)

    def init_gui(self):
        background_color = "#a8c0ff"  # soft baby blue stronger background
        self.master.configure(bg=background_color)

        background = tk.Frame(self.master, bg=background_color, width=520, height=520)
        background.grid(padx=10, pady=10)
        for i in range(self.game.size):
            row = []
            for j in range(self.game.size):
                canvas = tk.Canvas(
                    background,
                    width=self.TILE_SIZE,
                    height=self.TILE_SIZE,
                    bg=background_color,
                    highlightthickness=0
                )
                canvas.grid(row=i, column=j, padx=self.TILE_PADDING // 2, pady=self.TILE_PADDING // 2)
                row.append(canvas)
            self.grid_cells.append(row)

        self.score_label = tk.Label(self.master, text="Score: 0", font=("Verdana", 16), fg="#333366", bg=background_color)
        self.score_label.grid()

        # Reset button - pretty pastel pink
        self.reset_button = tk.Button(
            self.master,
            text="Reset",
            font=("Verdana", 14, "bold"),
            bg="#ff7f9f",
            fg="#fff",
            activebackground="#ff95ab",
            activeforeground="#fff",
            bd=0,
            relief="flat",
            padx=15,
            pady=8,
            command=self.reset_game
        )
        self.reset_button.grid(pady=10)
        self.reset_button.bind("<Enter>", lambda e: e.widget.config(bg="#ff95ab"))
        self.reset_button.bind("<Leave>", lambda e: e.widget.config(bg="#ff7f9f"))

        # Auto Play button - pastel baby blue
        self.auto_button = tk.Button(
            self.master,
            text="Auto Play",
            font=("Verdana", 14, "bold"),
            bg="#7fcaff",
            fg="#fff",
            activebackground="#a1d2ff",
            activeforeground="#fff",
            bd=0,
            relief="flat",
            padx=15,
            pady=8,
            command=self.start_autoplay
        )
        self.auto_button.grid(pady=10)
        self.auto_button.bind("<Enter>", lambda e: e.widget.config(bg="#a1d2ff"))
        self.auto_button.bind("<Leave>", lambda e: e.widget.config(bg="#7fcaff"))

    def draw_rounded_rect(self, canvas, x1, y1, x2, y2, radius, fill):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1,
        ]
        return canvas.create_polygon(points, fill=fill, smooth=True)

    def update_gui(self):
        board = self.game.get_board()
        for i in range(self.game.size):
            for j in range(self.game.size):
                canvas = self.grid_cells[i][j]
                canvas.delete("all")

                value = board[i, j]
                bg_color = self.COLORS.get(value, "#e0e0e0")
                fg_color = "#333333" if value <= 16 else "#111111"

                self.draw_rounded_rect(
                    canvas,
                    5, 5,
                    self.TILE_SIZE - 5,
                    self.TILE_SIZE - 5,
                    self.CORNER_RADIUS,
                    fill=bg_color
                )

                if value != 0:
                    canvas.create_text(
                        self.TILE_SIZE // 2,
                        self.TILE_SIZE // 2,
                        text=str(value),
                        font=self.FONT,
                        fill=fg_color
                    )
        self.score_label.configure(text=f"Score: {self.game.get_score()}")
        self.master.update_idletasks()

    def key_handler(self, event):
        key = event.keysym
        if key in ['Up', 'Down', 'Left', 'Right']:
            moved = self.game.move(key)
            if moved:
                self.update_gui()
                if self.game.is_game_over():
                    self.game_over()

    def reset_game(self):
        self.game.reset()
        self.update_gui()
        self.master.bind("<Key>", self.key_handler)
        # Remove any 'Game Over' label
        for widget in self.master.grid_slaves():
            if isinstance(widget, tk.Label) and widget.cget("text") == "Game Over!":
                widget.destroy()
        self.reset_button.config(state="normal")
        self.auto_button.config(state="normal")

    def game_over(self):
        over_label = tk.Label(self.master, text="Game Over!", font=("Verdana", 48), fg="#cc3366", bg="#a8c0ff")
        over_label.grid(row=0, column=0, columnspan=self.game.size, pady=10)
        self.master.unbind("<Key>")
        self.reset_button.config(state="normal")
        self.auto_button.config(state="normal")

    def start_autoplay(self):
        self.auto_button.config(state="disabled")
        self.reset_button.config(state="disabled")
        self.master.unbind("<Key>")
        self.autoplay_step()

    def autoplay_step(self):
        if self.game.is_game_over():
            tk.messagebox.showinfo("Auto Play", "Game Over!")
            self.reset_button.config(state="normal")
            self.auto_button.config(state="normal")
            self.master.bind("<Key>", self.key_handler)
            return

        board = self.game.get_board()
        best_move = get_best_move(board, self.game, max_depth=3)

        if best_move is None:
            tk.messagebox.showinfo("Auto Play", "No moves available. Game Over!")
            self.reset_button.config(state="normal")
            self.auto_button.config(state="normal")
            self.master.bind("<Key>", self.key_handler)
            return

        self.game.move(best_move)
        self.update_gui()
        self.master.after(300, self.autoplay_step)


if __name__ == "__main__":
    root = tk.Tk()
    game_gui = Game2048GUI(root)
    root.mainloop()
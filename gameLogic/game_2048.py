import tkinter as tk
import random
import pickle
from collections import Counter
from utilities import GRID_SIZE, BACKGROUND_COLOR, CELL_SIZE, TILE_COLORS, PADDING, FONT
from ai_simulation import Game2048AI
from q_trainer_2048 import QTrainer
from mainGameLogic import GameLogic

class Game2048(GameLogic):
    def __init__(self, root):
        self.root = root
        self.root.title("2048 Game")
        self.root.geometry(f"{GRID_SIZE * CELL_SIZE + 100}x{GRID_SIZE * CELL_SIZE + 100}")

        frame = tk.Frame(self.root)
        frame.pack()

        self.canvas = tk.Canvas(frame, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE, bg=BACKGROUND_COLOR)
        self.canvas.pack()

        tk.Button(self.root, text="AI Move", command=self.auto_play).pack(pady=10)
        tk.Button(self.root, text="Run 50 AI Games", command=self.start_auto_evaluate).pack(pady=10)
        tk.Button(self.root, text="Train AI Model", command=self.train_model).pack(pady=10)

        self.board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.add_random_tile()
        self.add_random_tile()
        self.draw_board()

        self.root.bind("<Key>", self.key_handler)

        self.auto_runs = 0
        self.max_auto_runs = 50
        self.auto_scores = []
        self.auto_max_tiles = []

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = self.board[i][j]
                color = TILE_COLORS.get(value, "#3c3a32")
                x0 = j * CELL_SIZE + PADDING
                y0 = i * CELL_SIZE + PADDING
                x1 = x0 + CELL_SIZE - 2 * PADDING
                y1 = y0 + CELL_SIZE - 2 * PADDING
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
                if value != 0:
                    self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2,
                                            text=str(value), font=FONT, fill="#776e65")

    def add_random_tile(self):
        empty = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.board[i][j] == 0]
        if empty:
            i, j = random.choice(empty)
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def key_handler(self, event):
        key = event.keysym
        moved = False

        if key == "Up":
            moved = self.move_vertical(self.board, up=True)
        elif key == "Down":
            moved = self.move_vertical(self.board, up=False)
        elif key == "Left":
            moved = self.move_horizontal(self.board, left=True)
        elif key == "Right":
            moved = self.move_horizontal(self.board, left=False)

        if moved:
            self.add_random_tile()
            self.draw_board()
            if not self.can_move():
                self.show_game_over()

    def can_move(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.board[i][j] == 0:
                    return True
                if j < GRID_SIZE - 1 and self.board[i][j] == self.board[i][j + 1]:
                    return True
                if i < GRID_SIZE - 1 and self.board[i][j] == self.board[i + 1][j]:
                    return True
        return False

    def get_best_move(self):
        directions = ['Up', 'Down', 'Left', 'Right']
        best_score = -float('inf')
        best_direction = None
        for direction in directions:
            temp_game = Game2048AI(self.board)
            moved = temp_game.move(direction)
            if moved:
                score = temp_game.heuristic()
                if score > best_score:
                    best_score = score
                    best_direction = direction
        return best_direction

    def auto_play(self):
        direction = self.get_best_move()
        if direction:
            if direction == "Up":
                self.move_vertical(self.board, up=True)
            elif direction == "Down":
                self.move_vertical(self.board, up=False)
            elif direction == "Left":
                self.move_horizontal(self.board, left=True)
            elif direction == "Right":
                self.move_horizontal(self.board, left=False)
            self.add_random_tile()
            self.draw_board()
            if self.can_move():
                self.root.after(300, self.auto_play)
            else:
                self.show_game_over()

    def show_game_over(self):
        self.canvas.create_text(GRID_SIZE * CELL_SIZE / 2, GRID_SIZE * CELL_SIZE / 2,
                                text="Game Over!", font=("Verdana", 32, "bold"), fill="red")

    def reset_game(self):
        self.board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.add_random_tile()
        self.add_random_tile()
        self.draw_board()

    def start_auto_evaluate(self):
        self.auto_runs = 0
        self.auto_scores = []
        self.auto_max_tiles = []
        self.log_eval_file = open("evaluation_results_log.txt", "w")
        self.run_single_game()

    def run_single_game(self):
        if self.auto_runs >= self.max_auto_runs:
            self.show_auto_results()
            return
        self.reset_game()
        self.root.after(500, self.auto_play_once)

    def auto_play_once(self):
        if not self.can_move():
            final_score = sum(map(sum, self.board))
            max_tile = max(map(max, self.board))
            self.auto_scores.append(final_score)
            self.auto_max_tiles.append(max_tile)
            self.log_eval_file.write(f"Game {self.auto_runs + 1} - Final Score: {final_score}, Max Tile: {max_tile}\n")
            self.auto_runs += 1
            self.root.after(300, self.run_single_game)
            return
        self.auto_play()

    def show_auto_results(self):
        avg_score = sum(self.auto_scores) / len(self.auto_scores)
        max_tile_counts = Counter(self.auto_max_tiles)
        result_text = f"Average Score: {avg_score:.2f}\n"
        for tile in sorted(max_tile_counts):
            percent = 100 * max_tile_counts[tile] / self.max_auto_runs
            result_text += f"Reached {tile}: {percent:.2f}% of the time\n"
        tk.Label(tk.Toplevel(self.root), text=result_text, font=("Verdana", 14), justify="left").pack(padx=20, pady=20)
        self.log_eval_file.write("\nSummary:\n" + result_text)
        self.log_eval_file.close()

    def train_model(self):
        trainer = QTrainer()
        for ep in range(1000):
            self.reset_game()
            state = trainer.get_state_key(self.board)
            total_reward = 0

            while self.can_move():
                action = trainer.choose_action(state)
                moved = self.move_action(action)
                reward = self.get_reward(moved)
                next_state = trainer.get_state_key(self.board)
                done = not self.can_move()

                trainer.update_q(state, action, reward, next_state, done)
                state = next_state
                total_reward += reward

                if done:
                    break

            trainer.decay_epsilon()
            print(f"Episode {ep + 1}, Score: {total_reward}")

        with open("q_model.pkl", "wb") as f:
            pickle.dump(trainer.q_table, f)

    def move_action(self, action):
        if action == "Up":
            return self.move_vertical(self.board, up=True)
        elif action == "Down":
            return self.move_vertical(self.board, up=False)
        elif action == "Left":
            return self.move_horizontal(self.board, left=True)
        elif action == "Right":
            return self.move_horizontal(self.board, left=False)
        return False

    def get_reward(self, moved):
        if not moved:
            return -1
        return sum(map(sum, self.board))


if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()

"""Simple cross-platform Snake game using Tkinter."""

import random
import tkinter as tk

# Size of each grid cell and number of cells
CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 20
DELAY_MS = 100


class SnakeGame(tk.Frame):
    """Tkinter-based Snake game."""

    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master)
        self.master = master
        self.canvas = tk.Canvas(self,
                                width=CELL_SIZE * GRID_WIDTH,
                                height=CELL_SIZE * GRID_HEIGHT,
                                bg="black")
        self.canvas.pack()
        self.pack()

        self.master.bind("<Key>", self.on_key)
        self.reset()
        self.after_id = None
        self.running = True
        self.step()

    def reset(self) -> None:
        """Reset the game state."""
        self.direction = "Right"
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.food = self._random_food()
        self.draw()

    def _random_food(self) -> tuple[int, int]:
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1),
                   random.randint(0, GRID_HEIGHT - 1))
            if pos not in self.snake:
                return pos

    def draw(self) -> None:
        self.canvas.delete("all")
        for x, y in self.snake:
            self.canvas.create_rectangle(x * CELL_SIZE,
                                         y * CELL_SIZE,
                                         (x + 1) * CELL_SIZE,
                                         (y + 1) * CELL_SIZE,
                                         fill="green",
                                         outline="")
        fx, fy = self.food
        self.canvas.create_rectangle(fx * CELL_SIZE,
                                     fy * CELL_SIZE,
                                     (fx + 1) * CELL_SIZE,
                                     (fy + 1) * CELL_SIZE,
                                     fill="red",
                                     outline="")

    def on_key(self, event: tk.Event) -> None:
        if event.keysym in {"Up", "Down", "Left", "Right"}:
            self.direction = event.keysym

    def step(self) -> None:
        if not self.running:
            return
        head_x, head_y = self.snake[0]
        if self.direction == "Up":
            head_y -= 1
        elif self.direction == "Down":
            head_y += 1
        elif self.direction == "Left":
            head_x -= 1
        elif self.direction == "Right":
            head_x += 1

        new_head = (head_x, head_y)
        if (
            head_x < 0 or head_x >= GRID_WIDTH or
            head_y < 0 or head_y >= GRID_HEIGHT or
            new_head in self.snake
        ):
            self.running = False
            self.canvas.create_text(GRID_WIDTH * CELL_SIZE // 2,
                                    GRID_HEIGHT * CELL_SIZE // 2,
                                    text="Game Over",
                                    fill="white",
                                    font=("Arial", 16))
            return

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.food = self._random_food()
        else:
            self.snake.pop()
        self.draw()
        self.after_id = self.after(DELAY_MS, self.step)


def main() -> None:
    root = tk.Tk()
    root.title("Snake")
    SnakeGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()

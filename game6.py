import tkinter as tk
import random

# Constants
GRID_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 15
SNAKE_SPEED = 100

# Colors
HEAD_COLOR = "blue"
BODY_COLOR = "green"
FOOD_COLOR = "red"
BG_COLOR = "black"

# Direction constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")

        self.canvas = tk.Canvas(master, width=GRID_WIDTH*GRID_SIZE, height=GRID_HEIGHT*GRID_SIZE, bg=BG_COLOR)
        self.canvas.pack()

        self.snake = [(4, 4)]
        self.food = self.generate_food()
        self.direction = RIGHT
        self.score = 0

        self.master.bind("<Key>", self.change_direction)
        self.update()

        self.restart_button = tk.Button(master, text="Restart", command=self.restart)
        self.restart_button.pack()

    def generate_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
            if food not in self.snake:
                return food

    def change_direction(self, event):
        if event.keysym == "Up" and self.direction != DOWN:
            self.direction = UP
        elif event.keysym == "Down" and self.direction != UP:
            self.direction = DOWN
        elif event.keysym == "Left" and self.direction != RIGHT:
            self.direction = LEFT
        elif event.keysym == "Right" and self.direction != LEFT:
            self.direction = RIGHT

    def update(self):
        new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])

        if (
            new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
            new_head in self.snake[1:]
        ):
            self.game_over()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            self.snake.pop()

        self.canvas.delete("all")

        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(
                x * GRID_SIZE, y * GRID_SIZE,
                (x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE,
                fill=BODY_COLOR, outline="white"
            )

        x, y = self.food
        self.canvas.create_rectangle(
            x * GRID_SIZE, y * GRID_SIZE,
            (x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE,
            fill=FOOD_COLOR, outline="white"
        )

        self.master.title(f"Snake Game - Score: {self.score}")
        self.master.after(SNAKE_SPEED, self.update)

    def game_over(self):
        self.canvas.delete("all")
        self.canvas.create_text(
            GRID_WIDTH * GRID_SIZE / 2,
            GRID_HEIGHT * GRID_SIZE / 2,
            text=f"Game Over! Your Score: {self.score}",
            fill="white",
            font=("Helvetica", 20)
        )
        self.restart_button.pack()

    def restart(self):
        self.snake = [(4, 4)]
        self.food = self.generate_food()
        self.direction = RIGHT
        self.score = 0
        self.restart_button.pack_forget()  # Hide the restart button
        self.update()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()

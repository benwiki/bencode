import tkinter as tk
from datetime import datetime
from random import choice, randint
from time import time
from rubik_solver import utils
from pprint import pprint


def main():
    RubikVisual()


class RubiksCube:
    def __init__(self):
        self.faces = {
            "U": [["Y" for j in range(3)] for i in range(3)],
            "L": [["B" for j in range(3)] for i in range(3)],
            "F": [["R" for j in range(3)] for i in range(3)],
            "R": [["G" for j in range(3)] for i in range(3)],
            "B": [["O" for j in range(3)] for i in range(3)],
            "D": [["W" for j in range(3)] for i in range(3)],
        }
        self.randomized = False
        
    def export(self):
        return "".join(C[0] for face in self.faces.values() for line in face for C in line).lower()
        
    def is_solved(self):
        return all(
            all(
                all(val == face[0][0] for val in row)
                for row in face
            )
            for face in self.faces.values()
        )
        
    def reset(self):
        self.faces = {
            "U": [["Y" for j in range(3)] for i in range(3)],
            "L": [["B" for j in range(3)] for i in range(3)],
            "F": [["R" for j in range(3)] for i in range(3)],
            "R": [["G" for j in range(3)] for i in range(3)],
            "B": [["O" for j in range(3)] for i in range(3)],
            "D": [["W" for j in range(3)] for i in range(3)],
        }
        
    def randomize(self):
        import sys
        import os
        steps = int(sys.argv[1]) if os.getcwd() == r"C:\Users\Admin" else randint(100, 150)
        for _ in range(steps):
            self.rotate(choice("udfblrUDFBLR"))
        self.randomized = True

    def rotate(self, face: str):
        if face.isupper():
            face = face.lower()
            self.rotate(face)
            self.rotate(face)
            self.rotate(face)
            return
        face = face.upper()
        match face:
            case "U":
                self.faces["U"] = [
                    [self.faces["U"][j][2 - i] for j in range(3)] for i in range(3)
                ]
                F = self.faces["F"][0].copy()
                self.faces["F"][0] = self.faces["L"][0].copy()
                self.faces["L"][0] = self.faces["B"][0].copy()
                self.faces["B"][0] = self.faces["R"][0].copy()
                self.faces["R"][0] = F
            case "F":
                self.faces["F"] = [
                    [self.faces["F"][j][2 - i] for j in range(3)] for i in range(3)
                ]
                D = self.faces["D"].copy()
                self.faces["D"][0] = [row[2] for row in self.faces["L"]]
                self.faces["L"][0][2] = self.faces["U"][2][2]
                self.faces["L"][1][2] = self.faces["U"][2][1]
                self.faces["L"][2][2] = self.faces["U"][2][0]
                self.faces["U"][2] = [row[0] for row in self.faces["R"]]
                self.faces["R"][0][0] = D[0][2]
                self.faces["R"][1][0] = D[0][1]
                self.faces["R"][2][0] = D[0][0]
            case "L":
                self.switch("U")
                self.rotate("F")
                self.switch("U")
                self.switch("U")
                self.switch("U")
            case "B":
                self.switch("U")
                self.switch("U")
                self.rotate("F")
                self.switch("U")
                self.switch("U")
            case "R":
                self.switch("U")
                self.switch("U")
                self.switch("U")
                self.rotate("F")
                self.rotate("F")
                self.rotate("F")
                self.switch("U")
            case "D":
                self.faces["D"] = [
                    [self.faces["D"][j][2 - i] for j in range(3)] for i in range(3)
                ]
                self.faces["D"] = [
                    [self.faces["D"][j][2 - i] for j in range(3)] for i in range(3)
                ]
                self.faces["D"] = [
                    [self.faces["D"][j][2 - i] for j in range(3)] for i in range(3)
                ]
                F = self.faces["F"][2].copy()
                self.faces["F"][2] = self.faces["L"][2].copy()
                self.faces["L"][2] = self.faces["B"][2].copy()
                self.faces["B"][2] = self.faces["R"][2].copy()
                self.faces["R"][2] = F

    def switch(self, face: str):
        match face:
            case "U":
                self.faces["U"] = [
                    [self.faces["U"][j][2 - i] for j in range(3)] for i in range(3)
                ]
                self.faces["D"] = [
                    [self.faces["D"][j][2 - i] for j in range(3)] for i in range(3)
                ]
                self.faces["D"] = [
                    [self.faces["D"][j][2 - i] for j in range(3)] for i in range(3)
                ]
                self.faces["D"] = [
                    [self.faces["D"][j][2 - i] for j in range(3)] for i in range(3)
                ]
                F = self.faces["F"].copy()
                self.faces["F"] = self.faces["L"].copy()
                self.faces["L"] = self.faces["B"].copy()
                self.faces["B"] = self.faces["R"].copy()
                self.faces["R"] = F


class RubikVisual(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.cube = RubiksCube()
        self.time = 0
        self.time_saved = False
        self.rects: list[int] = []
        
        self.w, self.h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.draw = tk.Canvas(width=self.w, height=self.h)
        self.draw.pack()
        self.timelabel = self.draw.create_text(self.w//2, 50, text="Press ENTER to randomize")
        self.bind("<Key>", self.key)
        
        self.after(1, self.update_time)
        self.update_cube()
        self.mainloop()

    def key(self, event):
        key: str = event.char
        key = {
            "f": "l",
            "r": "L",
            
            "j": "r",
            "u": "R",
            
            "e": "b",
            "i": "B",
            
            "l": "d",
            "s": "D",
            
            "o": "u",
            "w": "U",
            
            "d": "f",
            "k": "F",
            
            "a": "LEFT",
            "é": "RIGHT",
            
            "1": "SOLVE",
            "2": "SHOW",
        }.get(key, "")
        
        if event.keysym == "Return":
            self.cube.reset()
            self.cube.randomize()
            self.time = 0
            self.time_saved = False
        else:
            if self.cube.randomized:
                self.time = time()
                self.cube.randomized = False
            if key == "SOLVE":
                print(utils.solve(self.cube.export(), "Kociemba"))
            if key == "SHOW":
                
                pprint(self.cube.faces)
            elif key == "LEFT":
                self.cube.switch("U")
                self.cube.switch("U")
                self.cube.switch("U")
            elif key == "RIGHT":
                self.cube.switch("U")
            else:
                self.cube.rotate(key)
        self.update_cube()
        
        if self.cube.is_solved() and not self.time_saved:
            with open("rubiktimes.txt", "a", encoding="utf-8") as f:
                f.write(datetime.now().strftime(f"%Y.%m.%d. %H:%M:%S - {time()-self.time}\n"))
            self.time_saved = True
        
    def update_time(self):
        if self.time > 0 and not self.time_saved:
            self.draw.itemconfig(self.timelabel, text=str(time()-self.time))
            
        self.after(1, self.update_time)

    def update_cube(self):
        if self.rects:
            self.draw.delete(*self.rects)
        self.rects.clear()
        self.draw_side(self.w // 5, self.h // 2, "L")
        self.draw_side(self.w // 5 * 2, self.h // 2, "F")
        self.draw_side(self.w // 5 * 3, self.h // 2, "R")
        self.draw_side(self.w // 5 * 4, self.h // 2, "B")
        self.draw_side(self.w // 5 * 2, self.h // 4, "U")
        self.draw_side(self.w // 5 * 2, self.h // 4 * 3, "D")

    def draw_side(self, x, y, side: str, w=50, padding=10):
        for i in range(3):
            for j in range(3):
                self.rects.append(self.draw.create_rectangle(
                    self.sq_coords(
                        x + (j - 1) * (w + padding), y + (i - 1) * (w + padding), w
                    ),
                    fill=self.to_color(self.cube.faces[side][i][j][0]),
                ))

    def sq_coords(self, x, y, w):
        return [x - w // 2, y - w // 2, x + w // 2, y + w // 2]

    def to_color(self, col):
        return {
            "W": "white",
            "Y": "yellow",
            "G": "green",
            "B": "blue",
            "O": "orange",
            "R": "red",
        }.get(col, "black")


if __name__ == "__main__":
    main()

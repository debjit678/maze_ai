import tkinter as tk
from tkinter import messagebox, ttk
import random
import heapq
import time
from collections import deque

# --- NEURAL-VIZ THEME ---
COLOR_BG = "#020617"       
COLOR_SIDEBAR = "#0F172A"  
COLOR_WALL = "#1E293B"     
COLOR_PATH = "#020617"     
COLOR_PLAYER = "#38BDF8"   
COLOR_AI = "#F43F5E"       
COLOR_GOAL = "#10B981"     
COLOR_TRAIL = "#1E3A8A"    

GRID_SIZE = 15
CELL_SIZE = 42

MAZE = [
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0],
    [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
]

def solve_maze(algo, maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    visited = set()
    if algo == "BFS": container = deque([(start, [])])
    elif algo == "DFS": container = [(start, [])]
    else: 
        container = [(0, start, [])]
        g_score = {tuple(start): 0}
    while container:
        if algo == "BFS": (curr, path) = container.popleft()
        elif algo == "DFS": (curr, path) = container.pop()
        else: _, curr, path = heapq.heappop(container)
        if tuple(curr) in visited: continue
        visited.add(tuple(curr))
        if curr == goal: return path
        for dr, dc, move in [(-1,0,'Up'), (1,0,'Down'), (0,-1,'Left'), (0,1,'Right')]:
            r, c = curr[0] + dr, curr[1] + dc
            if 0 <= r < rows and 0 <= c < cols and maze[r][c] == 0:
                if algo == "A*":
                    new_g = len(path) + 1
                    if tuple([r,c]) not in g_score or new_g < g_score[tuple([r,c])]:
                        g_score[tuple([r,c])] = new_g
                        f = new_g + abs(r-goal[0]) + abs(c-goal[1])
                        heapq.heappush(container, (f, [r,c], path + [move]))
                elif tuple([r,c]) not in visited:
                    container.append(([r,c], path + [move]))
    return []

class NeuralVizFinal:
    def __init__(self, root):
        self.root = root
        self.root.title("Neural-Viz AI Competition v4.0")
        self.root.geometry("1100x850")
        self.root.configure(bg=COLOR_BG)

        self.player_pos = [0, 0]
        self.ai_pos = [0, 0]
        self.ai_trail = set()
        self.is_running = False
        self.start_time = 0
        self.player_time = None
        self.ai_time = None
        self.race_id = 0

        self.setup_ui()
        self.draw_grid()
        self.root.bind("<KeyPress>", self.move_player)
        # Ensure initial focus is on the root window
        self.root.focus_set()

    def setup_ui(self):
        self.side = tk.Frame(self.root, width=300, bg=COLOR_SIDEBAR, padx=20, pady=30)
        self.side.pack(side="right", fill="y")

        tk.Label(self.side, text="RACE COMMAND", fg=COLOR_PLAYER, bg=COLOR_SIDEBAR, font=("Arial", 18, "bold")).pack(pady=10)
        
        tk.Label(self.side, text="AI ALGORITHM", fg="#64748B", bg=COLOR_SIDEBAR).pack(anchor="w")
        self.algo_box = ttk.Combobox(self.side, values=["BFS", "DFS", "A*"], state="readonly")
        self.algo_box.set("A*")
        self.algo_box.pack(pady=5, fill="x")
        # BUG FIX: Reset focus after selection
        self.algo_box.bind("<<ComboboxSelected>>", lambda e: self.root.focus())

        tk.Label(self.side, text="DIFFICULTY LEVEL", fg="#64748B", bg=COLOR_SIDEBAR).pack(anchor="w", pady=(10,0))
        self.diff_var = tk.StringVar(value="Medium")
        self.diff_menu = ttk.Combobox(self.side, textvariable=self.diff_var, values=["Easy", "Medium", "Hard"], state="readonly")
        self.diff_menu.pack(fill="x", pady=5)
        # BUG FIX: Reset focus after selection
        self.diff_menu.bind("<<ComboboxSelected>>", lambda e: self.root.focus())

        self.go_btn = tk.Button(self.side, text="EXECUTE RACE", bg=COLOR_GOAL, fg=COLOR_BG, font=("Arial", 11, "bold"), command=self.start_race, relief="flat", pady=12)
        self.go_btn.pack(pady=20, fill="x")

        self.rst_btn = tk.Button(self.side, text="SYSTEM RESET", bg=COLOR_AI, fg="white", font=("Arial", 11, "bold"), command=self.reset_game, relief="flat", pady=10)
        self.rst_btn.pack(pady=5, fill="x")

        self.hud = tk.LabelFrame(self.side, text=" LIVE FEED ", fg=COLOR_PLAYER, bg=COLOR_SIDEBAR, padx=10, pady=10)
        self.hud.pack(side="bottom", fill="x", pady=20)
        
        self.clock_lbl = tk.Label(self.hud, text="TIMER: 0.0s", fg="white", bg=COLOR_SIDEBAR, font=("Courier", 12, "bold"))
        self.clock_lbl.pack(anchor="w")
        
        self.status_lbl = tk.Label(self.hud, text="STATUS: Ready", fg="#94A3B8", bg=COLOR_SIDEBAR, font=("Courier", 9), wraplength=200, justify="left")
        self.status_lbl.pack(pady=10)

        self.canvas = tk.Canvas(self.root, width=GRID_SIZE*CELL_SIZE, height=GRID_SIZE*CELL_SIZE, bg=COLOR_BG, highlightthickness=0)
        self.canvas.pack(expand=True)

    def draw_grid(self):
        self.canvas.delete("all")
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x1, y1 = c*CELL_SIZE, r*CELL_SIZE
                color = COLOR_PATH
                if MAZE[r][c] == 1: color = COLOR_WALL
                elif (r, c) in self.ai_trail: color = COLOR_TRAIL
                if [r, c] == [14, 14]: 
                    self.canvas.create_rectangle(x1, y1, x1+CELL_SIZE, y1+CELL_SIZE, fill=COLOR_GOAL, outline="white")
                    continue
                self.canvas.create_rectangle(x1, y1, x1+CELL_SIZE, y1+CELL_SIZE, fill=color, outline="#0F172A")

        px, py = self.player_pos[1]*CELL_SIZE, self.player_pos[0]*CELL_SIZE
        self.canvas.create_oval(px+8, py+8, px+CELL_SIZE-8, py+CELL_SIZE-8, fill=COLOR_PLAYER, outline="white", width=2)
        ax, ay = self.ai_pos[1]*CELL_SIZE, self.ai_pos[0]*CELL_SIZE
        self.canvas.create_oval(ax+8, ay+8, ax+CELL_SIZE-8, ay+CELL_SIZE-8, fill=COLOR_AI, outline="white", width=2)

    def reset_game(self):
        self.is_running = False
        self.race_id += 1
        self.player_pos = [0, 0]
        self.ai_pos = [0, 0]
        self.ai_trail = set()
        self.player_time = None
        self.ai_time = None
        self.clock_lbl.config(text="TIMER: 0.0s")
        self.status_lbl.config(text="STATUS: Reset Complete")
        self.draw_grid()
        self.root.focus_set() # Ensure focus is reset

    def start_race(self):
        self.reset_game()
        self.is_running = True
        self.start_time = time.time()
        self.tick()
        path = solve_maze(self.algo_box.get(), MAZE, [0,0], [14,14])
        self.ai_engine(path, self.race_id)

    def tick(self):
        if self.is_running:
            self.clock_lbl.config(text=f"TIMER: {time.time()-self.start_time:.1f}s")
            self.root.after(100, self.tick)

    def ai_engine(self, path, rid):
        if not self.is_running or not path or rid != self.race_id: return
        r, c = self.ai_pos
        self.ai_trail.add((r, c))
        
        neighbors = []
        for dr, dc, n in [(-1,0,'Up'),(1,0,'Down'),(0,-1,'Left'),(0,1,'Right')]:
            nr, nc = r+dr, c+dc
            if 0<=nr<GRID_SIZE and 0<=nc<GRID_SIZE and MAZE[nr][nc]==0:
                neighbors.append(([nr,nc], n))

        if len(neighbors) > 2:
            diff = self.diff_var.get()
            error_rate = 0.7 if diff == "Easy" else 0.4 if diff == "Medium" else 0.1
            if random.random() < error_rate:
                self.status_lbl.config(text="AI STATUS: Confused at Junction!", fg="#FBBF24")
                wrong = [n for n in neighbors if n[1] != path[0]]
                if wrong:
                    self.ai_pos = random.choice(wrong)[0]
                    self.draw_grid()
                    new_p = solve_maze(self.algo_box.get(), MAZE, self.ai_pos, [14,14])
                    self.root.after(400, lambda: self.ai_engine(new_p, rid))
                    return

        move = path.pop(0)
        if move == 'Up': self.ai_pos[0] -= 1
        elif move == 'Down': self.ai_pos[0] += 1
        elif move == 'Left': self.ai_pos[1] -= 1
        elif move == 'Right': self.ai_pos[1] += 1
        self.draw_grid()
        if self.ai_pos == [14, 14]:
            self.ai_time = time.time() - self.start_time
            self.check_race_finish()
            return
        self.root.after(200, lambda: self.ai_engine(path, rid))

    def move_player(self, e):
        if not self.is_running: return
        r, c = self.player_pos
        if e.keysym == 'Up': r -= 1
        elif e.keysym == 'Down': r += 1
        elif e.keysym == 'Left': c -= 1
        elif e.keysym == 'Right': c += 1
        if 0<=r<GRID_SIZE and 0<=c<GRID_SIZE and MAZE[r][c]==0:
            self.player_pos = [r, c]
            self.draw_grid()
            if self.player_pos == [14, 14]:
                self.player_time = time.time() - self.start_time
                self.status_lbl.config(text="PLAYER FINISHED!", fg=COLOR_PLAYER)
                self.check_race_finish()

    def check_race_finish(self):
        if self.player_time is not None and self.ai_time is not None:
            self.is_running = False
            self.show_results()

    def show_results(self):
        res = tk.Toplevel(self.root)
        res.title("Post-Race Analysis")
        res.geometry("400x400")
        res.configure(bg=COLOR_SIDEBAR)
        tk.Label(res, text="📊 FINAL PERFORMANCE 📊", fg=COLOR_GOAL, bg=COLOR_SIDEBAR, font=("Arial", 14, "bold")).pack(pady=20)
        summary = f"PLAYER TIME: {self.player_time:.2f}s\n\nAI TIME: {self.ai_time:.2f}s\n\nALGO: {self.algo_box.get()}\nDIFFICULTY: {self.diff_var.get()}"
        tk.Label(res, text=summary, fg="white", bg=COLOR_BG, font=("Courier", 12), padx=20, pady=20, borderwidth=2, relief="groove").pack(pady=10)
        winner = "🏆 YOU DEFEATED THE AI! 🏆" if self.player_time < self.ai_time else "💀 AI OUTPERFORMED YOU! 💀"
        color = COLOR_GOAL if self.player_time < self.ai_time else COLOR_AI
        tk.Label(res, text=winner, fg=color, bg=COLOR_SIDEBAR, font=("Arial", 12, "bold")).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use('clam')
    app = NeuralVizFinal(root)
    root.mainloop()
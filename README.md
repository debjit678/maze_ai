# MAZE_AI
Neural-Viz is a real-time AI visualization tool and competitive game that demonstrates the power of search algorithms in a pathfinding environment. Built with Python and Tkinter, it allows users to race against a "Human-like" AI that utilizes BFS, DFS, and A* algorithms to navigate complex mazes.
🧠 Neural-Viz: AI Search Engine & Maze Racer

Neural-Viz is a real-time AI visualization tool and competitive game that demonstrates the power of search algorithms in a pathfinding environment. Built with Python and Tkinter, it allows users to race against a "Human-like" AI that utilizes BFS, DFS, and A* algorithms to navigate complex mazes.
🚀 Key Features

    Multi-Algorithm AI: Toggle between Breadth-First Search (Shortest Path), Depth-First Search (Exploratory), and A (Heuristic-Optimized)*.

    Stochastic Junction Confusion: A custom-built logic that simulates human error. The AI analyzes its surroundings and has a probability-based chance of taking a "wrong turn" specifically at maze divergences.

    Real-Time Performance Analytics: Post-race dashboard comparing Manual vs. AI latency (time taken) to evaluate algorithm efficiency.

    Dynamic Difficulty: Three levels of AI "Intelligence" (Easy, Medium, Hard) that adjust the probability of decision-making errors.

    Professional UI: A modern Obsidian/Slate-themed dashboard with real-time HUD and visual "Thought Trails."

🛠️ Technical Implementation
Algorithms

    A Search:* Implemented using a Priority Queue (heapq) and Manhattan Distance as the heuristic function (h(n)), ensuring optimal pathfinding with reduced state-space exploration.

    BFS: Guaranteed shortest path discovery using a FIFO queue.

    DFS: Demonstrated for its memory efficiency in specific tree-structures, though non-optimal for maze shortest paths.

Decision Logic

The AI employs a Divergence Check at every step. By evaluating neighboring nodes, the AI detects intersections (where available paths >2). At these points, a stochastic roll determines if the AI follows the calculated path or commits to an exploratory error.
📦 Installation & Usage

    Clone the repository:
    Bash

    git clone https://github.com/YOUR_USERNAME/Neural-Viz-AI.git

    Run the application:
    Ensure you have Python installed, then run:
    Bash

    python main.py

    Packaging:
    To create a standalone executable:
    Bash

    python -m PyInstaller --noconsole --onefile --name="NeuralMaze" main.py

🎓 Academic Context

This project was developed for a 2nd-year Artificial Intelligence course to demonstrate the practical application of Informed vs. Uninformed Search Strategies and the simulation of non-deterministic behavior in autonomous agents.

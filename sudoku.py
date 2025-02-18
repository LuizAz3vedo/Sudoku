import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
import random

sudoku_board = np.array([
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
])

fixed_positions = {(i, j) for i in range(9) for j in range(9) if sudoku_board[i, j] != 0}
solution_steps = []

def is_valid(board, row, col, num):
    if num in board[row, :] or num in board[:, col]:
        return False
    box_x, box_y = (row // 3) * 3, (col // 3) * 3
    if num in board[box_x:box_x+3, box_y:box_y+3]:
        return False
    return True

def find_best_empty_cell(board):
    best_cell = None
    min_options = 10  
    for i in range(9):
        for j in range(9):
            if board[i, j] == 0:
                possibilities = {num for num in range(1, 10) if is_valid(board, i, j, num)}
                if len(possibilities) < min_options:
                    min_options = len(possibilities)
                    best_cell = (i, j)
                if min_options == 1:  
                    return best_cell  
    return best_cell

def solve_sudoku(board):
    empty = find_best_empty_cell(board)
    if not empty:
        return True  

    row, col = empty
    possibilities = sorted([num for num in range(1, 10) if is_valid(board, row, col, num)])

    if possibilities:
        wrong_attempt = random.choice([num for num in range(1, 10) if num not in possibilities]) if random.random() < 0.4 else None

        if wrong_attempt:
            board[row, col] = wrong_attempt
            solution_steps.append((row, col, wrong_attempt, 'remove'))  
            board[row, col] = 0  

        for num in possibilities:
            board[row, col] = num
            solution_steps.append((row, col, num, 'add'))
            
            if solve_sudoku(board):
                return True

            solution_steps.append((row, col, num, 'remove'))
            board[row, col] = 0  

    return False  

solve_sudoku(sudoku_board.copy())

def create_sudoku_graph():
    G = nx.Graph()
    for i in range(9):
        for j in range(9):
            G.add_node((i, j))
    
    edges_row, edges_col, edges_box = [], [], []
    for i in range(9):
        for j in range(9):
            for k in range(9):
                if k != j:
                    edges_row.append(((i, j), (i, k)))
                if k != i:
                    edges_col.append(((i, j), (k, j)))
            
            region_i, region_j = i // 3, j // 3
            for x in range(region_i * 3, (region_i + 1) * 3):
                for y in range(region_j * 3, (region_j + 1) * 3):
                    if (x, y) != (i, j):
                        edges_box.append(((i, j), (x, y)))
    
    G.add_edges_from(edges_row + edges_col + edges_box)
    return G, edges_row, edges_col, edges_box

def get_grid_layout():
    return {(i, j): (j, -i) for i in range(9) for j in range(9)}

def animate_sudoku():
    G, edges_row, edges_col, edges_box = create_sudoku_graph()
    
    initial_pos = nx.circular_layout(G)
    final_pos = get_grid_layout()
    
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor('#f5f5f5')

    transition_frames = 20
    solve_frames = len(solution_steps) * 2
    num_frames = transition_frames + solve_frames

    def update(frame):
        ax.clear()
        ax.set_facecolor('#f5f5f5')

        transition_progress = min(1, frame / transition_frames)
        interp_pos = {
            node: (
                initial_pos[node][0] * (1 - transition_progress) + final_pos[node][0] * transition_progress,
                initial_pos[node][1] * (1 - transition_progress) + final_pos[node][1] * transition_progress
            ) for node in G.nodes()
        }

        nx.draw(G, interp_pos, ax=ax, node_size=300, node_color='white', edgecolors='black', linewidths=0.8)
        nx.draw_networkx_edges(G, interp_pos, edgelist=edges_row, edge_color='red', alpha=0.2, ax=ax)
        nx.draw_networkx_edges(G, interp_pos, edgelist=edges_col, edge_color='blue', alpha=0.2, ax=ax)
        nx.draw_networkx_edges(G, interp_pos, edgelist=edges_box, edge_color='green', alpha=0.2, ax=ax)

        for (i, j) in fixed_positions:
            ax.text(final_pos[(i, j)][0], final_pos[(i, j)][1], str(sudoku_board[i, j]), 
                    fontsize=16, ha='center', va='center', fontweight='bold', color='black')

        if frame >= transition_frames:
            num_to_show = (frame - transition_frames) // 2
            for k in range(num_to_show):
                if k < len(solution_steps):
                    i, j, value, action = solution_steps[k]
                    color = "blue" if action == "add" else "red"
                    ax.text(final_pos[(i, j)][0], final_pos[(i, j)][1], str(value) if value > 0 else "", 
                            fontsize=16, ha='center', va='center', fontweight='bold', color=color)

        ax.set_xticks(range(9))
        ax.set_yticks(range(-8, 1))
        ax.set_xticklabels(range(1, 10))
        ax.set_yticklabels(range(1, 10)[::-1])
        ax.set_title("Resolução do Sudoku com Grafo de Restrições", fontsize=18, fontweight="bold")

        for i in range(10):
            ax.plot([i-0.5, i-0.5], [-8.5, 0.5], color="gray", lw=1, alpha=0.5)
            ax.plot([-0.5, 8.5], [-i+0.5, -i+0.5], color="gray", lw=1, alpha=0.5)

    ani = FuncAnimation(fig, update, frames=num_frames, interval=30, repeat=False)
    #ani.save("sudoku_solver.gif", writer=PillowWriter(fps=10))
    plt.show()

animate_sudoku()

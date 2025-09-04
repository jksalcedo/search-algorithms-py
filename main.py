# Simple GUI for Search Algorithms
import tkinter as tk
from tkinter import ttk, messagebox
from dfs import dfs
from bfs import bfs
from gbfs import gbfs
from astar import astar
from graph_data import graph, straight_line_heuristic

ALGORITHMS = {
    'DFS': dfs,
    'BFS': bfs,
    'GBFS': lambda g, s, go: gbfs(g, s, go, straight_line_heuristic),
    'A*': lambda g, s, go: astar(g, s, go, straight_line_heuristic)
}

class SearchGUI:
    def __init__(self, root):
        self.root = root
        root.title('AI Search Algorithms')
        
        ttk.Label(root, text='Start:').grid(row=0, column=0)
        self.start_var = tk.StringVar(value='Arad')
        self.start_entry = ttk.Combobox(root, textvariable=self.start_var, values=list(graph.keys()))
        self.start_entry.grid(row=0, column=1)
        
        ttk.Label(root, text='Goal:').grid(row=1, column=0)
        self.goal_var = tk.StringVar(value='Bucharest')
        self.goal_entry = ttk.Combobox(root, textvariable=self.goal_var, values=list(graph.keys()))
        self.goal_entry.grid(row=1, column=1)
        
        ttk.Label(root, text='Algorithm:').grid(row=2, column=0)
        self.alg_var = tk.StringVar(value='DFS')
        self.alg_menu = ttk.Combobox(root, textvariable=self.alg_var, values=list(ALGORITHMS.keys()))
        self.alg_menu.grid(row=2, column=1)
        
        self.run_btn = ttk.Button(root, text='Run', command=self.run_search)
        self.run_btn.grid(row=3, column=0, pady=5)

        self.visual_btn = ttk.Button(root, text='Visualize Path', command=self.visualize_path)
        self.visual_btn.grid(row=3, column=1, pady=5)

        self.result_box = tk.Text(root, height=5, width=40)
        self.result_box.grid(row=4, column=0, columnspan=2)
    
    def run_search(self):
        start = self.start_var.get()
        goal = self.goal_var.get()
        alg = self.alg_var.get()
        if start not in graph or goal not in graph:
            messagebox.showerror('Error', 'Invalid start or goal node!')
            self.current_path = None
            return
        func = ALGORITHMS[alg]
        path = func(graph, start, goal)
        self.current_path = path
        self.result_box.delete('1.0', tk.END)
        if path:
            self.result_box.insert(tk.END, f'Path: {" -> ".join(path)}')
        else:
            self.result_box.insert(tk.END, 'No path found.')

    def visualize_path(self):
        try:
            from visualize_path import show_path
        except ImportError:
            messagebox.showerror('Error', 'visualize_path file not found!')
            return
        if not hasattr(self, 'current_path') or not self.current_path:
            messagebox.showinfo('Info', 'Run a search first to get a path!')
            return
        show_path(self.current_path, title=f"{self.alg_var.get()} Path: {self.start_var.get()} to {self.goal_var.get()}")

if __name__ == '__main__':
    root = tk.Tk()
    gui = SearchGUI(root)
    root.mainloop()

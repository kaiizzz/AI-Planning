'''
    Main.py 
    Author: Kailiang Zhu
    Version: V1.0
    Time: 30/08/2024
    Description: This file is used to run the project.
'''

from GraphCreation import Graph, Node
from Search import Search
import tkinter as tk
import math

# Global variable to hold the graph object
graph = None

def add_node():
    user_input = entry.get()  # Get the text from the entry field
    # Example input format: "1 1 1"
    tokens = user_input.split(maxsplit=2)
    
    if len(tokens) == 3:
        node_id = tokens[0]
        position = (int(tokens[1]), int(tokens[2]))  # Convert string "(x,y)" to tuple (x,y)
        graph.add_node(node_id, position)
        label.config(text=f"Node {node_id} added at position {position}")
    else:
        label.config(text="Invalid node input. Use format: <id> (<x>,<y>)")
    
    # Clear the input field
    entry.delete(0, tk.END)
    
    # Redraw the graph on the canvas
    canvas.delete("all")
    draw_graph_on_canvas(canvas, graph)

def add_edge():
    user_input = entry.get()  # Get the text from the entry field
    # Example input format: "1 2 3"
    tokens = user_input.split()
    
    if len(tokens) == 3:
        node1_id = tokens[0]
        node2_id = tokens[1]
        cost = float(tokens[2])
        graph.add_edge(node1_id, node2_id, cost)  # Assuming default weight is 1
        label.config(text=f"Edge added between {node1_id} and {node2_id} with cost {cost}")
    else:
        label.config(text="Invalid edge input. Use format: <node1_id> <node2_id> <cost>")
    
    # Clear the input field
    entry.delete(0, tk.END)
    
    # Redraw the graph on the canvas
    canvas.delete("all")
    draw_graph_on_canvas(canvas, graph)

def draw_graph_on_canvas(canvas, graph, path_nodes=None, path_edges=None, start=None, goal=None):
    nodes = graph.get_nodes()
    edges = graph.get_edges()

    # Get canvas dimensions to calculate the center
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    center_x = canvas_width // 2
    center_y = canvas_height // 2

    # Set to keep track of drawn edges
    done = set()

    # Draw edges
    for edge in edges:
        node1 = edge[0]
        node2 = edge[1]
        weight = edge[2]  # Assuming the edge weight is stored in the third element

        # Ensure each edge is only drawn once
        edge_id = tuple(sorted((node1.id, node2.id)))
        if edge_id in done:
            continue
        done.add(edge_id)

        x1, y1 = node1.get_position()
        x2, y2 = node2.get_position()

        # Convert graph coordinates to canvas coordinates
        canvas_x1 = center_x + x1 * 50
        canvas_y1 = center_y - y1 * 50  # Inverted y-axis
        canvas_x2 = center_x + x2 * 50
        canvas_y2 = center_y - y2 * 50  # Inverted y-axis

        # Set color based on whether the edge is in the path
        edge_color = "green" if path_edges and edge_id in path_edges else "black"
        #edge_color = "red" if start and goal and (node1.id == start.id or node2.id == start.id or node1.id == goal.id or node2.id == goal.id) else edge_color

        # Draw the line between nodes
        canvas.create_line(canvas_x1, canvas_y1, canvas_x2, canvas_y2, fill=edge_color)

        # Calculate the midpoint of the line
        mid_x = (canvas_x1 + canvas_x2) / 2
        mid_y = (canvas_y1 + canvas_y2) / 2

        # Calculate the slope of the line
        dx = canvas_x2 - canvas_x1
        dy = canvas_y2 - canvas_y1
        length = math.sqrt(dx**2 + dy**2)

        # Normalize the direction vector and calculate perpendicular direction
        nx = -dy / length
        ny = dx / length

        # Offset the midpoint in the perpendicular direction
        offset = 20  # Change this value to adjust the amount of offset
        offset_x = mid_x + nx * offset
        offset_y = mid_y + ny * offset

        # Draw the edge cost near the middle of the line with offset
        canvas.create_text(offset_x, offset_y, text=str(weight), fill="red")

    # Draw nodes
    for node in nodes:
        x, y = node.get_position()

        # Convert graph coordinates to canvas coordinates
        canvas_x = center_x + x * 50
        canvas_y = center_y - y * 50  # Inverted y-axis

        # Set color based on whether the node is in the path
        node_color = "purple" if path_nodes and node.id in path_nodes else "blue"
        node_color = "green" if start and node.id == start.id else node_color
        node_color = "red" if goal and node.id == goal.id else node_color
        # Draw the node
        canvas.create_oval(canvas_x-10, canvas_y-10, canvas_x+10, canvas_y+10, fill=node_color)
        canvas.create_text(canvas_x, canvas_y, text=str(node.id), fill="white")



def search(algorithm, heuristic, start=None, goal=None):
    if graph.get_node("I") is not None:
        start = graph.get_node("I")  # Top-left corner
    if graph.get_node("G") is not None:
        goal = graph.get_node("G")   # Bottom-right corner
    s = Search(algorithm, graph, start, goal, heuristic)
    path = s.search()
    if path is not None:
        path.insert(0, start.id)
        label.config(text=f"Path found: {path}")
        path_edges = set()
        for i in range(len(path) - 1):
            edge_id = tuple(sorted((path[i], path[i+1])))
            path_edges.add(edge_id)
    else:
        label.config(text="No path found")
    
    # Draw the graph with the path highlighted
    canvas.delete("all")
    draw_graph_on_canvas(canvas, graph, path, path_edges, start, goal)

def clear_graph():
    global graph
    graph = Graph()  # Reset the graph
    canvas.delete("all")  # Clear the canvas
    label.config(text="Graph cleared")

def main():
    global graph
    graph = Graph()

    # You can initialize the graph with nodes and edges if needed
    return graph

def create_window():
    global canvas, entry, label
    
    # Initialize the graph
    graph = main()

    # # Function to add nodes in a grid pattern
    # def add_grid_nodes(graph, width, height):
    #     for x in range(width):
    #         for y in range(height):
    #             node_id = f"{x}_{y}"
    #             graph.add_node(node_id, (x, y))

    # # Function to add edges in a grid pattern
    # def add_grid_edges(graph, width, height):
    #     for x in range(width):
    #         for y in range(height):
    #             node_id = f"{x}_{y}"
    #             # Connect to the right neighbor
    #             if x < width - 1:
    #                 right_neighbor = f"{x+1}_{y}"
    #                 graph.add_edge(node_id, right_neighbor, 1)
    #             # Connect to the bottom neighbor
    #             if y < height - 1:
    #                 bottom_neighbor = f"{x}_{y+1}"
    #                 graph.add_edge(node_id, bottom_neighbor, 1)

    # # Create a 10x10 grid
    # width, height = 6, 6

    # # Adding nodes
    # add_grid_nodes(graph, width, height)

    # # Adding edges
    # add_grid_edges(graph, width, height)

    # Set the start and goal nodes for demonstration

    
    # Create the main window
    window = tk.Tk()
    
    # Set the window title
    window.title("AI Planner")
    
    # Set the window size
    window.geometry("1920x1080")
    
    # Create an entry widget (input field)
    entry = tk.Entry(window, width=50)
    entry.pack(pady=10)
    
    # Create buttons for adding nodes and edges
    button_node = tk.Button(window, text="Add Node", command=add_node)
    button_node.pack(pady=10)
    
    button_edge = tk.Button(window, text="Add Edge", command=add_edge)
    button_edge.pack(pady=10)

    # Dropdown for the heuristic
    heuristic = tk.StringVar(window)
    heuristic.set("Manhattan")  # Default value
    dropdown_heuristic = tk.OptionMenu(window, heuristic, "Manhattan", "Euclidean", "Chebyshev", "h+", "hadd", "hmax", "hff", "badHeuristic")
    dropdown_heuristic.pack(pady=10)

    # Dropdown for the search algorithm
    algorithm = tk.StringVar(window)
    algorithm.set("A*")  # Default value
    dropdown_algorithm = tk.OptionMenu(window, algorithm, "A*", "Greedy", "Uniform Cost")
    dropdown_algorithm.pack(pady=10)

    # Create a button to run the search algorithm
    button_search = tk.Button(window, text="Search", command=lambda: search(algorithm.get(), heuristic.get()))
    button_search.pack(pady=10)

    # Create a button to clear the graph
    button_clear = tk.Button(window, text="Clear Graph", command=clear_graph)
    button_clear.pack(pady=10)
    
    # Create a label to display the output
    label = tk.Label(window, text="")
    label.pack(pady=10)
    
    # Create a canvas widget for drawing the graph
    canvas = tk.Canvas(window, width=1920, height=1080, bg="white")
    canvas.pack(pady=20)
    
    
    
    # Start the GUI event loop
    window.mainloop()

if __name__ == "__main__":
    create_window()

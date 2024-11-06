import sys

# Selection Sort
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    print("Sorted array:", arr)

# Prim's MST
def prim_mst(graph, start_vertex=0):
    num_vertices = len(graph)
    selected = [False] * num_vertices
    selected[start_vertex] = True  # Mark the start vertex as selected
    mst_cost = 0
    num_edges = 0
    
    # Continue until we select all vertices
    while num_edges < num_vertices - 1:
        min_edge = sys.maxsize
        u = v = -1
        
        # Find the minimum weight edge connecting selected and unselected vertices
        for i in range(num_vertices):
            if selected[i]:
                for j in range(num_vertices):
                    if not selected[j] and graph[i][j] > 0:  # Ensure there's an edge
                        if graph[i][j] < min_edge:
                            min_edge = graph[i][j]
                            u, v = i, j
        
        if u != -1 and v != -1:
            selected[v] = True  # Mark the vertex as selected
            mst_cost += min_edge  # Add the edge weight to the MST cost
            num_edges += 1  # Increment the number of edges in the MST
    
    print(f"Total cost of MST starting from vertex {start_vertex + 1}: {mst_cost}")

# Menu system
def menu():
    while True:
        print("\nMain Menu:")
        print("1. Selection Sort")
        print("2. Prim's MST")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            arr = list(map(int, input("Enter numbers separated by space: ").split()))
            selection_sort(arr)
        elif choice == '2':
            num_vertices = int(input("Enter number of vertices: "))
            graph = [[0] * num_vertices for _ in range(num_vertices)]
            num_edges = int(input("Enter number of edges: "))
            for _ in range(num_edges):
                u, v, weight = map(int, input("Enter edge (u v weight): ").split())
                u -= 1  # Adjust index to be 0-based
                v -= 1  # Adjust index to be 0-based
                graph[u][v] = weight
                graph[v][u] = weight
            start_vertex = int(input("Enter the start vertex (1-based index): ")) - 1
            prim_mst(graph, start_vertex)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()

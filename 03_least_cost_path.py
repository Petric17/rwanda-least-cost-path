import numpy as np
import matplotlib.pyplot as plt
import heapq

dem_patch = np.load("/kaggle/working/rwanda_dem_patch_1000x1000.npy")
cost_surface = np.load("/kaggle/working/cost_surface_1000x1000.npy")

rows, cols = cost_surface.shape

start_node = (160, 160)
target_node = (860, 860)

def run_dijkstra(cost_grid, start, target):
    """
    Dijkstra Algorithm with priority queue for raster grid with 8 neighbors 
    """
    sr, sc = start
    tr, tc = target
    
    # Matrix of accumulated distances/costs
    dist = np.full((rows, cols), np.inf, dtype=np.float32)
    dist[sr, sc] = 0.0

    parent = {}
    pq = [(0.0, sr, sc)]
    
    # Directions of movement (8 neighbors) and corresponding lengths
    moves = [
        (-1, 0, 1.0), (1, 0, 1.0), (0, -1, 1.0), (0, 1, 1.0),               # Cardinali
        (-1, -1, 1.4142), (-1, 1, 1.4142), (1, -1, 1.4142), (1, 1, 1.4142) # Diagonale
    ]
    
    visited_nodes = 0 
    while pq:
        d, r, c = heapq.heappop(pq)
        visited_nodes += 1
        
        # If we hit the target we stop
        if (r, c) == (tr, tc):
            print(f"Target hit: {visited_nodes} nodes explored")
            break
            
        if d > dist[r, c]:
            continue
            
        current_cell_cost = cost_grid[r, c]
        
        for dr, dc, step_len in moves:
            nr, nc = r + dr, c + dc
            
            # Check matrix limits
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbor_cost = cost_grid[nr, nc]
                
                # Ignore impassable barriers
                if neighbor_cost >= 9000.0:
                    continue
                    
                # Crossing cost = average cost between cells * physical step length
                step_cost = ((current_cell_cost + neighbor_cost) / 2.0) * step_len
                new_dist = d + step_cost
                
                if new_dist < dist[nr, nc]:
                    dist[nr, nc] = new_dist
                    parent[(nr, nc)] = (r, c)
                    heapq.heappush(pq, (new_dist, nr, nc))

    # Reconstruction of the route from the target back to the start (tot in interiorul functiei)
    path = []
    curr = (tr, tc)
    if curr not in parent and curr != start:
        print("Attention: No feasible route was found!")
        return []
        
    while curr != start:
        path.append(curr)
        curr = parent[curr]
    path.append(start)
    
    return path[::-1]


# Run the algorithm least cost path
optimal_path = run_dijkstra(cost_surface, start_node, target_node)

if optimal_path:
    path_r = [p[0] for p in optimal_path]
    path_c = [p[1] for p in optimal_path]
    
    # Visualization
    plt.figure(figsize=(12, 10))
    
    # Show background terrain
    plt.imshow(dem_patch, cmap='terrain', alpha=0.85)
    plt.colorbar(label="Altitude (m)")
    
    # Direct routing
    plt.plot([start_node[1], target_node[1]], [start_node[0], target_node[0]], 
             color='red', linestyle='--', linewidth=2.5, label='Direct Route')
    
    # Optimal route
    plt.plot(path_c, path_r, color='cyan', linewidth=3.0, label='Optimal Route (Least-Cost Path)')
    plt.scatter([start_node[1]], [start_node[0]], color='lime', s=140, edgecolors='black', zorder=5, label='Start')
    plt.scatter([target_node[1]], [target_node[0]], color='red', s=140, edgecolors='black', zorder=5, label='Destination')
    
    plt.title("Optimization of the Transit Route across Rwanda’s Terrain (10 km x 10 km)", fontsize=13)
    plt.xlabel("East (pixels - 10m)")
    plt.ylabel("North (pixels - 10m)")
    plt.legend(loc='upper right')
    
    output_png = "/kaggle/working/Rwanda_Optimal_Route.png"
    plt.savefig(output_png, dpi=300, bbox_inches='tight')
    plt.close()
    

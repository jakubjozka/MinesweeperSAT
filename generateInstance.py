import random
import sys

def generate_random_instance(rows, cols, mine_density=0.2, reveal_density=0.3):
    grid = [[False for _ in range(cols)] for _ in range(rows)]
    
    total_cells = rows * cols
    num_mines = int(total_cells * mine_density)
    
    mine_positions = set()
    while len(mine_positions) < num_mines:
        r = random.randint(0, rows - 1)
        c = random.randint(0, cols - 1)
        mine_positions.add((r, c))
    
    for (r, c) in mine_positions:
        grid[r][c] = True 
    
    def count_mines(r, c):
        if grid[r][c]: 
            return -1
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc]:
                    count += 1
        return count
    
    numbers = [[count_mines(r, c) for c in range(cols)] for r in range(rows)]
    
    revealed = [[False for _ in range(cols)] for _ in range(rows)]
    
    non_mine_cells = [(r, c) for r in range(rows) for c in range(cols) if not grid[r][c]]
    num_reveal = int(len(non_mine_cells) * reveal_density)
    
    cells_to_reveal = random.sample(non_mine_cells, min(num_reveal, len(non_mine_cells)))
    for (r, c) in cells_to_reveal:
        revealed[r][c] = True
    
    print(f"{rows} {cols}")
    for r in range(rows):
        row_str = []
        for c in range(cols):
            if revealed[r][c]:
                row_str.append(str(numbers[r][c]))
            else:
                row_str.append("?")
        print(" ".join(row_str))

def generate_dense_instance(size):
    print(f"{size} {size}")
    for r in range(size):
        row = []
        for c in range(size):
            if (r + c) % 2 == 0:
                num = ((r % 3) + (c % 3)) % 5
                row.append(str(num))
            else:
                row.append("?")
        print(" ".join(row))

def generate_sparse_hard_instance(size):
    print(f"{size} {size}")
    for r in range(size):
        row = []
        for c in range(size):
            if r == 0 or r == size-1 or c == 0 or c == size-1:
                num = (r + c) % 4
                row.append(str(num))
            elif (r % 5 == 2 and c % 5 == 2):
                row.append("3")
            elif (r % 5 == 2 and c % 5 == 3):
                row.append("4")
            else:
                row.append("?")
        print(" ".join(row))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python generate_instance.py random <rows> <cols> [mine_density] [reveal_density]")
        print("  python generate_instance.py dense <size>")
        print("  python generate_instance.py sparse <size>")
        print()
        print("Examples:")
        print("  python generate_instance.py random 20 20 0.2 0.3")
        print("  python generate_instance.py dense 100")
        print("  python generate_instance.py sparse 150")
        sys.exit(1)
    
    mode = sys.argv[1]
    
    if mode == "random":
        rows = int(sys.argv[2])
        cols = int(sys.argv[3])
        mine_density = float(sys.argv[4]) if len(sys.argv) > 4 else 0.2
        reveal_density = float(sys.argv[5]) if len(sys.argv) > 5 else 0.3
        generate_random_instance(rows, cols, mine_density, reveal_density)
    
    elif mode == "dense":
        size = int(sys.argv[2])
        generate_dense_instance(size)
    
    elif mode == "sparse":
        size = int(sys.argv[2])
        generate_sparse_hard_instance(size)
    
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)
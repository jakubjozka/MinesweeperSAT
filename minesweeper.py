import subprocess
from argparse import ArgumentParser

def load_instance(input_file_name):
    global ROWS, COLS
    grid = []

    with open(input_file_name, 'r') as file:
        first_line = next(file).split()
        ROWS, COLS = int(first_line[0]), int(first_line[1])

        for line in file:
            line = line.split()
            if line:
                grid.append(line)
    
    return grid

def encode (grid):
    """
    Encode the Minesweeper instance as a CNF formula

    Variables:
    - Mine(r, c): cell at row r, column c contains a mine

    Constraints:
    - If a cell shows number k, exactly k of its neighbors must contain mines
    - If a cell is revealed (has a number), it cannot contain a mine

    Return:
    - CNF: list of clauses (each clause is a list of integers ending with 0)
    - nr_vars: total number of variables
    """
    cnf = []
    nr_vars = ROWS * COLS

    for r in range(ROWS):
        for c in range(COLS):
            cell = grid[r][c]

            if cell.isdigit():
                k = int(cell)

                cnf.append([-pos_to_mineID(r, c), 0])
                neigbors = get_neighbors(r, c)

                add_exactly_k_constraints(cnf, neigbors, k)
    
    return (cnf, nr_vars)

def pos_to_mineID(r, c):
    return r * COLS + c + 1

def get_neighbors(r, c):
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                neighbors.append((nr, nc))
    return neighbors

def add_exactly_k_constraints(cnf, neighbors, k):
    """
    Add constraints that exactly k of the neighbors cells contain mines

    - "At most k": for every subset of (k+1) neighbors, at least one is NOT a mine
    - "At least k": for every subset of (n-k+1) neighbors, at least one IS a mine

    where n = total number of neighbors
    """
    from itertools import combinations

    n = len(neighbors)

    if k < n:
        for subset in combinations(neighbors, k + 1):
            clause = []
            for (nr, nc) in subset:
                clause.append(-pos_to_mineID(nr, nc))
            clause.append(0)
            cnf.append(clause)

    if k > 0:
        for subset in combinations(neighbors, n - k + 1):
            clause = []
            for (nr, nc) in subset:
                clause.append(pos_to_mineID(nr, nc))
            clause.append(0)
            cnf.append(clause)

def call_solver(cnf, nr_vars, output_name, solver_name, verbosity):
    with open(output_name, 'w') as file:
        file.write("p cnf " + str(nr_vars) + " " + str(len(cnf)) + "\n")
        for clause in cnf:
            file.write(' '.join(str(lit) for lit in clause) + '\n')

    return subprocess.run(['./' + solver_name, '-model', '-verb=' + str(verbosity), output_name],
                          stdout=subprocess.PIPE)

def print_result(result, grid):
    for line in result.stdout.decode('utf-8').split('\n'):
        print(line)

    if result.returncode == 20:
        print("\n" + "="*50)
        print("UNSATISFIABLE - No valid mine configuration exists")

    model = []
    for line in result.stdout.decode('utf-8').split('\n'):
        if line.startswith("v"):
            vars = line.split(" ")
            vars.remove("v")
            model.extend(int(v) for v in vars)
    model.remove(0)

    print("\n" + "="*50)
    print("SOLUTION - Mine Configuration:")
    print("\n" + "="*50)

    for r in range(ROWS):
        for c in range(COLS):
            var_id = pos_to_mineID(r, c)
            if model[var_id - 1] > 0:
                print("M", end=" ")
            else:
                if grid[r][c].isdigit():
                    print(grid[r][c], end=" ")
                else:
                    print(".", end=" ")
        print()

if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument(
        "-i",
        "--input",
        default="input.in",
        type=str,
        help="The input file name (default: input.in)"
    )
    parser.add_argument(
        "-o",
        "--output",
        default="formula.cnf",
        type=str,
        help="Ouput file for the DIMACS CNF formula (default: formula.cnf)"
    )
    parser.add_argument(
        "-s",
        "--solver",
        default="glucose-syrup",
        type=str,
        help="The SAT solver to be used (default: glucose-syrup)"
    )
    parser.add_argument(
        "-v",
        "--verb",
        default=1,
        type=int,
        choices=range(0, 2),
        help="Verbosity of the SAT solver"
    )
    args = parser.parse_args()

    grid = load_instance(args.input)

    cnf, nr_vars = encode(grid)
    
    result = call_solver(cnf, nr_vars, args.output, args.solver, args.verb)

    print_result(result, grid)
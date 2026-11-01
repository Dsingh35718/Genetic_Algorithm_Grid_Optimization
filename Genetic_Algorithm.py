"""Name - Darshdeep Singh CS 4400 Homework 3 - Genetic Algorithm """

import argparse
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROBLEMS = [(5, 4), (13, 7), (35, 37), (100, 75), (730, 490)]


def total_cost(values, rows, cols):
    """Sum absolute differences for each horizontal/vertical edge once."""
    total = 0
    for r in range(rows):
        start = r * cols
        for c in range(cols):
            i = start + c
            if c + 1 < cols:
                total += abs(values[i] - values[i + 1])
            if r + 1 < rows:
                total += abs(values[i] - values[i + cols])
    return total


def crossover_order(parent_a, parent_b, rng):
    """Order crossover (OX): children remain legal permutations."""
    size = len(parent_a)
    left, right = sorted(rng.sample(range(size), 2))
    child = [None] * size
    child[left:right + 1] = parent_a[left:right + 1]
    used = set(parent_a[left:right + 1])
    remaining = (gene for gene in parent_b if gene not in used)
    for index in list(range(right + 1, size)) + list(range(left)):
        child[index] = next(remaining)
    return child


def mutate(genes, rng, probability=0.8):
    """Swap or reverse a short segment without losing/duplicating genes."""
    if len(genes) < 2 or rng.random() >= probability:
        return
    a, b = sorted(rng.sample(range(len(genes)), 2))
    if rng.random() < 0.70:
        genes[a], genes[b] = genes[b], genes[a]
    else:
        genes[a:b + 1] = reversed(genes[a:b + 1])


def tournament(scored, rng, count=3):
    """Select the best member of a random tournament (minimization)."""
    return min(rng.sample(scored, min(count, len(scored))), key=lambda item: item[0])[1]


def evolve(population, fitness, rng, generations, elite_count=2):
    """Standard GA loop: fitness, tournament selection, OX, mutation, elitism."""
    population_size = len(population)
    best_score = None
    best_genes = None
    for _ in range(generations):
        ranked = sorted(((fitness(genes), genes) for genes in population),
                        key=lambda item: item[0])
        if best_score is None or ranked[0][0] < best_score:
            best_score = ranked[0][0]
            best_genes = ranked[0][1][:]
        next_population = [genes[:] for _, genes in ranked[:elite_count]]
        while len(next_population) < population_size:
            parent_a = tournament(ranked, rng)
            parent_b = tournament(ranked, rng)
            if rng.random() < 0.85:
                child = crossover_order(parent_a, parent_b, rng)
            else:
                child = parent_a[:]
            mutate(child, rng)
            next_population.append(child)
        population = next_population
    # Score the final generation as well; keep the best across ALL generations.
    for genes in population:
        score = fitness(genes)
        if score < best_score:
            best_score = score
            best_genes = genes[:]
    return best_genes, best_score


def initial_population(base, size, rng, count):
    """Keep a valid structured seed, diverse mutations, and random states."""
    population = [base[:]]
    while len(population) < count:
        candidate = base[:]
        if len(population) % 7 == 0:
            rng.shuffle(candidate)
        else:
            for _ in range(rng.randint(1, min(15, max(1, size // 4)))):
                mutate(candidate, rng, probability=1.0)
        population.append(candidate)
    return population


def full_permutation_ga(rows, cols, rng):
    """Unrestricted permutations of all numbers: suitable for up to 1,295 cells."""
    size = rows * cols
    # Two useful seed layouts and their reversals.
    row_major = list(range(1, size + 1))
    column_major = [c * rows + r + 1
                    for r in range(rows) for c in range(cols)]
    base = min((row_major, column_major),
            key=lambda board: total_cost(board, rows, cols))
    if size <= 30:
        population_size, generations = 50, 150
    elif size <= 150:
        population_size, generations = 40, 110
    else:
        population_size, generations = 22, 35
    population = initial_population(base, size, rng, population_size)
    population[1] = row_major
    population[2] = column_major
    return evolve(population, lambda genes: total_cost(genes, rows, cols),
                rng, generations)


def block_permutation_ga(rows, cols, rng):
    """Compact GA: permute complete numbered rows/columns for huge cases.

    For row blocks, the cost is rows*(cols-1) plus
    cols**2 * sum(abs(permutation[r] - permutation[r+1])).
    The column-block formula is symmetric. We calculate this analytical
    fitness quickly and materialize the large grid only for the winner.
    """
    row_baseline = rows * (cols - 1) + (rows - 1) * cols * cols
    col_baseline = cols * (rows - 1) + (cols - 1) * rows * rows
    use_rows = row_baseline <= col_baseline
    blocks = rows if use_rows else cols
    block_size = cols if use_rows else rows
    constant = blocks * (block_size - 1)

    def fitness(order):
        return constant + block_size * block_size * sum(
            abs(order[i] - order[i - 1]) for i in range(1, blocks))

    seed = list(range(blocks))
    population = initial_population(seed, blocks, rng, 24)
    # This is a valid GA over a restricted but scalable search space.
    order, predicted_cost = evolve(population, fitness, rng, 70)
    if use_rows:
        board = [order[r] * cols + c + 1
                for r in range(rows) for c in range(cols)]
    else:
        board = [order[c] * rows + r + 1
                for r in range(rows) for c in range(cols)]
    actual_cost = total_cost(board, rows, cols)
    if actual_cost != predicted_cost:
        raise AssertionError('Analytical GA cost disagrees with grid cost')
    return board, actual_cost


def solve(rows, cols, seed=4400):
    if rows < 1 or cols < 1:
        raise ValueError('M and N must be positive integers.')
    if rows * cols == 1:
        return [1], 0
    rng = random.Random(seed + 1009 * rows + cols)
    if rows * cols <= 1500:
        board, cost = full_permutation_ga(rows, cols, rng)
    else:
        board, cost = block_permutation_ga(rows, cols, rng)
    assert len(board) == rows * cols
    assert len(set(board)) == rows * cols
    assert min(board) == 1 and max(board) == rows * cols
    assert total_cost(board, rows, cols) == cost
    return board, cost


def matrix_lines(board, rows, cols):
    for r in range(rows):
        yield ','.join(str(value) for value in board[r * cols:(r + 1) * cols])


def save_solution(filename, board, rows, cols):
    with (ROOT / filename).open('w', encoding='utf-8', newline='\n') as stream:
        for line in matrix_lines(board, rows, cols):
            stream.write(line + '\n')


def save_costs(results):
    with (ROOT / 'solution_cost.txt').open('w', encoding='utf-8', newline='\n') as stream:
        for index in sorted(results):
            rows, cols, cost = results[index]
            stream.write(f'Problem {index}: M={rows}, N={cols}, Cost={cost}\n')


def read_problem(index):
    """Each problem_X.txt is one line containing M,N."""
    content = (ROOT / f'problem_{index}.txt').read_text(encoding='utf-8').strip()
    parts = content.replace(' ', '').split(',')
    if len(parts) != 2:
        raise ValueError(f'problem_{index}.txt must contain one line: M,N')
    return int(parts[0]), int(parts[1])


def load_costs():
    results = {}
    path = ROOT / 'solution_cost.txt'
    if not path.exists():
        return results
    pattern = re.compile(r'^Problem (\d+): M=(\d+), N=(\d+), Cost=(\d+)$')
    for line in path.read_text(encoding='utf-8').splitlines():
        match = pattern.fullmatch(line)
        if match:
            index, rows, cols, cost = map(int, match.groups())
            results[index] = (rows, cols, cost)
    return results


def run_one(index, rows, cols, results, quiet):
    board, cost = solve(rows, cols)
    save_solution(f'solution_{index}.txt', board, rows, cols)
    results[index] = (rows, cols, cost)
    save_costs(results)
    if not quiet:
        print(f'Problem {index}: M={rows}, N={cols}')
        for line in matrix_lines(board, rows, cols):
            print(line)
        print(f'Total cost: {cost}\n')
    else:
        print(f'Problem {index}: M={rows}, N={cols}, Cost={cost} (saved)')


def verify():
    """Check saved values, dimensions, uniqueness, and exact costs."""
    results = load_costs()
    success = True
    for index in range(1, 6):
        rows, cols = read_problem(index)
        path = ROOT / f'solution_{index}.txt'
        if not path.exists():
            print(f'Problem {index}: MISSING solution file')
            success = False
            continue
        lines = path.read_text(encoding='utf-8').splitlines()
        try:
            if len(lines) != rows:
                raise ValueError(f'expected {rows} rows, received {len(lines)}')
            board = []
            for line in lines:
                cells = line.split(',')
                if len(cells) != cols:
                    raise ValueError(f'expected {cols} columns in every row')
                board.extend(int(cell) for cell in cells)
            if set(board) != set(range(1, rows * cols + 1)):
                raise ValueError('values are not exactly 1..M*N once each')
            actual = total_cost(board, rows, cols)
            if results.get(index) != (rows, cols, actual):
                raise ValueError('solution_cost.txt does not match calculated cost')
            print(f'Problem {index}: PASS, {rows}x{cols}, cost={actual}')
        except ValueError as error:
            print(f'Problem {index}: FAIL, {error}')
            success = False
    return success


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('M', type=int, nargs='?', help='Number of rows')
    parser.add_argument('N', type=int, nargs='?', help='Number of columns')
    parser.add_argument('--all', action='store_true', help='Solve problem_1.txt through problem_5.txt')
    parser.add_argument('--quiet', action='store_true', help='Print summary instead of every matrix row')
    parser.add_argument('--verify', action='store_true', help='Check all saved solutions and costs')
    args = parser.parse_args()
    if args.verify:
        if not verify():
            parser.exit(1)
        return
    if args.all:
        results = {}
        for index in range(1, 6):
            rows, cols = read_problem(index)
            if (rows, cols) != PROBLEMS[index - 1]:
                parser.error(f'Problem {index} dimensions do not match the assignment')
            run_one(index, rows, cols, results, args.quiet)
    elif args.M is not None and args.N is not None:
        pair = (args.M, args.N)
        if pair not in PROBLEMS:
            parser.error('Use an assigned problem size, or --all for all five problems')
        index = PROBLEMS.index(pair) + 1
        run_one(index, args.M, args.N, load_costs(), args.quiet)
    else:
        parser.error('Provide M N (for example: 5 4), or use --all')


if __name__ == '__main__':
    main()
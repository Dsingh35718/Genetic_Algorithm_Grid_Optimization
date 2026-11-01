# Genetic Algorithm for Grid Optimization

A Python implementation of a **genetic algorithm (GA)** for arranging the integers from `1` to `M × N` in a rectangular grid while minimizing the total absolute difference between horizontally and vertically adjacent cells.

This project was developed for **CS 4400: Artificial Intelligence (Fall 2026)**. It demonstrates permutation-based evolutionary search and a scalable, restricted block-permutation approach for larger instances.

## Objective

Given an `M × N` grid containing each integer from `1` to `M × N` exactly once, minimize

\[
C(A) = \sum_{r=0}^{M-1}\sum_{c=0}^{N-2}|A_{r,c}-A_{r,c+1}|
     + \sum_{r=0}^{M-2}\sum_{c=0}^{N-1}|A_{r,c}-A_{r+1,c}|.
\]

Each horizontal and vertical neighboring pair is counted **once**. Lower scores are better.

For example, the following 5 × 4 grid has a cost of **79**:

```text
1,2,3,4
5,6,7,8
9,10,11,12
13,14,15,16
17,18,19,20
```

## How it works

The implementation in [`Genetic_Algorithm.py`](Genetic_Algorithm.py) uses:

- **Population initialization:** structured row-major and column-major candidates, mutations, and randomized candidates.
- **Fitness evaluation:** exact adjacent-difference cost from `total_cost()`.
- **Tournament selection:** selects comparatively low-cost parents.
- **Order crossover (OX):** produces valid permutations without duplicate or missing values.
- **Mutation:** swaps positions or reverses a segment.
- **Elitism:** preserves the two best candidates in each generation.
- **Best-so-far tracking:** retains the lowest-cost candidate encountered.

For grids of **1,500 cells or fewer**, `full_permutation_ga()` searches permutations of all cells. Larger grids use `block_permutation_ga()`, which evolves the ordering of whole numbered row/column blocks and evaluates an equivalent analytical cost without repeatedly materializing the full grid.

> **Limitations:** This is a heuristic. Costs are valid feasible results, not proofs of global optimality. The block-based strategy explores a deliberately restricted subset of all possible permutations.

## Requirements

- Python **3.9+**
- Only Python's standard library (`argparse`, `random`, `re`, and `pathlib`)
- macOS, Linux, or Windows 10/11

## Run the program

Open a terminal in this repository's directory.

**Run one assigned problem:**

```bash
python3 Genetic_Algorithm.py 5 4
python3 Genetic_Algorithm.py 13 7
python3 Genetic_Algorithm.py 35 37 --quiet
python3 Genetic_Algorithm.py 100 75 --quiet
python3 Genetic_Algorithm.py 730 490 --quiet
```

**Run all five assigned problems:**

```bash
python3 Genetic_Algorithm.py --all --quiet
```

**Verify saved solutions and their costs:**

```bash
python3 Genetic_Algorithm.py --verify
```

On Windows, replace `python3` with `python` or `py` if necessary. The `--quiet` flag prints a compact result instead of the entire matrix; **the full solution is still saved**.

## Files

```text
genetic-algorithm-grid-optimization/
├── Genetic_Algorithm.py   # main GA program and verification CLI
├── README.md              # GitHub project documentation
├── README.txt             # plain-text run instructions
├── problem_1.txt          # 5,4 (rows,columns)
├── problem_2.txt          # 13,7
├── problem_3.txt          # 35,37
├── problem_4.txt          # 100,75
├── problem_5.txt          # 730,490
├── solution_1.txt         # generated 5×4 matrix
├── solution_2.txt         # generated 13×7 matrix
├── solution_3.txt         # generated 35×37 matrix
├── solution_4.txt         # generated 100×75 matrix
├── solution_5.txt         # generated 730×490 matrix
├── solution_cost.txt      # recorded cost for each problem
└── .gitignore
```

The `problem_*.txt` files contain only dimensions in `M,N` format; `solution_*.txt` files contain the resulting full comma-separated matrix (M rows, N columns). This separation is intentional.

## Results

The following values are from the saved outputs included in this repository and were checked with the `--verify` command.

| Problem | Grid (M × N) | Number of cells | Total cost | Verification |
|:--|--:|--:|--:|:--|
| 1 | 5 × 4 | 20 | 79 | PASS |
| 2 | 13 × 7 | 91 | 666 | PASS |
| 3 | 35 × 37 | 1,295 | 45,358 | PASS |
| 4 | 100 × 75 | 7,500 | 564,275 | PASS |
| 5 | 730 × 490 | 357,700 | 175,389,870 | PASS |

Validation checks the matrix dimensions, confirms that the values form a permutation of `1..M×N`, recomputes the exact neighboring-difference cost, and compares that cost against `solution_cost.txt`.

## Reproducibility

The program uses a deterministic random seed (`4400`, combined with grid dimensions) when solving an assigned instance. Running it again with the same code and Python environment is intended to reproduce the included results.

## Learning outcomes

This project illustrates the design of fitness functions, permutation-safe genetic operators, exploration versus exploitation, and trade-offs between unrestricted search and scalable restricted representations.

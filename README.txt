CS 4400 - Artificial Intelligence
Homework #3: Genetic Algorithm
Fall 2026

PROJECT DESCRIPTION
This project uses a genetic algorithm to arrange the
integers from 1 to M*N in an M-by-N rectangle.

The objective is to minimize the sum of absolute
differences between horizontally and vertically
adjacent numbers.

REQUIRED SOFTWARE
Python 3
No third-party libraries required.

PROJECT FILES
Genetic_Algorithm.py - Main Python program
README.txt - Project instructions
problem_1.txt - Dimensions: 5 x 4
problem_2.txt - Dimensions: 13 x 7
problem_3.txt - Dimensions: 35 x 37
problem_4.txt - Dimensions: 100 x 75
problem_5.txt - Dimensions: 730 x 490
solution_1.txt - Solution for Problem 1
solution_2.txt - Solution for Problem 2
solution_3.txt - Solution for Problem 3
solution_4.txt - Solution for Problem 4
solution_5.txt - Solution for Problem 5
solution_cost.txt - Calculated costs

HOW TO RUN
Open Terminal in the project folder.

Run all five problems:
python3 Genetic_Algorithm.py --all

Run one problem with M rows and N columns:
python3 Genetic_Algorithm.py 5 4

Verify generated solutions:
python3 Genetic_Algorithm.py --verify

EXPECTED OUTPUT
Each solution file contains M rows and N columns.
Values are separated by commas.
Every integer from 1 to M*N appears exactly once.

The solution_cost.txt file records the total cost
for each problem.

COST FUNCTION
Cost = sum of absolute differences between
horizontally and vertically adjacent grid cells.

SUBMISSION
Submit the Python code, output text files,
PDF report, and required YouTube video link
according to the professor's instructions.

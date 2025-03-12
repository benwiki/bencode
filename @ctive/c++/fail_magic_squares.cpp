#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <numeric> // for std::iota
#include <unordered_set> // for std::unordered_set
#include <thread> // for std::this_thread::sleep_for
#include <chrono> // for std::chrono::seconds

// Function to check if the matrix is a magic square for powers up to d
bool checkMagicSquare(const std::vector<std::vector<int> > &matrix, int d) {
    int n = matrix.size();
    std::vector<long long> sums(d + 1, 0);

    // Calculate the sum of the first row for each power
    for (int p = 1; p <= d; ++p) {
        for (int j = 0; j < n; ++j) {
            sums[p] += std::pow(matrix[0][j], p);
        }
    }

    // Check rows
    for (int i = 1; i < n; ++i) {
        for (int p = 1; p <= d; ++p) {
            long long rowSum = 0;
            for (int j = 0; j < n; ++j) {
                rowSum += std::pow(matrix[i][j], p);
            }
            if (rowSum != sums[p]) return false;
        }
    }

    // Check columns
    for (int j = 0; j < n; ++j) {
        for (int p = 1; p <= d; ++p) {
            long long colSum = 0;
            for (int i = 0; i < n; ++i) {
                colSum += std::pow(matrix[i][j], p);
            }
            if (colSum != sums[p]) return false;
        }
    }

    // Check diagonals
    for (int p = 1; p <= d; ++p) {
        long long diag1Sum = 0, diag2Sum = 0;
        for (int i = 0; i < n; ++i) {
            diag1Sum += std::pow(matrix[i][i], p);
            diag2Sum += std::pow(matrix[i][n - i - 1], p);
        }
        if (diag1Sum != sums[p] || diag2Sum != sums[p]) return false;
    }

    return true;
}

// Function to check if there are repeating numbers in the elements
bool hasRepeatingNumbers(const std::vector<int>& elements) {
    std::unordered_set<int> seen;
    for (int num : elements) {
        if (seen.count(num)) return true;
        seen.insert(num);
    }
    return false;
}

// Function to print the matrix
void printMatrix(const std::vector<std::vector<int> > &matrix) {
    for (const auto &row : matrix) {
        for (int num : row) {
            std::cout << num << " ";
        }
        // std::cout << "\n";
    }
    std::cout << "\n";
}

// Function to generate the next combination of numbers with the same sum in lexicographic order
void succ(std::vector<int>& elements) {
    int n = elements.size();
    for (int i = n - 1; i > 0; --i) {
        if (elements[i] > 1) {
            elements[i]--;
            elements[i - 1]++;
            return;
        }
    }
    // If all elements are one except the first element, move on to the next sum value
    std::fill(elements.begin(), elements.end(), 1);
    elements[0]++;
}

// Function to generate matrices with diagonal enumeration and check if they are magic squares
void generateAndCheckMatrices(int n, int d) {
    std::vector<int> elements(n * n, 1);

    while (true) {
        // if (!hasRepeatingNumbers(elements)) {
            std::vector<std::vector<int> > matrix(n, std::vector<int>(n));
            for (int i = 0; i < n; ++i) {
                for (int j = 0; j < n; ++j) {
                    matrix[i][j] = elements[i * n + j];
                }
            }

            // if (checkMagicSquare(matrix, d)) {
            //     std::cout << "Magic square found:\n";
            //     printMatrix(matrix);
            //     break;
            // } else {
                // std::cout << "Trial matrix:\n";
                printMatrix(matrix);
            // }

            // Sleep for one second
            std::this_thread::sleep_for(std::chrono::seconds(1));
        // }

        // Increment the elements for the next trial using diagonal enumeration
        succ(elements);
        
    }
}

int main() {
    int n = 3, d = 2;
    generateAndCheckMatrices(n, d);
    return 0;
}

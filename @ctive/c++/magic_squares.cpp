#include <iostream>
#include <vector>
#include <thread> // for this_thread::sleep_for
#include <chrono> // for chrono::seconds
using namespace std;

// Recursive helper function.
// k             : number of positions still to fill
// sum_remaining : the remaining sum that the chosen numbers must add up to
// start         : lower bound for candidate numbers (this remains fixed so that we allow numbers out of order)
// s_max         : the maximum candidate number (here s, since no candidate can be greater than s)
// current       : the current partial tuple (built in order)
// results       : vector of complete tuples (each of which sums to s)
// used          : boolean vector (indexed from 0 to s) where used[i]==true means that i has already been chosen
void genDistinct(int k, int sum_remaining, int start, int s_max,
                 vector<int>& current, vector<vector<int>>& results, vector<bool>& used) {
    // Base case: if no positions remain, then check whether we exactly reached sum 0.
    if (k == 0) {
        if (sum_remaining == 0)
            results.push_back(current);
        return;
    }
    
    // --- Pruning ---
    // Compute a lower bound on the sum we can get from the next k available numbers.
    int needed = k;
    int minSum = 0, count = 0;
    for (int i = start; i <= s_max && count < needed; i++) {
        if (!used[i]) {
            minSum += i;
            count++;
        }
    }
    if (count < needed || minSum > sum_remaining)
        return;
    
    // Compute an upper bound on the sum from the next k available numbers.
    int maxSum = 0;
    count = 0;
    for (int i = s_max; i >= start && count < needed; i--) {
        if (!used[i]) {
            maxSum += i;
            count++;
        }
    }
    if (count < needed || maxSum < sum_remaining)
        return;
    
    // --- Recurse ---
    // Loop over all candidate numbers in the range [start, s_max] that are at most sum_remaining.
    for (int i = start; i <= s_max && i <= sum_remaining; i++) {
        if (used[i])
            continue;  // skip numbers already in the tuple
        
        // Choose i.
        used[i] = true;
        current.push_back(i);
        
        // Note: we always allow any candidate ≥ start for the subsequent positions.
        // (This lets us generate, for example, both (1,2) and (2,1) when k==2.)
        genDistinct(k - 1, sum_remaining - i, start, s_max, current, results, used);
        
        // Backtrack.
        current.pop_back();
        used[i] = false;
    }
}
 
// This is the main function that returns all k-tuples (in lexicographic order)
// with distinct numbers (each ≥ start) that sum to s.
vector<vector<int>> distinctTuplesWithSum(int k, int s, int start = 1) {
    vector<vector<int>> results;
    // If start > s, there is no candidate at all.
    if (start > s)
        return results;
    
    vector<int> current;
    // Our candidates come from start up to s.
    // We use an array "used" (of size s+1) to mark which numbers are already in the tuple.
    vector<bool> used(s + 1, false);
    
    genDistinct(k, s, start, s, current, results, used);
    return results;
}

bool checkMagicSquare(const vector<int> &matrix, int n, int d) {
    vector<long long> sums(d + 1, 0);

    // Calculate the sum of the first row for each power
    for (int p = 1; p <= d; ++p) {
        for (int j = 0; j < n; ++j) {
            sums[p] += pow(matrix[0*n+j], p);
        }
    }

    // Check rows
    for (int i = 1; i < n; ++i) {
        for (int p = 1; p <= d; ++p) {
            long long rowSum = 0;
            for (int j = 0; j < n; ++j) {
                rowSum += pow(matrix[i*n+j], p);
            }
            if (rowSum != sums[p]) return false;
        }
    }

    // Check columns
    for (int j = 0; j < n; ++j) {
        for (int p = 1; p <= d; ++p) {
            long long colSum = 0;
            for (int i = 0; i < n; ++i) {
                colSum += pow(matrix[i*n+j], p);
            }
            if (colSum != sums[p]) return false;
        }
    }

    // Check diagonals
    for (int p = 1; p <= d; ++p) {
        long long diag1Sum = 0, diag2Sum = 0;
        for (int i = 0; i < n; ++i) {
            diag1Sum += pow(matrix[i*n+i], p);
            diag2Sum += pow(matrix[i*n+n - i - 1], p);
        }
        if (diag1Sum != sums[p] || diag2Sum != sums[p]) return false;
    }

    return true;
}

int main() {
    int n = 3;
    for (int s = 45; s <= 100000; ++s) {
        auto tuples = distinctTuplesWithSum(n * n, s, 1);
        for (const auto &tuple : tuples) {
            if (checkMagicSquare(tuple, n, 2)) {
                for (int i = 0; i < tuple.size(); ++i) {
                    cout << tuple[i] << " ";
                }
                cout << "is a magic square!\n";
                return 0;
            }
        }
        cout << "No magic square found for sum " << s << "\n";
    }
}

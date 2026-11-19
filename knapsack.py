"""0/1 Knapsack using Dynamic Programming - tabulation (Unit 2)."""


def knapsack(weights, values, capacity):
    """Return (best_value, chosen_indices, dp_table).
    dp[i][w] = best value using the first i parcels with weight limit w.
    Time O(n*W), Space O(n*W)."""
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        wt, val = weights[i - 1], values[i - 1]
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]                       # skip parcel i
            if wt <= w and dp[i - 1][w - wt] + val > dp[i][w]:
                dp[i][w] = dp[i - 1][w - wt] + val        # take parcel i
    # backtrack to find which parcels were taken
    chosen, w = [], capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            chosen.append(i - 1)
            w -= weights[i - 1]
    chosen.reverse()
    return dp[n][capacity], chosen, dp

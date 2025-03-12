def tuples_with_sum(k, s, start=1):
    """
    A generator that yields all k-tuples of positive integers that sum to s.
    They are yielded in lexicographic order.
    """
    # if k == 1:
    #     yield (s,)
    # else:
    #     # The first element can be 1, 2, ..., up to s-k+1 (so that the remaining k-1 entries are at least 1)
    #     for i in range(min_val, s - k + 2):
    #         for rest in tuples_with_sum(k - 1, s - i):
    #             yield (i,) + rest
    if k == 1:
        if s >= start:
            yield (s,)
        return
    
    # The first element i can range from 'start' up to s - (k-1)*start.
    # Why? Because the remaining k-1 entries must contribute at least (k-1)*start.
    for i in range(start, s - (k - 1) * start + 1):
        # For each possible value i for the first element, generate all (k-1)-tuples
        # that sum to s-i, with each entry at least start.
        for rest in tuples_with_sum(k - 1, s - i, start):
            yield (i,) + rest

# Example usage:
if __name__ == "__main__":
    for s in range(5):
        for t in tuples_with_sum(3, s, 0):
            print(s, t)

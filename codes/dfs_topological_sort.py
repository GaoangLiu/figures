import os
import sys

def dfs_topological_sort(arr, n):
    """ Topological sort with DFS. Return an empty list if
    there is a cycle.
    """
    graph = [[] for _ in range(n)]
    for u, v in arr:
        graph[u].append(v)

    visited, stack = [0] * n, []

    def dfs(u):
        if visited[u] == -1:
            return False
        if visited[u] == 1:
            return True

        visited[u] = -1
        for v in graph[u]:
            if not dfs(v):
                return -1
        stack.append(u)
        visited[u] = 1
        return True

    for u in range(n):
        if not dfs(u):
            return []
    return stack[::-1]


arr = [[0, 3], [1, 2], [2, 3], [3, 4], [2, 4], [2, 5], [3, 5], [1, 3], [4, 5]]
s = dfs_topological_sort(arr, 6)
print(s)

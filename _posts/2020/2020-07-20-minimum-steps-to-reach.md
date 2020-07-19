---
layout: post
title: Minimum steps to reach
categories: [blog, algorithm]
tags: [dailycodingproblem]
---

+ toc
{:toc}

### Problem

This problem was asked by Google.

You are given an M by N matrix consisting of booleans that represents a board.
Each True boolean represents a wall. Each False boolean represents a tile you can walk on.

Given this matrix, a start coordinate, and an end coordinate, return the minimum number of
steps required to reach the end coordinate from the start. If there is no possible path,
then return null. You can move up, left, down, and right. You cannot move through walls.
You cannot wrap around the edges of the board.

For example, given the following board:

```cpp

[[f, f, f, f],
[t, t, f, t],
[f, f, f, f],
[f, f, f, f]]
```

and `start` = (3, 0) (bottom left) and `end` = (0, 0) (top left), the minimum number of steps
required to reach the end is `7`, since we would need to go through (1, 2) because there is a
wall everywhere else on the second row.

### Solution

+ Use Dijstra's method: we reach some target each round
  + TODO: add reference and formula here
+ If no path found, `-1` will be returned
+ If there is weight on each path, will be more interesting

```cpp
#include <iostream>
#include <vector>
#include <set>

using namespace std;

typedef pair<int, int> Pos;


int minimum_steps(const vector<vector<bool>>& m, pair<int, int> s, pair<int, int> e) {

    int row = m.size();
    int col = m[0].size();
    vector<vector<int>> distance(row, vector<int>(col, -1));
    distance[s.first][s.second] = 0;
    vector<Pos> st;
    vector<Pos> next_st;
    int step = 1;
    st.push_back(s);
    int limit = row * col;
    while (distance[e.first][e.second] == -1 && step < limit) {

        while (!st.empty()) {
            auto b = st.back(); st.pop_back();

            // right
            Pos p  = make_pair(b.first, b.second+1);
            if (p.second < col && !m[p.first][p.second]) {
                if (distance[p.first][p.second] == -1) {
                    distance[p.first][p.second] = step;
                    next_st.push_back(p);
                }
            }

            // left
            p  = make_pair(b.first, b.second-1);
            if (p.second >= 0 && !m[p.first][p.second]) {
                if (distance[p.first][p.second] == -1) {
                    distance[p.first][p.second] = step;
                    next_st.push_back(p);
                }
            }


            // top
            p  = make_pair(b.first-1, b.second);
            if (p.first >= 0 && !m[p.first][p.second]) {
                if (distance[p.first][p.second] == -1) {
                    distance[p.first][p.second] = step;
                    next_st.push_back(p);
                }
            }

            // bottom
            p  = make_pair(b.first+1, b.second);
            if (p.first < row && !m[p.first][p.second]) {
                if (distance[p.first][p.second] == -1) {
                    distance[p.first][p.second] = step;
                    next_st.push_back(p);
                }
            }
        }
        st.swap(next_st);
        ++step;
    }

    return distance[e.first][e.second];
}

int main() {
    vector<vector<bool>> m{
        {false, false, false, false},
        {true, true, false, true},
        {false, false, false, false},
        {false, false, false, false}
    };
    cout << minimum_steps(m, {3 ,0}, {0, 0}) << endl;
    return 0;
}

```

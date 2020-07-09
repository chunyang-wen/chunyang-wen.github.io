---
layout: post
title: Job scheduler
categories: [blog, algorithm]
tags: [dailycodingproblem, apple]
---

+ toc
{:toc}

### Problem

This problem was asked by Apple.

Implement a job scheduler which takes in a function f and an integer n,
and calls f after n milliseconds.

### Solution

We use a queue to track current jobs. After calling `JobScheduler::run`, jobs are
popped out by their delay. A new thread is created for each job.

+ Use a thread pool

```cpp
#include <iostream>
#include <chrono>
#include <functional>
#include <thread>
#include <queue>
#include <utility>
#include <vector>

using namespace std;

typedef std::function<void()> Func;
typedef std::pair<int, Func> Job;

struct JobCmp {
    bool operator()(const Job& l, const Job& r) {
        return l.first > r.first;
    }
};

class JobScheduler {
public:

    JobScheduler();

    void add(Func f, int delay /* in millionseconds */);

    void run();

private:
    std::priority_queue<Job, std::vector<Job>, JobCmp> _queue;

};

void JobScheduler::add(Func f, int delay) {
    _queue.push(std::make_pair(delay, f));
}

void JobScheduler::run() {

    int now = 0;
    vector<std::thread> tasks;
    while (!_queue.empty()) {
        auto job = _queue.top();
        if (now < job.first) {
            auto diff = job.first - now;
            std::cout << "sleep for: " << diff << "milliseconds" << std::endl;
            std::this_thread::sleep_for(std::chrono::milliseconds(diff));
        }
        now = job.first;
        auto t = std::thread(job.second);
        tasks.push_back(std::move(t));
        _queue.pop();
    }

    for (auto &t : tasks) {
        t.join();
    }

}

int main() {

    std::function<void()> f1 = []() {
        std::cout << "hello world" << std::endl;
    };
    std::function<void()> f2 = []() {
        std::cout << "hi world" << std::endl;
    };
    auto sched = JobScheduler();
    sched.add(f2, 100);
    sched.add(f1, 10);
    sched.run();
    return 0;
}
```

### Reference

+ [Python sched](https://github.com/python/cpython/blob/master/Lib/sched.py)

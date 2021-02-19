---
layout: post
title: Estimate PI
categories: [blog, algorithm]
tags: [dailycodingproblem, google]
include_math: True
hidden: true
---

+ toc
{:toc}

### Problem

This problem was asked by Google.

The area of a circle is defined as $\pi r^{2}$ . Estimate $\pi$ to 3 decimal places using a
Monte Carlo method.

Hint: The basic equation of a circle is $x^{2}+y^{2}=r^{2}$ .

### Solution


<img src="/images/dcp/estimator-pi.jpg" width="50%" height="50%" align="center">

We generate enough points in the up right of the rectangle. The probability is
$\dfrac {\pi }{4}$ .

```cpp
#include <iostream>
#include <iomanip>
#include <cstdlib>
#include <ctime>

using namespace std;

bool in_circle(double x, double y) {
    return x*x + y*y <= 1;
}

double estimator_pi() {
    const int COUNT = 3000000;
    int number = 0;
    srand(time(NULL));
    for (int i = 0; i < COUNT; ++i) {
        double x = rand()*1.0 / RAND_MAX;
        double y = rand()*1.0 / RAND_MAX;
        number += in_circle(x, y);
    }
    return 4.0 * number / COUNT;
}

int main() {


    cout << setprecision(4) << "PI = " << estimator_pi() << endl;
    return EXIT_SUCCESS;
}
```


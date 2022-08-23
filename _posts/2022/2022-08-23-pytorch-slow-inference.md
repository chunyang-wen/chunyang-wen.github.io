---
layout: post
title: PyTorch slow inference
categories: [blog, python]
tags: [python]
---

Our online systems support pytorch inference. It is very slow recently.
Previously there were not so many jobs running, so the CPU usage was low,
but the inference procedure finished quickly.

+ toc
{:toc}


## Background

There are two kinds of physical nodes in our cluster. They have different CPUs
and difference kinds of Os and container runtime.

+ Ubuntu 20.04.2 v.s. 20.04.3
+ Docker version: 20.10.8 v.s. 20.10.12

All pods in nodes (Ubuntu 20.04.3 and 20.10.12) run slowly when inference.

## First guess

### OS/runtime inconsistency

Bad luck! Our first guess actually took us a long time. We thought that it should
be the difference in the two nodes' configuration. Upgrading the system and docker
runtime is not possible currently.

+ Detail review of the release information about docker runtime
+ Searches about the os version and its related issues with docker

After several searches, we found
[Processes are running slow in docker container on ubuntu 18.04](https://github.com/docker/for-linux/issues/738)

It seems that some security related feature has bad impact on the performance. Tests
have been conducted on two machines, the results are similar.

### Resource request and limit

We checked the yaml files of the pods and found that there are no limit to the
resource of the pod. The pods may use more resource than requested and the speed
may be impacted according to the cpu usage of the corresponding node.

After adding the limit, code ran even slower. Oops!

### Run other code

We wrote a PI calculation code to test the performance. The speeds are similar. Oops!

## Second guess

So it seems that the root cause hides in our own code.
We divided the inference into two parts:

+ Feature generation
+ Forward calculation

The speeds of feature generation are similar. So the true difference lies in the
forward calculation.

I have no idea what happens here. Instead of searching for issues that cause
bad performance, We search how to improve the performance when using CPU. We
can set the cpu torch can use when inference. It can be set using environment
variables or using code
+ `OMP_NUM_THREADS` or `MKL_NUM_THREADS`
+ `torch.set_num_threads(num)`

After using `torch.get_num_threads()` to get current threads available to torch,
we found that torch can see a lot more CPU cores than requested. It is weird.

We add an environment variable `OMP_NUM_THREADS` in the pod's yaml and run the
code again.

The speed becomes normal.

### Test

```python
import time

import numpy as np
import torch

INDEX = 10000
NELE = 1000
a = torch.rand(INDEX, NELE)
index = np.random.randint(INDEX-1, size=INDEX*8)
b = torch.from_numpy(index)

start = time.time()
for _ in range(10):
    res = a.index_select(0, b)
print(
    "the number of cpu threads: {}, time: {}".format(torch.get_num_threads(), time.time()-start)
)
```

Save previous code into a file named `test.py`. We can execute code using bash:

```bash
OMP_NUM_THREADS=1 python test.py

# Create the container to run the code
docker run --rm -ti --cpus=4 --entrypoint bash IMAGE
```

We run the code in a docker environment and limit the CPU the container can use.
It is interesting that if we set `OMP_NUM_THREADS` to a number that is larger than
the number of cores we have, the speed drops.

```bash
the number of cpu threads: 4, time: 0.7660698890686035
the number of cpu threads: 48, time: 3.9600183963775635
```

## Final thought

+ If we can not find the answer in the forward direction, try the backward one.
+ Programs in a docker environment should not see the resource of the physical node.
+ We should collect enough information about each step before diving into the details.

## Reference

+ [Processes are running slow in docker container on ubuntu 18.04](https://github.com/docker/for-linux/issues/738)
+ [GROKKING PYTORCH INTEL CPU PERFORMANCE FROM FIRST PRINCIPLES](https://pytorch.org/tutorials/intermediate/torchserve_with_ipex.html)
+ [Set the Number of Threads to Use in PyTorch](https://jdhao.github.io/2020/07/06/pytorch_set_num_threads/)


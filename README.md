GIL Demo
--------

Quick little demonstration of the global interpreter lock in python.

Use `make` to run the demo.


In python, the global interpreter lock (GIL) restricts a python to only be
interpreted by a single thread at a time. Therefore when `app.py` creates a
thread pool of 4 threads to complete `python_work` 20 times still completes in
~14 secs (20 times the duration of a single run through `python_work`).

```python
# as defined in python_work.py, takes about ~0.7 sec.
def python_work() -> int:
    x = 0
    for _ in range(10_000_000):
        x += 1
    return x
```

The interesting thing is that from the output, the time for a thread to complete
is ~2.8 sec instead of ~0.7 sec. The reason for this is that each thread will share
the execution process roughly receiving the GIL 25% of the time which increases
the time of completion by a factor of 4.

```
# snapshot of the python output
Doing python work using threads!
python_work finished in 2.698422356
future.result()=10000000
python_work finished in 2.903675378
future.result()=10000000
python_work finished in 2.914717786
python_work finished in 2.92771538
future.result()=10000000
future.result()=10000000
```

Considering all this, python may not be single threaded (as clearly multiple
threads are running in the python example) but it is limited to a single thread
executing a given time due to the GIL.

To demonstrate releasing the GIL, one can define a similar "do work" function
in C++, as shown below.

```c++
# as defined in cpp_work.cpp, takes about ~0.2 sec.
unsigned long long cpp_work()
{
    auto rslt = 0U;
    for (auto i = 0U; i < 10000000; ++i)
        rslt++;
    return rslt;
}
```

Leveraging pybind11, it's extremely easy to expose the above function as a
python module with the GIL released:

```c++
    m.def("cpp_work", &cpp_work, pybind11::call_guard<pybind11::gil_scoped_release>(),
          "A function that does some work");
```

Finally, we can run the same experiment this time with `cpp_work` and see that
each thread finishes `cpp_work` in roughly ~0.02 sec, same as before. But more
importantly the entire execution finishes in ~0.1 sec (5 times due to running
20 times on 4 threads).

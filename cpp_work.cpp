#include <pybind11/pybind11.h>

unsigned long long cpp_work()
{
    auto rslt = 0U;
    for (auto i = 0U; i < 10000000; ++i)
        rslt++;
    return rslt;
}

PYBIND11_MODULE(cpp_work, m)
{
    m.doc() = "Do some cpp_work";
    m.def("cpp_work", &cpp_work, pybind11::call_guard<pybind11::gil_scoped_release>(),
          "A function that does some work");
}

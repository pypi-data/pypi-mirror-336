
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

extern "C" void sort_array(double *arr, int size);

namespace py = pybind11;

py::array_t<double> py_sort(py::array_t<double> input)
{
    auto buf = input.request();
    double *ptr = static_cast<double *>(buf.ptr);
    sort_array(ptr, buf.size);
    return input;
}

PYBIND11_MODULE(sortlib_cpp, m)
{
    m.def("sort", &py_sort, "Sort an array in-place");
}
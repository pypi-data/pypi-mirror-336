
#include <algorithm>

extern "C" void sort_array(double *arr, int size);

void sort_array(double *arr, int size)
{
    std::sort(arr, arr + size);
}
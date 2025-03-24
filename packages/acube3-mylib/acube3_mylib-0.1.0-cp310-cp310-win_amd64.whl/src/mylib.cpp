#include <pybind11/pybind11.h>

namespace py = pybind11;

class MyLib {
public:
    void do_work() {
        printf("Doing work, counter = %d\\n", counter_);
        counter_++;
    }

    int get_counter() const {
        return counter_;
    }

    void reset_counter() {
        counter_ = 0;
    }

private:
    int counter_ = 0;
};

PYBIND11_MODULE(mylib, m) {
    py::class_<MyLib>(m, "MyLib")
        .def(py::init<>())
        .def("do_work", &MyLib::do_work)
        .def("get_counter", &MyLib::get_counter)
        .def("reset_counter", &MyLib::reset_counter);
}

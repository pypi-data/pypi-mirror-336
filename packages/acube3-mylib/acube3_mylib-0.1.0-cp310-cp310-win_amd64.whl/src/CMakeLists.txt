pybind11_add_module(mylib MODULE
    mylib.cpp
)

set_target_properties(mylib PROPERTIES PREFIX "")

add_executable(test_mylib test.cpp)

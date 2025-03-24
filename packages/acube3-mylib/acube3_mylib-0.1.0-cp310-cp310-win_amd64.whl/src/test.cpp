#include <iostream>

class MyLib {
public:
    void do_work() {
        std::cout << "Doing work, counter = " << counter_ << std::endl;
        counter_++;
    }

    int get_counter() const { return counter_; }

    void reset_counter() { counter_ = 0; }

private:
    int counter_ = 0;
};

int main() {
    MyLib lib;
    lib.do_work();
    std::cout << "Counter after work: " << lib.get_counter() << std::endl;
    lib.reset_counter();
    std::cout << "Counter after reset: " << lib.get_counter() << std::endl;
    return 0;
}

/**
 * @brief test to use function pointer
 */
#include <iostream>
#include <vector>

void func_ptr(void (*func)(int, int), int data1, int data2);
void print_plus(int a, int b);
void print_minus(int a, int b);
void print_times(int a, int b);
void print_divide(int a, int b);

int main(int argc, char **argv)
{
    typedef std::vector<void (*)(int, int)> container;
    container vec;
    vec.push_back(print_plus);
    vec.push_back(print_minus);
    vec.push_back(print_times);
    vec.push_back(print_divide);
    for (container::iterator i = vec.begin(), e = vec.end(); i < e; i++)
        func_ptr(*i, 100, 20);
    return 0;
}

/**
 * @param func is a function name whose arguments are two.
               Here are four examples.
               - print_plus.
               - print_minus.
               - print_times.
               - print_divide.
 * @param data1 is a operand calculated in `func`.
 * @param data2 is also a operand calculated in `func`.
 */
void func_ptr(void (*func)(int, int), int data1, int data2)
{
    func(data1, data2);
}

void print_plus(int a, int b)
{
    std::cout << a << " + " << b << " = " << a+b << std::endl;
}
void print_minus(int a, int b)
{
    std::cout << a << " - " << b << " = " << a-b << std::endl;
}
void print_times(int a, int b)
{
    std::cout << a << " * " << b << " = " << a*b << std::endl;
}
void print_divide(int a, int b)
{
    std::cout << a << " / " << b << " = " << a/b << std::endl;
}


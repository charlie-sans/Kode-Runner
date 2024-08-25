#include <iostream>
#include <stdio.h>
long long factorial(long long n);

int main() 

{

    puts("Hi");
    std::cout << "hello" << std::endl;
    std::cout << factorial(5) << std::endl;
    std::cout << factorial(50) << std::endl;
    return 0;
}


long long factorial(long long n) 

{
    return (n == 1) ? 1 : n*factorial(n-1);

}

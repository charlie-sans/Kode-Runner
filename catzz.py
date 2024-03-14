import subprocess
from lib.resonite import wnr, write, rn
code = r"""
#include <iostream>
using namespace std;
int main()
{
int a = 1; 
int b = 9;
cout << a+b;
return 0;
}

"""

write(code,"temp.cpp")
subprocess.call("g++ temp.cpp -o temp", shell=True)
rn("./temp")
#include <stdio.h>
void helloworld(int a)
{
    printf("Hello world.%d\n", a);
}
void helloworld(char c)
{
    printf("Hello world.%c\n", c);
}
#ifndef SHARED_FAIL
void helloworld(double c)
{
    printf("Hello world.%f\n", c);
}
#endif


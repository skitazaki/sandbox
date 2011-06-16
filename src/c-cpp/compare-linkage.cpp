#include "helloworld.h"
int main(int argc, char* argv[])
{
    int    i = 65;
    char   c = 65;
#ifdef SHARED_FAIL
    double d = 1.0;
#endif

    helloworld(i);
    helloworld(c);
#ifdef SHARED_FAIL
    helloworld(d);
#endif

    return 0;
}

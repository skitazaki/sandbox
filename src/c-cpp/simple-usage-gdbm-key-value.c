/**
 * A sample program which uses `gdbm`.
 * you must have ``gdbm.h`` on your system.
 *
 * try this if you use Ubuntu:
 *
 *     $ sudo apt-get install libgdbm-dev
 *
 * and, compile and run:
 *
 *     $ gcc -O3 -lgdbm -o gdbm_test d65.c
 *     $ ./gdbm_test
 *
 * try this if you use MacOSX:
 *
 *     $ sudo port install gdbm
 *
 * and, compile and run:
 *
 *     $ gcc -O3 -I/opt/local/include -L/opt/local/lib -lgdbm -o gdbm_test d65.c
 *     $ ./gdbm_test
 */
#include <stdio.h>
#include <string.h>   // for strlen()
#include <gdbm.h>
#include <sys/stat.h> // for permission bits

#define BLOCK_SIZE 1024

int main(int argc, char* argv[])
{
    char* fname = "gdbm_test.gdb";
    datum key, value, ret;

    key.dptr    = "Hello";
    key.dsize   = strlen(key.dptr);
    value.dptr  = "world";
    value.dsize = strlen(value.dptr);

    GDBM_FILE dbf = gdbm_open(fname, BLOCK_SIZE, GDBM_WRCREAT, S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH, NULL);
    if (!dbf) {
        printf("could not open database file (%s).", fname);
        return 1;
    }
    if (gdbm_store(dbf, key, value, GDBM_INSERT) < 0) {
        printf("error: key=%s, value=%s\n", key.dptr, value.dptr);
        gdbm_close(dbf);
        return 1;
    }
    printf("store: key=%s, value=%s\n", key.dptr, value.dptr);
    if (gdbm_exists(dbf, key)) {
        printf("found: key=%s\n", key.dptr);
    } else {
        printf("not found: key=%s\n", key.dptr);
    }
    ret = gdbm_fetch(dbf, key);
    if (ret.dptr == NULL) {
        printf("not found: key=%s\n", key.dptr);
        gdbm_close(dbf);
        return 1;
    }
    printf("found: key=%s, value=%s\n", key.dptr, ret.dptr);

    gdbm_close(dbf);
    return 0;
}


/**
 * create posix thread which not join, and raise memory leak.
 *
 * @see `POSIX スレッド・プログラミングでのメモリー・リークを防ぐ
 *  <http://www.ibm.com/developerworks/jp/linux/library/l-memory-leaks/>`_
 */

#include<stdio.h>
#include<pthread.h>

void run() {
   pthread_exit(0);
}

int main () {
   pthread_t thread;
   int rc;
   long count = 0;
   while (1) {
      if (rc = pthread_create(&thread, 0, run, 0)) {
         printf("ERROR, rc is %d, so far %ld threads created\n", rc, count);
         perror("Fail:");
         return 1;
      }
      count++;
   }
   return 0;
}


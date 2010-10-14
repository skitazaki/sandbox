/**
 * simple www client.
 *
 * compile and run:
 * $ gcc -O3 -o wwwclient d69.c
 * $ ./wwwclient google.com 80
 */

#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <strings.h>
#include <sys/socket.h>
#include <sys/types.h>

#define DATA "GET /index.html HTTP1.0 \r\n\r\n"

int main(int argc, char *argv[])
{
    int sock, rval;
    struct sockaddr_in server;
    struct hostent *hp, *gethostbyname();
    char buf[1024];

    if (argc != 3) {
        printf("usage: %s {hostname} {port}", argv[0]);
        return 1;
    }

    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        perror("opening stream socket");
        return 1;
    }

    server.sin_family = AF_INET;
    hp = gethostbyname(argv[1]);
    if (hp == 0) {
        fprintf(stderr, "%s: unknown host\n", argv[1]);
        return 2;
    }
    bcopy(hp->h_addr, &server.sin_addr, hp->h_length);
    server.sin_port = htons(atoi(argv[2]));

    if (connect(sock, (struct sockaddr *)&server, sizeof(server)) < 0) {
        perror("connecting stream socket");
        return 1;
    }

    if (write(sock, DATA, sizeof(DATA)) < 0)
        perror("writing on stream socket");

    do {
        bzero(buf, sizeof(buf));
        rval = read(sock,buf,1023);
        if (rval != 0)
            printf("%s",buf);
    } while (rval != 0);

    close(sock);
}


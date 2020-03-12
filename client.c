#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

#define FIB_DEV "/dev/fibonacci"

int main(int argc, char **argv)
{
    if (argc != 2) {
        printf("Usage: %s <num_method>\n", argv[0]);
        exit(1);
    }

    long long sz;

    char buf[1];
    /* TODO: try test something bigger than the limit */
    int offset = 92, choice = atoi(argv[1]);

    int fd = open(FIB_DEV, O_RDWR);
    if (fd < 0) {
        perror("Failed to open character device");
        exit(1);
    }

    sz = write(fd, "", choice);
    printf("Writing to " FIB_DEV " with choice %d, returned the method %lld.\n",
           choice, sz);

    for (int i = 0; i <= offset; i++) {
        lseek(fd, i, SEEK_SET);
        sz = read(fd, buf, 1);
        printf("Reading from " FIB_DEV
               " at offset %d, returned the sequence "
               "%lld.\n",
               i, sz);
    }

    close(fd);
    return 0;
}

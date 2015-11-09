#include "stdio.h"
#include "stdlib.h"
#include "unistd.h"
#include "mqueue.h"
#include "fcntl.h"
#include "sys/mman.h"
#include "string.h"
long (*f)(void);
int main(void)
{
	int fd;
	long *dstptr=NULL;
	printf("this is shm be call\n");
	fd=shm_open("/shmdxw2",O_RDWR,0666);
        if(fd==-1)
        printf("open mq error\n");
	printf("open ok\n");
        ftruncate(fd,sizeof(f));
	dstptr=(long *)mmap(NULL,sizeof(f),PROT_READ|PROT_WRITE,MAP_SHARED,fd,0);
	printf("mmap ok\n");
	f=(long *)*dstptr;
	printf("be call f=%p\n",f);
	f();
	printf("shm f is called\n");
	return 0;
}

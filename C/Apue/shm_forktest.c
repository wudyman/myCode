#include "stdio.h"
#include "stdlib.h"
#include "unistd.h"
#include "mqueue.h"
#include "fcntl.h"
#include "sys/mman.h"
#include "string.h"
long (*f)(void);
//long (*func)(void);
long testfunc(void)
{
	printf("pid:%d testfunc call\n",getpid());
	return 0;
}
int main(void)
{
char *msg="123456";
long *srcptr=NULL;
long *dstptr=NULL;
int fd;
long p=(long)&testfunc;
f=(void *)p;
//f=&testfunc;
fd=shm_open("/shmdxw2",O_CREAT|O_RDWR,0666);
if(fd==-1)
	printf("open mq error\n");
ftruncate(fd,sizeof(f));

if(fork()==0)
{
	sleep(1);
	//execl("./shm_becall",NULL);
	dstptr=(long *)mmap(NULL,sizeof(f),PROT_READ|PROT_WRITE,MAP_SHARED,fd,0);
	printf("shm receive");
	f=(long *)*dstptr;
	printf("f is %p\n",f);
	f();
	exit(0);
}
else
{
	testfunc();
	srcptr=(long *)mmap(NULL,sizeof(f),PROT_READ|PROT_WRITE,MAP_SHARED,fd,0);
	//close(fd);
	memcpy(srcptr,&p,sizeof(f));
	printf("send f=%p\n",p);
	printf("send done\n");
}
return 0;
}

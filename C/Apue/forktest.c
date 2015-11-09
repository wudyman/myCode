#include "stdio.h"
#include "stdlib.h"
#include "unistd.h"
#include "mqueue.h"
#include "fcntl.h"
void (*f)(void);
void testfunc(void)
{
	printf("pid:%d testfunc call\n",getpid());
}
int main(void)
{
char msg[10];
mqd_t mqd1=mq_open("/mqdxw1",O_CREAT|O_RDWR,0666,NULL);
f=&testfunc;
if(mqd1==-1)
	printf("open mq error\n");
if(fork()==0)
{
//	testfunc();
	f();
	execl("./becall",NULL);
//	mq_receive(mqd1,msg,8192,0);
	printf("msg=%s\n",msg);
	exit(0);
}
else
{
	testfunc();
	mq_send(mqd1,(const char *)f,sizeof(f),6);
	printf("send done\n");
}
return 0;
}

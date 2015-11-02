#include "sys/stat.h"
#include "mqueue.h"
#include "stdio.h"
#include "stdlib.h"
#define FILE_MODE S_IRWXU|S_IRWXG|S_IRWXO
int main(void)
{
	mqd_t mq1;
	pid_t pid1;
	char *msg="123";
	char buff[20];
	int flags=O_CREAT|O_RDWR|O_BLOCK;
	mq1=mq_open("/mqdxw1",flags,0600,NULL);
	printf("mq1=%d\n",mq1);
	if((pid1=fork())==0)
	{
		mq_send(mq1,msg,4,0);
		exit(0);
	}
	sleep(3);
	mq_receive(mq1,buff,4,0);
	printf("receive is %s\n",buff);
	return 0;
}		

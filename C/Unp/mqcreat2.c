#include "sys/stat.h"
#include "sys/types.h"
#include "mqueue.h"
#include "stdio.h"
#include "stdlib.h"
#include "unistd.h"
#include "fcntl.h"
#define FILE_MODE S_IRWXU|S_IRWXG|S_IRWXO
int main(void)
{
	mqd_t mq1;
	pid_t pid1;
	char *msg="123";
	char buff[20];
	int flags=O_CREAT|O_RDWR;
	mq1=mq_open("/mqdxw2",flags,0600,NULL);
	printf("mq1=%d\n",mq1);
	if((pid1=fork())==0)
	{
		//mq_send(mq1,msg,4,4);
		exit(0);
	}
	{
  struct mq_attr mqAttr;
  mq_getattr(mq1, &mqAttr);
  printf("mqAttr.mq_msgsize=%ld\n",mqAttr.mq_msgsize);
	sleep(3);
	mq_receive(mq1,buff,mqAttr.mq_msgsize,NULL);
	printf("receive is %s\n",buff);
  }
	return 0;
}		

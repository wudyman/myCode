#include "stdlib.h"
#include "stdio.h"
#include "mqueue.h"
int main(char argc,char **argv)
{
	mqd_t mqdr;
	int n;
	char buff[10];
	if(argc>1)
	{
		mqdr=mq_open(argv[1],O_RDONLY);
		if(mqdr==-1)
			printf("open error\n");
		while((n=mq_receive(mqdr,buff,5,0))<=0)
		{
		printf("wait\n");
		sleep(1);
		}
		printf("buff is %s,n=%d\n",buff,n);
		mq_close(mqdr);
	}
	return 0;
}

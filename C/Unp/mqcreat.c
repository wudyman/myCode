#include "stdio.h"
#include "stdlib.h"
#include "mqueue.h"
int main(char argc,char **argv)
{
	mqd_t mqdc;
	if(argc>1)
	{
	mqdc=mq_open(argv[1],O_CREAT|O_RDWR|O_WRONLY,0666,NULL);
	if(mqdc==-1)
		printf("open error\n");
	mq_close(mqdc);
	}
	return 0;
}

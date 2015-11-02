#include "stdlib.h"
#include "stdio.h"
#include "mqueue.h"
int main(char argc,char **argv)
{
	mqd_t mqds;
	if(argc>1)
	{
		mqds=mq_open(argv[1],O_WRONLY);
		if(mqds==-1)
			printf("open error\n");
		mq_send(mqds,"1234",5,0);
		mq_close(mqds);
	}
	return 0;
}

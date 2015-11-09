#include "stdio.h"
#include "stdlib.h"
#include "mqueue.h"
#include "unistd.h"

int main(void)
{
	char msg[10];
	mqd_t mqd2=mq_open("/mqdxw1",O_RDONLY);
						
	printf("this is be call\n");
	mq_receive(mqd2,msg,8192,0);
	printf("receive msg is %s\n",msg);
	
	return 0;
}

#include "stdio.h"
#include "stdlib.h"
#include "unistd.h"
#include "sys/types.h"
#include "sys/stat.h"
#include "fcntl.h"
#include "string.h"
int main(void)
{
	int fd;
	char *temp="123456";
	fd=creat("test9.text",S_IRWXU|S_IRWXO);
	printf("fd=%d\n",fd);
	if(fd==-1)
		printf("open file error\n");
	//write(fd,temp,strlen(temp)+1);
	return 0;
}

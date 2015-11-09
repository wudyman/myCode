#include "stdio.h"
#include "stdlib.h"
#include "unistd.h"
#include "fcntl.h"
int main(void)
{
	int fd=open("tempprint1",O_CREAT|O_RDWR,0666);
	//fd=dup(1);
	dup2(fd,1);
	printf("this is test\n");
	return 0;
}

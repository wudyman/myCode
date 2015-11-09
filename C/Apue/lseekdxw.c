#include "stdlib.h"
#include "stdio.h"
#include "unistd.h"
#include "sys/types.h"
#include "fcntl.h"
int main(void)
{
	int pos;
	char cha;
	int fd=open("tmp",O_RDWR);
	pos=lseek(fd,0,SEEK_SET);
	printf("pos=%d\n",pos);
	pos=lseek(fd,1,SEEK_SET);
	printf("pos=%d\n",pos);
	pos=lseek(fd,1,SEEK_SET);
	printf("pos=%d\n",pos);
	pos=lseek(fd,1,SEEK_CUR);
	printf("pos=%d\n",pos);
	pos=lseek(fd,1,SEEK_END);
	printf("pos=%d\n",pos); 
	write(fd,&pos,1);
	close(fd);
	return 0;
}

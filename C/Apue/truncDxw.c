#include "stdio.h"
#include "stdlib.h"
#include "unistd.h"
#include "fcntl.h"
int main(void)
{
	int fd=open("./out",O_RDWR|O_TRUNC);	
	close(fd);
}

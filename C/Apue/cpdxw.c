#include "stdio.h"
#include "fcntl.h"
#include "sys/types.h"
#include "stdlib.h"
#include "unistd.h"
#define BUFF_SIZE 10
int main(char argc,char **argv)
{
	int n,i,infile,outfile;
	FILE *fp=NULL;
	char buff[BUFF_SIZE];
	if(argc<3)
	{
		printf("usage worng\n");
		printf("usage: ./a.out arg1 arg2, like './a.out in out'\n");
		return 0;
        }
	infile=open(argv[1],O_RDONLY);
	outfile=open(argv[2],O_CREAT|O_RDWR|O_TRUNC,S_IRWXU);
	if((infile==-1)||(outfile==-1))
		printf("open error\n");
	while((n=read(infile,buff,sizeof(buff)))>0)
	{
		printf("sizeof(buf)=%d\n",sizeof(buff));	
		printf("receive data\n");
		for(i=0;i<n;i++)
			printf("0x%02x",buff[i]);
		printf("\n");
		//printf("buff=%s\n",buff);
		printf("write start\n");
		if(write(outfile,buff,n)!=n)
		printf("\nwrite error\n");
		printf("\nwrite end\n");
	}	
	return 0;
}

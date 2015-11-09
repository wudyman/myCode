#include "stdio.h"
#include "stdlib.h"
#include "unistd.h"
#define rF "readFile"
#define wF "writeFile"
#define SOD 1//size of data
#define NOD 100// number of data
#define BUFF_SIZE 1005
FILE *openFile(const char *filename,const char *mode)
{
	FILE *fp=fopen(filename,mode);
	if(fp==NULL)
	{
		printf("open file error\n");
		exit(0);
	}
	else
		printf("open file ok\n");
	return fp;
}
void copyFile(FILE *fpr,FILE *fpw)
{
	char buff[BUFF_SIZE];
	int n;
	while((n=fread(buff,SOD,NOD,fpr))>0)
		{
		printf("read %d bytes\n",n);
		fwrite(buff,SOD,n,fpw);
		}
}
void initFile(const char *filename)
{
	int n;
	char buff[BUFF_SIZE];
	for(n=0;n<BUFF_SIZE;n++)
	buff[n]=(char)n%256;
	FILE *fp=fopen(filename,"w");
	fwrite(buff,1,BUFF_SIZE,fp);
}
int main(char argc,char **argv)
{
	FILE *fpR=NULL;
	FILE *fpW=NULL;
	if(argc==1)
	initFile(rF);
	if(argc>1)
	fpR=openFile(rF,argv[1]);
	if(argc>2)
	{
	fpW=openFile(wF,argv[2]);	
	copyFile(fpR,fpW);
	}
	return 0;
}

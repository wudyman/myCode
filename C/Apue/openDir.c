#include "dirent.h"
#include "stdio.h"
#include "stdlib.h"
#include "sys/types.h"
int main(char argc ,char *argv[])
{
	DIR *dp;
	struct dirent *dir;
	if(argc<2)
		printf("open error\n");
	if((dp=opendir(argv[1]))==NULL)
		printf("open error 2\n");
	while((dir=readdir(dp))!=NULL)
		printf("%s\n",dir->d_name);
	closedir(dp);
	return 0;
}

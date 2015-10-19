#include "stdio.h"
#include "string.h"
#include "stdlib.h"
int main(void)
{
	char *src="123456",temp;
	printf("sizeof(src)=%d,sizeof(*src)=%d,strlen(src)=%d\n",sizeof(src),sizeof(*src),strlen(src));
	char *dst=malloc(strlen(src));
	strcpy(dst,src);
	strcpy(&temp,src);
	printf("dst=%s\n",dst);
	printf("temp=%s\n",&temp);
	free(dst);
	return 0;
}

#include "string.h"
#include "stdio.h"
#include "stdlib.h"
int main(void)
{
	char s1[100]="originnew";
	char *s2="new";
	char *s3="123";
	s3=strstr(s1,s2);
	strcat(s1,s2);
	printf("s1=%s,s2=%s,s3=%s\n",s1,s2,s3);
	return 0;
}

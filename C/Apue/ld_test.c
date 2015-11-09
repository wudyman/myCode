#include "stdio.h"
#include "stdlib.h"
#include "string.h"
extern void testso(void);
int main(void)
{
	char *a="123";
	char *b="456";
	testso();
	if(strcmp(a,b)!=0)
		printf("compare error\n");
	return 0;
}

#include "stdio.h"
#include "stdlib.h"
int main(void)
{
	char c;
	while((c=getc(stdin))!=EOF)
	{
		printf("get a char\n");
		if(putc(c,stdout)==EOF)
		printf("error\n");
	}
	return 0;
}

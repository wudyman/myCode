#include "stdio.h"
#include "stdlib.h"
#include "unistd.h"
void func(void)
{
	printf("this is func %d\n",getpid());
}

int main(void)
{
	int i=1;
	char *p=malloc(1);
	*p=111;
	printf("start\n");
	if(vfork()==0)
	{
 		func();
		execl("./vfork_becall",NULL);
		//while(1){
		//sleep(1);
		//i+=1;
		//*p+=1;
 		//printf("this is clild\n");
		//printf("addr of func is %p,f is %p,i=%d,*p=%d\n",func,&i,i,*p);
		//}
 		exit(0);
	}
	else
	{
		func();
		while(1){
		sleep(1);
		i+=1;
		*p+=1;
		//printf("addr of func is %p,f is %p,i=%d,*p=%d\n",func,&i,i,*p);
		printf("this is parent\n");
		}
	}
	return 0;
}

#include "stdio.h"
#include "stdlib.h"
#include <time.h>
int main(void)
{
	struct timespec tmout={0,0};
	time(&tmout.tv_sec);
	time(&tmout.tv_nsec);
	printf("tv_sec=%d,tv_nsec=%d\n",tmout.tv_sec,tmout.tv_nsec);
	sleep(1);
	time(&tmout.tv_sec);
	time(&tmout.tv_nsec);
	printf("tv_sec=%d,tv_nsec=%d\n",tmout.tv_sec,tmout.tv_nsec);
	sleep(1);
	clock_gettime(CLOCK_REALTIME,&tmout);
	printf("tv_sec=%d,tv_nsec=%d\n",tmout.tv_sec,tmout.tv_nsec);
	sleep(1);
	clock_gettime(CLOCK_REALTIME,&tmout);
	printf("tv_sec=%d,tv_nsec=%d\n",tmout.tv_sec,tmout.tv_nsec);
	return 0;
}

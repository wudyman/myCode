#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <sys/types.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <mqueue.h>
#include <semaphore.h>
#include <time.h>
#include <unistd.h>
#include <fcntl.h>
void pf_callback(union sigval v)
{
	static int number=0;
	printf("number=%d\n",number++);
}
static void sys_timer_set(timer_t t_timer,unsigned int ui4_start,unsigned int  ui4_interval)
{
	struct itimerspec ts;
	ts.it_value.tv_sec=ui4_start/1000;
	ts.it_value.tv_nsec=((ui4_start)%1000)*1000000;
	ts.it_interval.tv_sec=ui4_interval/1000;
	ts.it_interval.tv_nsec=((ui4_interval)%1000)*1000000;
	timer_settime(t_timer,0,&ts,NULL);
}

int main(void)
{
	struct sigevent se;
	memset(&se,0,sizeof(struct sigevent));
	se.sigev_notify=SIGEV_THREAD;
	se.sigev_notify_attributes=NULL;
	se.sigev_notify_function=&pf_callback;

	timer_t t_timer;
	timer_create(CLOCK_REALTIME,&se,&t_timer);
	sys_timer_set(t_timer,3000,3000);

	while(1);
	return 0;
}

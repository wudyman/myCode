#include<stdio.h>
#include<stdlib.h>
#include<mqueue.h>
#include<sys/types.h>
#include<sys/stat.h>
#include<unistd.h>
 
int main(int argc, char **argv)
{
    int c, flags;
    mqd_t mqd;
    ssize_t n;
    unsigned int prio;
    char *buff;
    struct mq_attr attr;
   
    flags = O_RDONLY;
    while((c = getopt(argc,argv, "n")) != -1)
    {
        switch(c){
            case 'n':flags |= O_NONBLOCK;
                 break;
        }
    }
 
    if(optind != argc - 1)
        perror("mqreceive error!\n");
    mqd = mq_open(argv[optind], flags);
    mq_getattr(mqd, &attr);
   
    buff = (char*)malloc(attr.mq_msgsize);
 
    n = mq_receive(mqd, buff, attr.mq_msgsize, &prio);
    printf("buff = %s, read %ld bytes, priority = %u\n",buff, (long)n, prio);
 
    exit(0);
}

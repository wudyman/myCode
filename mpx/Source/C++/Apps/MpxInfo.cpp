#include <stdio.h>
#include <stdlib.h>

#include "MpxVersion.h"


#define BANNER "MPX File Info - Version 0.0.1\n"\
               "(Mpx Version " MPX_VERSION_NAME ")\n"\
               "(c) 2002-2017 Axiomatic Systems, LLC"
 

static void
PrintUsageAndExit()
{
    fprintf(stderr, 
            BANNER 
			"\n\nusage: MpxInfo [options] <input>\n"
			"Options:\n"
			"  --verbose:		   show extended information when available\n"
			"  --format <format>:  display the information in this format.\n"
			"					   <format> is: text (default) or json\n"
			"  --show-layout:	   show sample layout\n"
			"  --show-samples:	   show sample details\n"
			"  --show-sample-data: show sample data\n"
			"  --fast:			   skip some details that are slow to compute\n");


    exit(1);
}


int main(int argc,char **argv)
{
	if(argc<2)
		PrintUsageAndExit();
	return 0;
}

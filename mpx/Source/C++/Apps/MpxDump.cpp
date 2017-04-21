#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <MpxType.h>
#include "MpxVersion.h"
#include "Mpx_FileByteStream.h"
#include "Mpx_BoxFactory.h"
#include "MpxLog.h"


#define BANNER "MPX File Dump - Version 0.0.1\n"\
               "(Mpx Version " MPX_VERSION_NAME ")\n"\
               "(c) 2002-2017 Axiomatic Systems, LLC"
 

static void
PrintUsageAndExit()
{
    fprintf(stderr, 
		BANNER 
		"\n\nusage: MpxDump [options] <input>\n"
		"options are:\n"
		"  --verbosity <n>\n"
		"	   sets the verbosity (details) level to <n> (between 0 and 3)\n"
		"  --track <track_id>[:<key>]\n"
		"	   writes the track data into a file\n"
		"	   (<mpxfilename>.<track_id>) and optionally\n"
		"	   tries to decrypt it with the key (128-bit in hex)\n"
		"	   (several --track options can be used, one for each track)\n"
		"	   Each sample is written preceded by its size encoded as a 32-bit\n"
		"	   value in big-endian byte order\n"
		"  --format <format>\n"
		"	   format to use for the output, where <format> is either \n"
		"	   'text' (default) or 'json'\n");

    exit(1);
}


int main(int argc,char **argv)
{
	int verbosity;
	int track_id;
	int format;
	Mpx_ByteStream *pInput=NULL;
	Mpx_ByteStream *pOutput=NULL;
	const char *filename=NULL;
	if(argc<2)
		PrintUsageAndExit();
	for(int i=0;i<argc;i++)
		printf("arg=%s\n",*(argv+i));

	char *arg=NULL;
	while(*++argv)
		{
		arg=*argv;
		if(0==strcmp(arg,"--verbosity"))
			verbosity=**++argv;
		else if(0==strcmp(arg,"--track"))
			track_id=**++argv;
		else if(0==strcmp(arg,"--format"))
			format=**++argv;
		else
			{
			filename=*argv;
			}
		}
	printf("filename=%s,track_id=%d,format=%d,verbosity=%d\n",filename,track_id,format,verbosity);

	MPX_Result Result=Mpx_FileByteStream::Create("stdc0",filename,Mpx_FileByteStream::STREAM_MODE_READ,pInput);
	if(MPX_SUCCESS!=Result)
		return MPX_FAILURE;

	Result=Mpx_FileByteStream::Create("stdc0",STDOUT,Mpx_FileByteStream::STREAM_MODE_WIRTE,pOutput);
	if(MPX_SUCCESS!=Result)
		return MPX_FAILURE;

    Mpx_BoxInspector *pBoxInspector =NULL;
	MpxBox *pBox=NULL;

	pBoxInspector=new Mpx_TextBoxInspector(*pOutput);
	Mpx_DefaultBoxFactory DefaultBoxFactory;
	while(MPX_SUCCESS==DefaultBoxFactory.CreateBoxFromStream(pInput,pBox))
		{
		MPX_Position Position;
		pInput->Tell(Position);
		pBox->Inspect(pBoxInspector);
		pInput->Seek(Position);
		}
}


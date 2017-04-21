#include "Mpx_FileByteStream.h"
#include "Mpx_StdCFileByteStream.h"

MPX_Result Mpx_FileByteStream::Create(const char* type,const char* filename,Mode mode, Mpx_ByteStream*& stream)
{
	if(0==strcmp("stdc0",type))
		{
		return Mpx_StdCFileByteStream::Create(filename,mode,stream);
		}
	/*
	else if(0==strcmp("stdc1",type))
		{
		return Mpx_StdC1FileByteStream::Create(const char* filename,Mode mode, Mpx_ByteStream* & stream);
		}
		*/
	else 
		{
		printf("no stand file bytestrem match\n");
		}
	return MPX_SUCCESS;
}
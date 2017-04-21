#ifndef _MPX_STDCFILEBYTESTREAM_H_
#define _MPX_STDCFILEBYTESTREAM_H_

#include "Mpx_ByteStream.h"
#include "Mpx_FileByteStream.h"


class Mpx_StdCFileByteStream: public Mpx_ByteStream
{
public:	
	static MPX_Result Create(const char* filename,Mpx_FileByteStream::Mode mode, Mpx_ByteStream* & stream);
	Mpx_StdCFileByteStream(Mpx_ByteStream* delegator,FILE *fp,MPX_LargeSize size);
	MPX_Result ReadPartial(void *buff,MPX_Size bytes_to_read,MPX_Size &bytes_actual_read);
	MPX_Result WritePartial(const void *buff,MPX_Size bytes_to_write,MPX_Size &bytes_actual_write);
	MPX_Result Seek(MPX_Position position);
	MPX_Result Tell(MPX_Position &position);
	MPX_Result GetSize(MPX_LargeSize &size);

private:
    Mpx_ByteStream* m_Delegator;
    //AP4_Cardinal    m_ReferenceCount;
    FILE*           m_File;
    MPX_Position    m_Position;
    MPX_Size   m_Size;

};
#endif

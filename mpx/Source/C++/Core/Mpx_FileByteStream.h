#ifndef _MPX_FILEBYTESTREAM_H_
#define _MPX_FILEBYTESTREAM_H_

#include "Mpx_ByteStream.h"
class Mpx_FileByteStream: public Mpx_ByteStream
{
public:
typedef enum
	{
	STREAM_MODE_READ=0,
	STREAM_MODE_WIRTE,
	STREAM_MODE_READ_WIRTE
	}Mode;

static MPX_Result Create(const char* type,const char* filename,Mode mode, Mpx_ByteStream*& stream);
};
#endif

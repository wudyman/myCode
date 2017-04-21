#ifndef _MPX_BYTESTREAM_H_
#define _MPX_BYTESTREAM_H_
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#include "MpxType.h"
#include "MpxVersion.h"
#include "Mpx_Results.h"
#include "MpxLog.h"
#include "MpxConfig.h"

class Mpx_ByteStream
{
public:
	virtual MPX_Result ReadPartial(void *buff,MPX_Size bytes_to_read,MPX_Size &bytes_actual_read)=0;
	MPX_Result Read(void* buff,MPX_Size bytes_to_read);
	MPX_Result ReadU8(MPX_U8 &value);
	MPX_Result ReadU16(MPX_U16 &value);
	MPX_Result ReadU24(MPX_U32 &value);
	MPX_Result ReadU32(MPX_U32 &value);
	MPX_Result ReadU64(MPX_U64 &value);

	virtual MPX_Result WritePartial(const void *buff,MPX_Size bytes_to_write,MPX_Size &bytes_actual_write)=0;
	MPX_Result Write(const void* buff,MPX_Size bytes_to_write);
	MPX_Result WriteU8(MPX_U8 value);
	MPX_Result WriteU16(MPX_U16 value);
	MPX_Result WriteU24(MPX_U32 value);
	MPX_Result WriteU32(MPX_U32 value);
	MPX_Result WriteU64(MPX_U64 value);
	MPX_Result WriteString(const char *buff);
	
	virtual MPX_Result Seek(MPX_Position position)=0;
	virtual MPX_Result Tell(MPX_Position &position)=0;
	virtual MPX_Result GetSize(MPX_LargeSize &size)=0;
	
	
};
#endif


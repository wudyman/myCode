#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <MpxType.h>
#include "MpxVersion.h"

class MPX_ByteStream
{
public:
	virtual MPX_Result ReadPartial(void *buff,MPX_Size BytesToRead,MPX_Size &BytesActualRead)=0;
	MPX_Result ReadU8(MPX_U8 &value);
	MPX_Result ReadU16(MPX_U16 &value);
	MPX_Result ReadU24(MPX_U32 &value);
	MPX_Result ReadU32(MPX_U32 &value);
	MPX_Result ReadU64(MPX_U64 &value);

	virtual MPX_Result WritePartial(const void *buff,MPX_Size BytesToWrite,MPX_Size &BytesActualWrite)=0;
	MPX_Result WriteU8(MPX_U8 value);
	MPX_Result WriteU16(MPX_U16 value);
	MPX_Result WriteU24(MPX_U32 value);
	MPX_Result WriteU32(MPX_U32 value);
	MPX_Result WriteU64(MPX_U64 value);

	virtual MPX_Result Seek(MPX_Position position)=0;
	virtual MPX_Result Tell(MPX_Position &position)=0;
	virtual MPX_Result GetSize(MPX_Size &size)=0;
	
	
}


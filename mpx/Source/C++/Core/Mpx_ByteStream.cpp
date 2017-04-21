#include "Mpx_ByteStream.h"
#include "MpxMisc.h"

MPX_Result Mpx_ByteStream::Read(void *buff,MPX_Size bytes_to_read)
{
	MPX_Size nbRead;
	while(bytes_to_read)
		{
		MPX_Result result=ReadPartial(buff,bytes_to_read,nbRead);
		if(MPX_SUCCESS!=result)
			return result;
		if (0==nbRead) 
			return MPX_ERROR_INTERNAL;
		assert(nbRead<=bytes_to_read);
		bytes_to_read=bytes_to_read-nbRead;
		buff=(void *)((MPX_U8 *)buff+nbRead);
		}
	return MPX_SUCCESS;
}

MPX_Result Mpx_ByteStream::ReadU8(MPX_U8& value)
{
	unsigned char buff[1];
	MPX_Result result=Read((void*)buff,1);
	if(MPX_SUCCESS==result)
		{
		value=(MPX_U8)buff[0];
		return MPX_SUCCESS;
		}
	return result;
}

MPX_Result Mpx_ByteStream::ReadU16(MPX_U16& value)
{
	unsigned char buff[2];
	MPX_Result result=Read((void*)buff,2);
	if(MPX_SUCCESS==result)
		{
		value=Mpx_Bytes2U16BE(buff);
		return MPX_SUCCESS;
		}
	return result;
}

MPX_Result Mpx_ByteStream::ReadU32(MPX_U32& value)
{
	unsigned char buff[4];
	MPX_Result result=Read((void*)buff,4);
	if(MPX_SUCCESS==result)
		{
		value=Mpx_Bytes2U32BE(buff);
		return MPX_SUCCESS;
		}
	return result;
}

MPX_Result Mpx_ByteStream::ReadU64(MPX_U64& value)
{
	unsigned char buff[8];
	MPX_Result result=Read((void*)buff,8);
	if(MPX_SUCCESS==result)
		{
		value=Mpx_Bytes2U64BE(buff);
		return MPX_SUCCESS;
		}
	return result;
}

MPX_Result Mpx_ByteStream::Write(const void* buff,MPX_Size bytes_to_write)
{
LOGENTY;
	MPX_Size nbWrite;
	while(bytes_to_write)
		{
		MPX_Result result=WritePartial(buff,bytes_to_write,nbWrite);
		if(MPX_SUCCESS!=result)
			return result;
		if (0==nbWrite) 
			return MPX_ERROR_INTERNAL;
		assert(nbWrite<=bytes_to_write);
		bytes_to_write=bytes_to_write-nbWrite;
		buff=(void *)((MPX_U8 *)buff+nbWrite);
		}
	return MPX_SUCCESS;
}
MPX_Result Mpx_ByteStream::WriteString(const char *buff)
{
LOGENTY;
	if(NULL==buff) 
		return MPX_SUCCESS;
	MPX_Size StringLength=strlen(buff);
	if (0==StringLength) 
		return MPX_SUCCESS;

	return Write((const void*)buff,StringLength);
}
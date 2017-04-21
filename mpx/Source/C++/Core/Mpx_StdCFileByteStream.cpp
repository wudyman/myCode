#include "Mpx_StdCFileByteStream.h"
MPX_Result Mpx_StdCFileByteStream::Create(const char* filename,Mpx_FileByteStream::Mode mode, Mpx_ByteStream*& stream)
{
	stream=NULL;
	if(NULL==filename)
		return MPX_ERROR_INVALID_PARAMETERS;
	FILE *fp=NULL;
	MPX_Position size=0;

	if(0==strcmp(filename,STDOUT))
		fp=stdout;
	else if(0==strcmp(filename,STDIN))
		fp=stdin;
	else if(0==strcmp(filename,STDERR))
		fp=stderr;
	else
		{
			if(mode==Mpx_FileByteStream::STREAM_MODE_READ)
				{
				fp=fopen(filename,"rb");
				if(NULL==fp)
					return MPX_ERROR_CANNOT_OPEN_FILE;
				}
			else if(mode==Mpx_FileByteStream::STREAM_MODE_WIRTE)
				{
				fp=fopen(filename,"wb+");
				if(NULL==fp)
					return MPX_ERROR_CANNOT_OPEN_FILE;
				}
			else if(mode==Mpx_FileByteStream::STREAM_MODE_READ_WIRTE)
				{
				fp=fopen(filename,"r+b");
				if(NULL==fp)
					return MPX_ERROR_CANNOT_OPEN_FILE;
				}

			    // get the size
			if (Mpx_fseek(fp, 0, SEEK_END) >= 0) 
			{
				size = Mpx_ftell(fp);
				Mpx_fseek(fp, 0, SEEK_SET);
			}
		}
	stream=new Mpx_StdCFileByteStream(NULL,fp,size);
	return MPX_SUCCESS;
}
Mpx_StdCFileByteStream::Mpx_StdCFileByteStream(Mpx_ByteStream* delegator,FILE *fp,MPX_LargeSize size):
m_File(fp),
m_Position(0),
m_Size(size)
{
}


MPX_Result Mpx_StdCFileByteStream::ReadPartial(void *buff,MPX_Size bytes_to_read,MPX_Size &bytes_actual_read)
{	
	size_t nbRead=fread(buff,1,bytes_to_read,m_File);
	if(nbRead>0)
		{
		bytes_actual_read=(MPX_Size)nbRead;
		m_Position+=nbRead;
		return MPX_SUCCESS;
		}
	else if(feof(m_File))
		{
		bytes_actual_read=0;
		return MPX_ERROR_EOS;
		}
	else
		{
		bytes_actual_read=0;
		return MPX_ERROR_READ_FAILED;
		}
}

MPX_Result Mpx_StdCFileByteStream::WritePartial(const void *buff,MPX_Size bytes_to_write,MPX_Size &bytes_actual_write)
{
LOGENTY;
	size_t nbWrite=fwrite(buff,1,bytes_to_write,m_File);
	if(nbWrite>0)
		{
		bytes_actual_write=(MPX_Size)nbWrite;
		m_Position+=nbWrite;
		return MPX_SUCCESS;
		}
	else
		{
		bytes_actual_write=0;
		return MPX_ERROR_READ_FAILED;
		}
	return MPX_SUCCESS;
}


MPX_Result Mpx_StdCFileByteStream::Seek(MPX_Position position)
{
	if(Mpx_fseek(m_File,position,SEEK_SET)>=0)
	{
	m_Position=position;
	return MPX_SUCCESS;
	}
	return MPX_FAILURE;
}
MPX_Result Mpx_StdCFileByteStream::Tell(MPX_Position &position)
{
	position=m_Position;
	return MPX_SUCCESS;
}
MPX_Result Mpx_StdCFileByteStream::GetSize(MPX_LargeSize &size)
{
	size=m_Size;
	return MPX_SUCCESS;
}

#include "Mpx_BoxFactory.h"
#include "Mpx_FtypBox.h"

MPX_Result Mpx_BoxFactory::CreateBoxFromStream(Mpx_ByteStream*& stream,MpxBox*& box)
{
LOGENTY;
	MPX_Position  Position=0;
	MPX_LargeSize LargeSize=0;
	MPX_LargeSize BytesAvailable=(MPX_LargeSize)-1;
	MPX_Result Result=stream->GetSize(LargeSize);
	if(MPX_FAILED(Result))
		return Result;
	Result=stream->Tell(Position);
	if(MPX_FAILED(Result))
		return Result;

	if((0!=LargeSize)&&(Position<=LargeSize))
		BytesAvailable=LargeSize-Position;

	return CreateBoxFromStream(stream,BytesAvailable,box);
		
}

MPX_Result Mpx_BoxFactory::CreateBoxFromStream(Mpx_ByteStream*& stream,MPX_LargeSize bytes_availabe,MpxBox*& box)
{
LOGENTY;
	box=NULL;
	MPX_U32 Size32;
	MPX_U64 Size64;
	MPX_U64 Size;
	MPX_U32 type;
	bool Force64=false;
	bool IsLargeBox=false;
	MPX_Result Result;
	if(0==bytes_availabe)
		return MPX_ERROR_EOS;

	
	MPX_Position Start;
	stream->Tell(Start);
	stream->ReadU32(Size32);
	stream->ReadU32(type);

	Size=Size32;
	LOG("Size=%lld\n",Size);
    if(0==Size32)// size expends to the end of file.
    	{
    	MPX_LargeSize TempStreamSize=0;
		stream->GetSize(TempStreamSize);
		if(TempStreamSize>=Start)
			Size=TempStreamSize-Start;
    	}
	if(1==Size32)// largesize
		{
		IsLargeBox=true;
		if(bytes_availabe<16)
			{
			stream->Seek(Start);
			LOGERRCODE("%d\n",MPX_ERROR_INVALID_FORMAT);
			return MPX_ERROR_INVALID_FORMAT;
			}
		stream->ReadU64(Size64);
		Size=Size64;
		if(Size64<0xffffffff)
			Force64=true;	
		}

	//check the size
	if((Size>0&&Size<8)||(Size>bytes_availabe))
		{
		stream->Seek(Start);
		LOGERRCODE("%d\n",MPX_ERROR_INVALID_FORMAT);
        return MPX_ERROR_INVALID_FORMAT;
		}
	    // create the atom
    Result = CreateBoxFromStream(stream, type, Size32, Size64, box);
    if (MPX_FAILED(Result))
    	{
    	LOGERRCODE("%d\n",Result);
		return Result;
    	}

	return MPX_SUCCESS;
}

MPX_Result Mpx_BoxFactory::CreateBoxFromStream(Mpx_ByteStream*& stream, MPX_U32 type, MPX_U32 size32,MPX_U64 size64, MpxBox*& box)
{
LOGENTY;
	bool bBoxIsLarge=(1==size32);
	bool bForce64=((1==size32)&&(0==(size64>>32)));
	switch(type)
		{
		case Mpx_Box_Type_Ftyp:
			LOG("find fytp box\n");
			if(bBoxIsLarge)
				return MPX_ERROR_INVALID_FORMAT;
			box=Mpx_FtypBox::Create(stream,size32);
			break;
		default:
			return MPX_ERROR_NOT_SUPPORTED;
			break;
		}
	return MPX_SUCCESS;
}
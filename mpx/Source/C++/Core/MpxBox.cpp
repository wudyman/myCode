#include "MpxBox.h"

MpxBox::MpxBox(MPX_U32 type,MPX_U32 size):
    m_Type(type),
    m_Size32(size),
    m_Size64(0),
    m_IsFullBox(false),
    m_Version(0),
    m_Flags(0)
{
}

void MpxBox::SetSize(MPX_U64 size,bool force64)
{
	if(!force64)
		{
		if((1==m_Size32)&&(size<=0xffffffff))
			force64=true;
		}
	if((!force64)&&(0==size>>32))
		{
		m_Size64=0;
		m_Size32=(MPX_U32)size;
		}
	else
		{
		m_Size32=1;
		m_Size64=size;
		}
}

MPX_Size MpxBox::GetHeaderSize()const
{
	return (m_IsFullBox? MPX_FULL_BOX_HEADER_SIZE : MPX_BOX_HEADER_SIZE)+(m_Size32==1?8:0);
}
MPX_Result MpxBox::Inspect(Mpx_BoxInspector*& inspector)
{
LOGENTY;
	InspectHeaders(inspector);
	InspectFields(inspector);
	return MPX_SUCCESS;
}

MPX_Result MpxBox::InspectHeaders(Mpx_BoxInspector*& inspector)
{
LOGENTY;
	char TypeName[5];
	Mpx_FormatFourCharsPrintable(TypeName,m_Type);
	inspector->StartBox(TypeName,m_Version,m_Flags,GetHeaderSize(),GetSize());
	return MPX_SUCCESS;
}






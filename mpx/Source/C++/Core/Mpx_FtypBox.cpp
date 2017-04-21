#include "Mpx_FtypBox.h"


Mpx_FtypBox::Mpx_FtypBox(Mpx_ByteStream*& stream,MPX_U32 size):MpxBox(Mpx_Box_Type_Ftyp,size)
{
	stream->ReadU32(m_MajorBrand);
	stream->ReadU32(m_MinorVersion);
	size-=16;
	while(size)
		{
		MPX_U32 CompatibleBrand;
		stream->ReadU32(CompatibleBrand);
		m_CompatibleBrands.push_back(CompatibleBrand);
		size-=4;
		}
}


MPX_Result Mpx_FtypBox::InspectFields(Mpx_BoxInspector*& inspector)
{
    char name[5];
    Mpx_FormatFourChars(name, m_MajorBrand);
    inspector->DescribeField("major_brand", name);
    inspector->DescribeField("minor_version", m_MinorVersion);

    // compatible brands
    vector<MPX_U32>::iterator it=m_CompatibleBrands.begin();
    for (; it!=m_CompatibleBrands.end(); it++) {
        MPX_U32 cb = *it;
        Mpx_FormatFourChars(name, cb);
        inspector->DescribeField("compatible_brand", name);
    }

	return MPX_SUCCESS;
}


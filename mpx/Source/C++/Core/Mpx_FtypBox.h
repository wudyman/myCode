#ifndef _MPX_FTYP_BOX_H_
#define _MPX_FTYP_BOX_H_

#include <vector>
#include "MpxBox.h"

class Mpx_FtypBox: public MpxBox
{
public:
	static Mpx_FtypBox* Create(Mpx_ByteStream*& stream,MPX_U32 size)
	{
		return new Mpx_FtypBox(stream,size);
	}

	
	MPX_Result InspectFields(Mpx_BoxInspector*& inspector);
private:
	Mpx_FtypBox(Mpx_ByteStream*& stream,MPX_U32 size);

    MPX_U32	m_MajorBrand;
    MPX_U32	m_MinorVersion;
	vector<MPX_U32> m_CompatibleBrands;
};
#endif

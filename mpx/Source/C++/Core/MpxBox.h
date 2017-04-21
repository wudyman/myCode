#ifndef _MPX_BOX_H_
#define _MPX_BOX_H_



#include "MpxType.h"
#include "MpxVersion.h"
#include "Mpx_Results.h"
#include "Mpx_ByteStream.h"
#include "MpxLog.h"
#include "MpxMisc.h"
#include "Mpx_BoxInspector.h"



#define MPX_BOX_TYPE(c1,c2,c3,c4) \
( \
	((MPX_U32)(c1)<<24)| \
	((MPX_U32)(c2)<<16)| \
	((MPX_U32)(c3)<<8)| \
	((MPX_U32)(c4)) \
) 

/*----------------------------------------------------------------------
|   constants
+---------------------------------------------------------------------*/
const MPX_U32 MPX_BOX_HEADER_SIZE         = 8;
const MPX_U32 MPX_BOX_HEADER_SIZE_64      = 16;
const MPX_U32 MPX_FULL_BOX_HEADER_SIZE    = 12;
const MPX_U32 MPX_FULL_BOX_HEADER_SIZE_64 = 20;
const MPX_U32 MPX_BOX_MAX_NAME_SIZE       = 256;
const MPX_U32 MPX_BOX_MAX_URI_SIZE        = 512;


const MPX_U32 Mpx_Box_Type_Ftyp=MPX_BOX_TYPE('f','t','y','p');

class MpxBox
{
public:
	MpxBox();
	MpxBox(MPX_U32 type,MPX_U32 size);
	virtual ~MpxBox(){}

	MPX_U64 GetSize() const{return m_Size32==1?m_Size64:m_Size32;}
	void    SetSize(MPX_U64 size,bool force64);
	MPX_U32 GetSize32() const{return m_Size32;}
	void    SetSize32(MPX_U32 size){m_Size32=size;}
	MPX_U32 GetSize64() const{return m_Size64;}
	void    SetSize64(MPX_U64 size){m_Size64=size;}
	MPX_U32 GetType() const{return m_Type;}
	void    SetType(MPX_U32 type){m_Type=type;}
	MPX_U8 GetVersion() const{return m_Version;}
	void    SetVersion(MPX_U8 version){m_Version=version;}
	MPX_U32 GetFlags() const{return m_Flags;}
	void    SetFlags(MPX_U32 flags){m_Flags=flags;}
	virtual MPX_Size    GetHeaderSize() const;

	virtual MPX_Result Inspect(Mpx_BoxInspector*& inspector);
	virtual MPX_Result InspectHeaders(Mpx_BoxInspector*& inspector);
	virtual MPX_Result InspectFields(Mpx_BoxInspector*& inspector){return MPX_SUCCESS;}

	
private:
	MPX_U32 m_Type;
	MPX_U32 m_Size32;
	MPX_U64 m_Size64;
	
	bool    m_IsFullBox;
	MPX_U8  m_Version;
	MPX_U32 m_Flags;
};

#endif

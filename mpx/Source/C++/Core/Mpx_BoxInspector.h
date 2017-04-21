#include "MpxType.h"
#include "MpxVersion.h"
#include "Mpx_Results.h"
#include "Mpx_ByteStream.h"

class Mpx_BoxInspector
{
public:
	virtual MPX_Result StartBox(const char* /* type name        */,
                           MPX_U8	   /* version     */,
                           MPX_U32     /* flags       */,
                           MPX_Size	   /* header_size */,
                           MPX_U64     /*size         */){return MPX_SUCCESS;}	
	virtual MPX_Result DescribeField(const char* name,const char* value){return MPX_SUCCESS;}
	virtual MPX_Result DescribeField(const char* name,MPX_U64 value){return MPX_SUCCESS;}
};

class Mpx_TextBoxInspector:public Mpx_BoxInspector
{
public:
	Mpx_TextBoxInspector(Mpx_ByteStream &stream){m_Stream=&stream;}
	MPX_Result StartBox(const char* /* type name        */,
                           MPX_U8	   /* version     */,
                           MPX_U32     /* flags       */,
                           MPX_Size	   /* header_size */,
                           MPX_U64     /*size         */);
	MPX_Result DescribeField(const char* name,const char* value);
	MPX_Result DescribeField(const char* name,MPX_U64 value);
private:
	MPX_U16 m_Indent;
	Mpx_ByteStream *m_Stream;
};
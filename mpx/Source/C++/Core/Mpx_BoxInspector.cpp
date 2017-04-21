#include "Mpx_BoxInspector.h"

/*----------------------------------------------------------------------
|   AP4_MakePrefixString
+---------------------------------------------------------------------*/
static void Mpx_MakePrefixString(unsigned int indent, char* prefix, MPX_Size size)
{
    if (size == 0) return;
    if (indent >= size-1) indent = size-1;
    for (unsigned int i=0; i<indent; i++) {
        prefix[i] = ' ';
    }
    prefix[indent] = '\0';    
}

MPX_Result Mpx_TextBoxInspector::StartBox(const char* type_name,
													MPX_U8 version,
													MPX_U32 flags,
													MPX_Size header_size,
													MPX_U64 size)
{
LOGENTY;
	char Extra[32]="";
	char Info[128]="";

	if((12==header_size)||(20==header_size)||(28==header_size))
		{
		if(version&&flags)
			Mpx_FormatString(Extra,sizeof(Extra),",version=%d,flags=%x",version,flags);
		else if(version)
			Mpx_FormatString(Extra,sizeof(Extra),",version=%d",version);
		else if(flags)
			Mpx_FormatString(Extra,sizeof(Extra),",flags=%x",flags);
		}

	Mpx_FormatString(Info,sizeof(Info),"size=%d+%lld %s",header_size,size-header_size,Extra);

	char Prefix[128];
	Mpx_MakePrefixString(m_Indent,Prefix,sizeof(Prefix));
	m_Stream->WriteString(Prefix);
	m_Stream->WriteString("[");
	m_Stream->WriteString(type_name);
    m_Stream->Write("] ", 2);
    m_Stream->WriteString(Info);
    m_Stream->Write("\n", 1);

    m_Indent += 2;

	return MPX_SUCCESS;

}

MPX_Result Mpx_TextBoxInspector::DescribeField(const char* name,const char* value)
{
	char prefix[256];
    Mpx_MakePrefixString(m_Indent, prefix, sizeof(prefix));
    m_Stream->WriteString(prefix);
    
    m_Stream->WriteString(name);
    m_Stream->WriteString(" = ");
    m_Stream->WriteString(value);
    m_Stream->Write("\n", 1);
	return MPX_SUCCESS;
}

MPX_Result Mpx_TextBoxInspector::DescribeField(const char* name,MPX_U64 value)
{
    char prefix[256];
    Mpx_MakePrefixString(m_Indent, prefix, sizeof(prefix));
    m_Stream->WriteString(prefix);

    char str[32];
    Mpx_FormatString(str, sizeof(str), "%lld", value);
    m_Stream->WriteString(name);
    m_Stream->WriteString(" = ");
    m_Stream->WriteString(str);
    m_Stream->Write("\n", 1);

	return MPX_SUCCESS;
}




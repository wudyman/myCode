#ifndef _MPX_MISC_H_
#define _MPX_MISC_H_

#include <stdio.h>
#include <stdlib.h>

#include "MpxType.h"
#include "MpxVersion.h"
#include "Mpx_Results.h"


inline MPX_U16 Mpx_Bytes2U16BE(const unsigned char* buff)
{
	MPX_U16 value;
	value=((MPX_U16)buff[0]<<8)|
		  ((MPX_U16)buff[1]);
	return value;
}

inline MPX_U32 Mpx_Bytes2U32BE(const unsigned char* buff)
{
	MPX_U32 value;
	value=((MPX_U32)buff[0]<<24)|
		  ((MPX_U32)buff[1]<<16)|
		  ((MPX_U32)buff[2]<<8)|
		  ((MPX_U32)buff[3]);
	return value;
}

inline MPX_U32 Mpx_Bytes2U64BE(const unsigned char* buff)
{
	MPX_U64 value;
	value=((MPX_U64)buff[0]<<56)|
		  ((MPX_U64)buff[1]<<48)|
		  ((MPX_U64)buff[2]<<40)|
		  ((MPX_U64)buff[3]<<32)|
		  ((MPX_U64)buff[4]<<24)|
		  ((MPX_U64)buff[5]<<16)|
		  ((MPX_U64)buff[6]<<8)|
		  ((MPX_U64)buff[7]);
	return value;
}

/*----------------------------------------------------------------------
|   AP4_FormatFourChars
+---------------------------------------------------------------------*/
void Mpx_FormatFourChars(char* str, MPX_U32 value);

/*----------------------------------------------------------------------
|   Mpx_FormatFourCharsPrintable
+---------------------------------------------------------------------*/
void Mpx_FormatFourCharsPrintable(char* str, MPX_U32 value);
#endif

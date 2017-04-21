#include "MpxMisc.h"

/*----------------------------------------------------------------------
|   AP4_FormatFourChars
+---------------------------------------------------------------------*/
void Mpx_FormatFourChars(char* str, MPX_U32 value)
{
    str[0] = (value >> 24) & 0xFF;
    str[1] = (value >> 16) & 0xFF;
    str[2] = (value >>  8) & 0xFF;
    str[3] = (value      ) & 0xFF;
    str[4] = '\0';
}


/*----------------------------------------------------------------------
|   Mpx_FormatFourCharsPrintable
+---------------------------------------------------------------------*/
void Mpx_FormatFourCharsPrintable(char* str, MPX_U32 value)
{
    Mpx_FormatFourChars(str, value);
    for (int i=0; i<4; i++) {
        if (str[i]<' ' || str[i] >= 127) {
            str[i] = '.';
        }
    }
}


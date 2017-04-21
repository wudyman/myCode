#ifndef _MPX_BOX_FACTORY_H_
#define _MPX_BOX_FACTORY_H_
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#include "MpxType.h"
#include "MpxVersion.h"
#include "Mpx_Results.h"
#include "MpxBox.h"
#include "Mpx_ByteStream.h"


class Mpx_BoxFactory
{
public:
	//Mpx_BoxFactory();
	//~Mpx_BoxFactory();

	MPX_Result CreateBoxFromStream(Mpx_ByteStream*& stream,MpxBox*& box);
	MPX_Result CreateBoxFromStream(Mpx_ByteStream*& stream,MPX_LargeSize bytes_availabe,MpxBox*& box);
	MPX_Result CreateBoxFromStream(Mpx_ByteStream*& stream, MPX_U32 type, MPX_U32 size32,MPX_U64 size64, MpxBox*& box);
private:
};

class Mpx_DefaultBoxFactory:public Mpx_BoxFactory
{
};
#endif

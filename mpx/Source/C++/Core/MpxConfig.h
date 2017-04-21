#ifndef _MPX_CONFIG_H_
#define _MPX_CONFIG_H_

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#define STDOUT   "stdout"
#define STDIN    "stdin"
#define STDERR   "stderr"



#define Mpx_fseek fseek
#define Mpx_ftell ftell
#define Mpx_FormatString snprintf
#endif

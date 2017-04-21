#ifndef _MPX_LOG_H_
#define _MPX_LOG_H_
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#define LOG_ENABLE 0

#if LOG_ENABLE
#define __BANNER 0


/*************************************************************************************
Color coding for various log levels
*************************************************************************************/
#define ICON_ERROR_ON						" \e[48;5;1m E \e[0m"
#define ICON_WARNING_ON						" \e[48;5;202m W \e[0m"
#define ICON_INFORMATION_ON					" \e[48;5;2m I \e[0m"
#define ICON_DEBUG_ON						" \e[48;5;4m D \e[0m"
#define ICON_VERBOSE_ON						" \e[48;5;235m V \e[0m"
#define ICON_EXCEPTION						" \e[48;5;1m EXCEPTION \e[0m"

#define ICON_ERROR_OFF						" \e[48;5;250m E \e[0m"
#define ICON_WARNING_OFF					" \e[48;5;250m W \e[0m"
#define ICON_INFORMATION_OFF				" \e[48;5;250m I \e[0m"
#define ICON_DEBUG_OFF						" \e[48;5;250m D \e[0m"
#define ICON_VERBOSE_OFF					" \e[48;5;250m V \e[0m"

#define FORMAT_SECONDS						"\e[48;5;208m %lu"
#define FORMAT_U_SECONDS					"\e[48;5;209m %08lu \e[0m"

#define SETTING_ON							"\e[38;5;10m ON\e[0m"
#define SETTING_OFF							"\e[38;5;9mOFF\e[0m"

#define FORMAT_TIME							FORMAT_SECONDS FORMAT_U_SECONDS


#define FORMAT_MESSAGE_ERROR_START			" \e[38;5;1m"
#define FORMAT_MESSAGE_WARN_START			" \e[38;5;202m"
#define FORMAT_MESSAGE_INFO_START			" \e[38;5;2m"
#define FORMAT_MESSAGE_DEBUG_START			" \e[38;5;4m"
#define FORMAT_MESSAGE_VERB_START			" \e[38;5;243m"

#define FORMAT_FILENAME						" \e[48;5;90m %s\e[48;5;91m %04d\e[0m"
#define FORMAT_FUNCTION						"\e[48;5;92m %s \e[0m"

#define FORMAT_PROCESS						" \e[48;5;23m %12s\e[48;5;24m %04d\e[48;5;25m %16s \e[0m"
#define FORMAT_RESET						"\e[0m\n"


#define FORMAT_START_VERBOSE				ICON_VERBOSE_ON FORMAT_FILENAME FORMAT_FUNCTION FORMAT_MESSAGE_VERB_START
#define FORMAT_START_DEBUG					ICON_DEBUG_ON FORMAT_FILENAME FORMAT_FUNCTION FORMAT_MESSAGE_DEBUG_START
#define FORMAT_START_INFORMATION			ICON_INFORMATION_ON FORMAT_FILENAME FORMAT_FUNCTION FORMAT_MESSAGE_INFO_START
#define FORMAT_START_WARNING				ICON_WARNING_ON FORMAT_FILENAME FORMAT_FUNCTION FORMAT_MESSAGE_WARN_START
#define FORMAT_START_ERROR					ICON_ERROR_ON FORMAT_FILENAME FORMAT_FUNCTION FORMAT_MESSAGE_ERROR_START
#define FORMAT_START_EXCEPTION				ICON_EXCEPTION FORMAT_FILENAME FORMAT_FUNCTION FORMAT_MESSAGE_ERROR_START



#define __verb(__verb__)					FORMAT_START_VERBOSE __verb__ FORMAT_RESET
#define __debug(__debug__)					FORMAT_START_DEBUG __debug__ FORMAT_RESET
#define __info(__info__)					FORMAT_START_INFORMATION __info__ FORMAT_RESET
#define __warn(__warn__)					FORMAT_START_WARNING __warn__ FORMAT_RESET
#define __err(__error__)					FORMAT_START_ERROR __error__ FORMAT_RESET
#define __exception(__error__)				FORMAT_START_EXCEPTION __error__ FORMAT_RESET


//#define __src()								__FILE__, __LINE__, __FUNCTION__
#define __src()								__FILE__, __LINE__, __FUNCTION__


#define __LOG(__BANNER, ...)									\
	do															\
	{															\
			fprintf(stderr,__VA_ARGS__);						\
	} while(0)



#define LOG(__format__, ...) 			do{ __LOG(BANNER,__verb(__format__),__src(),##__VA_ARGS__); }while(0)
#define LOGENTY 		LOG("ENTRY");
#define LOGERRCODE(__format__, ...)     do{ __LOG(BANNER,__verb(__format__),__src(),##__VA_ARGS__); }while(0)
#else
#define LOG(__format__, ...)
#define LOGENTY
#define LOGERRCODE(__format__, ...)
#endif

#endif

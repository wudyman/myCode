#ifndef _MPX_RESULTS_H_
#define _MPX_RESULTS_H_


/*----------------------------------------------------------------------
|   constants
+---------------------------------------------------------------------*/
const int MPX_SUCCESS                               =  0;
const int MPX_FAILURE                               = -1;
const int MPX_ERROR_OUT_OF_MEMORY                   = -2;
const int MPX_ERROR_INVALID_PARAMETERS              = -3;
const int MPX_ERROR_NO_SUCH_FILE                    = -4;
const int MPX_ERROR_PERMISSION_DENIED               = -5;
const int MPX_ERROR_CANNOT_OPEN_FILE                = -6;
const int MPX_ERROR_EOS                             = -7;
const int MPX_ERROR_WRITE_FAILED                    = -8;
const int MPX_ERROR_READ_FAILED                     = -9;
const int MPX_ERROR_INVALID_FORMAT                  = -10;
const int MPX_ERROR_NO_SUCH_ITEM                    = -11;
const int MPX_ERROR_OUT_OF_RANGE                    = -12;
const int MPX_ERROR_INTERNAL                        = -13;
const int MPX_ERROR_INVALID_STATE                   = -14;
const int MPX_ERROR_LIST_EMPTY                      = -15;
const int MPX_ERROR_LIST_OPERATION_ABORTED          = -16;
const int MPX_ERROR_INVALID_RTP_CONSTRUCTOR_TYPE    = -17;
const int MPX_ERROR_NOT_SUPPORTED                   = -18;
const int MPX_ERROR_INVALID_TRACK_TYPE              = -19;
const int MPX_ERROR_INVALID_RTP_PACKET_EXTRA_DATA   = -20;
const int MPX_ERROR_BUFFER_TOO_SMALL                = -21;
const int MPX_ERROR_NOT_ENOUGH_DATA                 = -22;
const int MPX_ERROR_NOT_ENOUGH_SPACE                = -23;


#define MPX_FAILED(result) 		(MPX_SUCCESS!=(result))
#define MPX_SUCCESSED(result)	(MPX_SUCCESS==(result))
#endif

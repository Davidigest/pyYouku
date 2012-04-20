#*******************************************************************************
# PyYouku : A python library for manipulating Youku videos
# Youku: http://Youku.com is China's equivalent of Youtube
# _______________________________
#
#  Authors : David Kou
#            Davidigest@gmail.com
# _______________________________
#
#*******************************************************************************
# History
# v0.1,  Apr. 19 2012
#




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# It is IMPORTANT to set below information before use
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
config = \
{
    'youku_pid'           :   '123456',                 # YOUKU partener ID
    'youku_user_name'     :   'YoukuUser@gmail.com',    # YOUKU user
    'youku_password'      :   'YoukuPassword',          # YOUKU user's password
    'upload_url'          :     r'http://gupload.youku.com/upload/uploadPackage'
}
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
config = \
{
    'youku_pid'           :   'XMjMzNg==',                 # YOUKU partener ID
    'youku_user_name'     :   'davidigest@gmail.com',   # YOUKU user
    'youku_password'      :   'xixihaha',               # YOUKU user's password
    'upload_url'          :    r'http://gupload.youku.com/upload/uploadPackage'
}


errorMsg = \
[
    "System Error",                                       #  0
	"File error, the size of the file is 0",              # -10
 	"File error, no data in the video file",              # -9
 	"Verifcation failure: incorrect user or password",    # -8
 	"Serialization error : failed to write to server",    # -7
 	"Temporary file IO error",                            # -6
    "Unkown error",                                       # -5, inserted by David
 	"The upload file is an empty file, no data found",    # -4
 	"Incomplete file : only partial data is uploaded",    # -3
	"The video is over size limit (MAX_FILE_SIZE)",       # -2
    "The video is over size limit (200M)"                 # -1
]

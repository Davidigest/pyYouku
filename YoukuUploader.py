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

import urlparse
import urllib, urllib2, json, time
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import webbrowser, os

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# It is IMPORTANT to set below information before use
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
config = \
{
    'youku_pid'           :   '123456',                 # YOUKU partener ID
    'youku_user_name'     :   'YoukuUser@gmail.com',    # YOUKU user
    'youku_password'      :   'YoukuPassword',          # YOUKU user's password
}
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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


class YoukuVideoUploader(object) :
    def __init__(self, config) :
        self.config = config

        # Private variables
        self.__youku_pid          = config ["youku_pid"]
        self.__youku_user_name    = config ["youku_user_name"]
        self.__youku_password     = config ["youku_password"]
        self.__upLoadURL = r'http://gupload.youku.com/upload/uploadPackage'

    def UploadVideo(self,
                    videoPath,      # video path in a file system
                    catId,          # Category ID
                    title =         "Good morning, David",
                    description =   "Upload video with Python, by David",
                    tagInfo =       "Comma, delimited, tags"
                    ) :
        """
        Upload the videos Youku's cloud storage
        Parameters:
        <I> videoPath:      the file in local file system
        <I> description:    a string
        <I> tagInfo :       comma delimited tags, e.g.  'tag1, tag2, tag3' etc.
        <I> catId :         the category id, default 105= technology

        <O> bSuccess :      boolean, if upload successes
        <O> extraInfo:      extra/detail info if error occurs
                            if bSuccess = True, return the video_id, an integer
                            if bSuccess = False, return the detailed error message
        Note :  to get embedded script to show the iploaded video in a webpage,
                use getVideoUrl() function which returns:
                [1] The ulr of the video
                [2] Embedded script for use in HTML or PHP files
        """

        print "Begin uploading video =====>"
        param = { }
        param['partnerid']  = config['youku_pid']
        param['title']  = title	        # Video Title, maximum 50 Chinese chars, and 100 Enlish letters, do not use numbers only
        param['tags']   = tagInfo       # Video Tag, single tag : 2-6/4-12 Chinese/Eng chars, this must not be empty, max 10 tags
        param['catIds'] = catId         # Video category, only 1 categary should be assigned
        param['memo']   = description   # Video description

        param['username'] = self.__youku_user_name     # the user who uploads the video
        param['password'] = self.__youku_password	   # the user's password, if the length of this parameter is 32 bit, MD5 verification is used, otherwise, password text

        # Hard-coded paramers
        param['sourceType'] = 1         # 0=Reproduced, 1=original
        param['publicType'] = 0         # Visibility, 0= public

        #param['folderIds'] 	    # Which folder(s) to upload, use comma to seperate multi-folders


        assert os.path.isfile(videoPath), "Invalid video file path %s" % (videoPath)
        param['Filedata']    =  open(videoPath, "rb")


        register_openers()
        datagen, headers = multipart_encode(param)
        request = urllib2.Request(self.__upLoadURL, datagen, headers)
        video_id = urllib2.urlopen(request).read()  # This is a string

        self.video_id = int(video_id)

        #print "video_id= ", video_id
        if self.video_id > 0 :
            bSuccess = True
            extraInfo = self.video_id
        else :
            if self.video_id < -10 :
                self.video_id = -5        # Unknown error

            bSuccess = False
            extraInfo = errorMsg[self.video_id]

        #print bSuccess, extraInfo
        #os.system("pause")
        return bSuccess, extraInfo

    def getVideoUrl(self) :
            """
            Call this function after calling UploadVideo()
            <I> None
            <O> videoURL    : the uploaded video's url
            <O> embedScript : this embedded script will be used in user's webpage
                              e.g. the Div in a HTML or a PHP file
            """

            qm = r'"'  # qutation mark
            def wrap(someString) :
                return qm + someString + qm

            urlFormatter = r"http://player.youku.com/player.php/sid/%s/partnerid/%s/v.swf"
            videoURL = urlFormatter %(self.video_id, self.__youku_pid)

            embedScript = "<embed src=" + qm + videoURL + qm + \
            " quality=" + wrap("high") + \
            " width=" + wrap("480") + " height=" + wrap("420") + \
            " align=" + wrap ("middle") + \
            " allowScriptAccess=" + wrap("sameDomain") + \
            " type=" + wrap("application/x-shockwave-flash") + \
            r"></embed>"

            return videoURL, embedScript

def main():
    t1= time.time()
    #---------------------------------------------------------------------------
    youku = YoukuVideoUploader(config)
    bSuccess, detailInfo = youku.UploadVideo(r"SampleData/sample1.mp4", catId ='105')
    if bSuccess:
        print "Video Sucessfully uploaded, and the video_id is: %s" %detailInfo
        result = youku.getVideoUrl()
        if result != None:
            url = result[0]                 # The direct url
            script = result[1]              # The embedding script
            print script
            webbrowser.open_new_tab(url)    # Open the video in web browser

    else :
        print detailInfo

    #---------------------------------------------------------------------------
    t2= time.time()
    print "Video Upload takes %s seconds" %(t2-t1)


if __name__ == "__main__":
    main()


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
import urllib, urllib2, json
import webbrowser, os, time
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

from config import *        # User account & err msg etc


class YoukuVideoUploader(object) :
    def __init__(self) :
                            
        # Private variables, config is imported from config.py
        self.__youku_pid          = config ["youku_pid"]
        self.__youku_user_name    = config ["youku_user_name"]
        self.__youku_password     = config ["youku_password"]
        self.__upLoadURL          = config ['upload_url']

    def UploadVideo(self,
                    videoPath,                      # video path in a file system
                    title       = "Video",
                    description = "Automatically uploaded video",
                    tagInfo     = "Tags",
                    private     = True,              # boolean
                    catId       = '105'              # Category ID : technology
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
        param['partnerid']  = self.__youku_pid
        param['username']   = self.__youku_user_name   # the user who uploads the video
        param['password']   = self.__youku_password	   # the user's password, if the length of this parameter is 32 bit, MD5 verification is used, otherwise, password text

        param['title']  = title	        # Video Title, maximum 50 Chinese chars, and 100 Enlish letters, do not use numbers only
        param['tags']   = tagInfo       # Video Tag, single tag : 2-6/4-12 Chinese/Eng chars, this must not be empty, max 10 tags
        param['catIds'] = catId         # Video category, only 1 categary should be assigned
        param['memo']   = description   # Video description

        # Hard-coded paramers
        param['sourceType'] = 1             # 0=Reproduced, 1=original
        param['publicType'] = int(private)  # Visibility, 0= public

        #param['folderIds'] 	    # Which folder(s) to upload, use comma to seperate multi-folders


        assert os.path.isfile(videoPath), "Invalid video file path %s" % (videoPath)
        param['Filedata']    =  open(videoPath, "rb")


        register_openers()
        datagen, headers = multipart_encode(param)
        request = urllib2.Request(self.__upLoadURL, datagen, headers)
        video_id = urllib2.urlopen(request).read()  # This is a string

        #print "video_id=", video_id
        #os.system("pause")

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
    youku = YoukuVideoUploader()

    sampleVideoPath = os.path.join( os.path.dirname(__file__),
                                    r"SampleData\sample1.mp4")

    bSuccess, detailInfo = youku.UploadVideo(sampleVideoPath, catId ='105', private = False )
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


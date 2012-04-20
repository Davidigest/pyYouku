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

##import urlparse
##import urllib, urllib2, json
##import webbrowser, os, time
##from poster.encode import multipart_encode
##from poster.streaminghttp import register_openers

import httplib, json, urllib
from config import *        # User account and err msg


class YoukuInfo (object) :
    def __init__(self) :

        self.config = config

        # Private variables
        self.__youku_pid          = config ["youku_pid"]
        self.__youku_user_name    = config ["youku_user_name"]
        self.__youku_password     = config ["youku_password"]
        self.__upLoadURL          = config ['upload_url']


    def getVideoCategories(self) :
        url = r'api.youku.com'
        conn = httplib.HTTPConnection(url)
        #print "conn=", conn

        path = r'/api_ptcategory/?'
        param = {}
        param['pid']    =   config ["youku_pid"]    # Partner ID
        param['catpid'] =   '0'                     # Parent category, default = 0?root
        param['rt']     =   'JSON'                  # Return type

        path += urllib.urlencode(param)
        #print path
        conn.request('GET', path)
        response = conn.getresponse()

        if response.status == 200 :
            result = response.read()
            unicodedJson = json.dumps(result)

            #print result
            #result2 = json.loads(unicodedJson)
            print result





##        url = "http://api.youku.com/api_ptcategory%s" % urllib.urlencode(param)
##        print url
##        f = urllib.urlopen(url)
        #print f.read()

##        result2 = json.loads(f.read())
##        print result2


##        import os
##        os.system('pause')

##        conn.request('GET', path + strParam)
##        response = conn.getresponse()
##
##        print response.status
##
##        if response.status == 200 :
##            result = response.read()
##            print result
##            #result2 = json.loads(result)
##            #print result2

def main():
    info = YoukuInfo()
    info.getVideoCategories()



if __name__ == "__main__":
    main()
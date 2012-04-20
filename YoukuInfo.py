# coding=utf-8
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

import httplib, json, urllib
from config import *                # config.py : User account and err msg etc.


class YoukuInfo (object) :
    def __init__(self) :
        self.config = config        # imported from config.py

    def getVideoCategories(self) :
        
        """
        This function returns a list of categories in a dictionary,
        { category id : category Name }, for instance
        100 : 动漫 ;  102 : 广告 ;    104 : 汽车
        """

        param = {}
        param['pid']    =   config ["youku_pid"]    # Partner ID, important!!!
        param['catpid'] =   '0'                     # Parent category, default = 0?root
        param['rt']     =   '3'                     # Return type: 2=xml, 3=json

        # Approach I, this also works 
        #url = r"http://api.youku.com/api_ptcategory?%s" % urllib.urlencode(param)
        #result = urllib.urlopen(url)        
        #result = json.loads(result.read())
        #print result

        # Approach II
        conn = httplib.HTTPConnection('api.youku.com')
        path = r'/api_ptcategory/?' + urllib.urlencode(param)
        conn.request('GET', path)
        response = conn.getresponse()
        
        output = {}

        if response.status == 200 :
            result = response.read()
            result = json.loads(result)

            allCategories = result['item']            
            for item in allCategories :
                output[item['id']] = item['name'].encode('utf-8')
        
        return output
        

def main():
    info = YoukuInfo()
    output = info.getVideoCategories()
    for id in output.iterkeys() :
        print id, ':', output[id]    

if __name__ == "__main__":
    main()
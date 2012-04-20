pyYouku
=======

Youku = Youtube in China (http://Youku.com).
This project aims at batch uploading videos to Youku's cloud.

Example :
>       youku = YoukuVideoUploader(config)
      bSuccess, detailInfo = youku.UploadVideo("sample.mp4", private = False )
      if bSuccess :
            youku.getVideoUrl( )	


Prerequisites:

>       If you haven't installed setup_tools, install it. 
      Go to http://pypi.python.org/pypi/setuptools/ and 
      follow the instructures there to install "setup tools"
---------------------------------------------------------------
>       Install Python Poster Library:    
      cmd > easy_install poster



Other notes:
>     You should have your own Youku account setup:
      User: "xxx@yyy.com"
      Psw : "mypassowrd"



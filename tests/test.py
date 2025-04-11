from FFMPEG_Filters import *

video = videoFilters()
#First we define the parameters of the video, which are as follows
video.setExportParameters(
    imagePath=r"C:\Users\Tgthegood\Pictures\Overlord\Tg_0.jpg", #Image input
    pathExport=r"C:\Users\Tgthegood\Documents\Novels\Example.mp4", #Output for the video
    exportResolution=(1280, 720), #Format for the video (1280, 720 Youtube), also, for other formats like (1080, 1920 tiktok), make sure your image ratio is 9/16 or higher depending on the filter, FFMPEG_Filters does not distort the image to create the video
    exportFfps=30, #Ffps of the video
    duration=10, #Duration of the video
    scale=2 #Scale for the Image, more the higher the value of this, the smoother the filters, but there is a limit, 2 is the most suitable.
)

#Filters that can be used, currently I only have 4, ZoomIn, ZoomOut, ScrollBottom, ScrollTop
#Also, you cannot call two contradicting functions like ZoomIn and ZoomOut at the same time.
video.zoomIn() 
video.scrollTop()

#Making the Video
video.makeVideo()
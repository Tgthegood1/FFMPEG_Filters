import subprocess
import sys
from pathlib import Path
from PIL import Image
import io

class videoFilters:
    def __init__(self):
        #Variables para el control de los filtros
        self.scale = 0

        #Variables para el control de exportacion de video
        self.image_Path = ""
        self.path_Export = ""
        self.export_Resolution = ()
        self.export_Ffps = 0
        self.export_Duration = 0
        self.pixelFrameZoom = 0
        self.intensity = 0

        #Variable para los filtros
        self.filtros = {}

    def setExportParameters(self, imagePath, pathExport, exportResolution=(1280, 720), exportFfps=30, duration=10, scale=2):
        if not imagePath or not Path(imagePath).is_file():
            sys.exit("You need to provide a valid videoPath for continue...")
        if not Path(pathExport).parent.exists():
            sys.exit("You need to provide a valid Path for export the video...")

        self.image_Path = imagePath
        self.path_Export = pathExport
        self.export_Resolution = exportResolution
        self.export_Ffps = exportFfps
        self.export_Duration = duration
        self.scale = scale

    def scrollTop(self):
        self.filtros["scrollTop"] = self.export_Duration

    def scrollBottom(self):
        self.filtros["scrollBottom"] =  self.export_Duration

    def zoomIn(self, intensity=6):
        self.filtros["zoomIn"] =  self.export_Duration
        self.intensity = intensity

    def zoomOut(self, intensity=6):
        self.filtros["zoomOut"] =  self.export_Duration
        self.intensity = intensity

    def makeVideo(self):
        #Rutas Imagen y video
        imageStrPath = str(self.image_Path)
        exportStrPath = str(self.path_Export)

        #Parametros de exportacion
        exportResolution = str(self.export_Resolution[0]) + "x" + str(self.export_Resolution[1])
        exportFfps = str(self.export_Ffps)

        #Variables para uso interno
        imageSteps = self.export_Ffps * self.export_Duration
        cutParameters = {}

        #Controlador de filtros Scroll
        if "scrollTop" in self.filtros and "scrollBottom" in self.filtros:
            sys.exit("Two scroll filters cannot be applied at the same time...")
        elif "scrollTop" in self.filtros:
            cutParameters["scrollTop"] = self.filtros["scrollTop"]
        elif "scrollBottom" in self.filtros:
            cutParameters["scrollBottom"] = self.filtros["scrollBottom"]
        #Controlador de filtros Zoom
        if "zoomIn" in self.filtros and "zoomOut" in self.filtros:
            sys.exit("Two zoom filters cannot be applied at the same time...")
        elif "zoomIn" in self.filtros:
            cutParameters["zoomIn"] = self.filtros["zoomIn"]
        elif "zoomOut" in self.filtros:
            cutParameters["zoomOut"] = self.filtros["zoomOut"]

        #Abriendo la imagen para pruebas
        imagePil = Image.open(imageStrPath)
        width, height = imagePil.size
        
        #Redimension de la imagen para el video
        scaleFactorImage = width / height
        newHeight = int(self.export_Resolution[0] / scaleFactorImage)
        resizedImage = imagePil.resize((self.export_Resolution[0], newHeight), Image.LANCZOS)
        w, h = resizedImage.size
        imagePilResized = resizedImage.resize((w*self.scale, h*self.scale), Image.LANCZOS)

        #Comprobantes necesarios para Scroll y Zoom "Tamaño de imagen para trabajar"
        if "scrollTop" in self.filtros or "scrollBottom" in self.filtros:
            relation = newHeight / self.export_Resolution[0]
            if relation >= 1.7:
                sys.exit("Image to small to scroll")

        print("Starting the process..")
        #Operacion con Duration para obtener el tamaño del recorte por frame para Scroll
        if "scrollTop" in self.filtros or "scrollBottom" in self.filtros:
            leftoverImage = (h - self.export_Resolution[1])
            stepFrameScroll = leftoverImage / imageSteps

        if "zoomIn" in self.filtros or "zoomOut" in self.filtros:
            #Operacion con Duration para obtener el tamaño del recorte por frame para Zoom
            stepFrameZoomWidth = (((self.export_Resolution[0]*self.scale) / self.intensity) / imageSteps)
            stepFrameZoomHeight = (((self.export_Resolution[1]*self.scale) / self.intensity) / imageSteps)
            distanceFrameZoomHeight = stepFrameZoomHeight * imageSteps
            distanceFrameZoomWidth = stepFrameZoomWidth * imageSteps

        #Definiendo area de Crop cuidado con Zoom out y Scrolltop
        AreaCrop = [0, 0, (self.export_Resolution[0] * self.scale), (self.export_Resolution[1] * self.scale)]
        if "scrollTop" in self.filtros:
            AreaCrop[1] = leftoverImage
            AreaCrop[3] = newHeight * self.scale
        if "zoomOut" in self.filtros:
            AreaCrop[1] = distanceFrameZoomHeight
            AreaCrop[3] = ((self.export_Resolution[1]*self.scale) - distanceFrameZoomHeight)
            AreaCrop[0] = distanceFrameZoomWidth
            AreaCrop[2] = ((self.export_Resolution[0]*self.scale) - distanceFrameZoomWidth)

        BytesForVideo = []
        for step in range(imageSteps):
            if "scrollBottom" in self.filtros:
                AreaCrop[1] += stepFrameScroll
                AreaCrop[3] += stepFrameScroll

            if "scrollTop" in self.filtros:
                AreaCrop[1] -= stepFrameScroll
                AreaCrop[3] -= stepFrameScroll

            if "zoomIn" in self.filtros:
                AreaCrop[1] += stepFrameZoomHeight
                AreaCrop[3] -= stepFrameZoomHeight
                AreaCrop[0] += stepFrameZoomWidth
                AreaCrop[2] -= stepFrameZoomWidth

            if "zoomOut" in self.filtros:
                AreaCrop[1] -= stepFrameZoomHeight
                AreaCrop[3] += stepFrameZoomHeight
                AreaCrop[0] -= stepFrameZoomWidth
                AreaCrop[2] += stepFrameZoomWidth

            imageCrop = imagePilResized.crop(tuple(AreaCrop))
            imageFinal = imageCrop.resize((self.export_Resolution[0], self.export_Resolution[1]), Image.LANCZOS)
            with io.BytesIO() as imgBytes:
                imageFinal.save(imgBytes, format="JPEG")
                BytesForVideo.append(imgBytes.getvalue())

        commandFfmpegOutput = [
            "ffmpeg",
            "-f", "image2pipe",
            "-y",
            "-framerate", exportFfps,
            "-i", "-",
            "-s", exportResolution,
            "-r", exportFfps,
            "-c:v", "libx264",
            "-preset", "medium",
            exportStrPath
        ]

        commandOutput = subprocess.Popen(commandFfmpegOutput, stdin=subprocess.PIPE)

        for imgBytes in BytesForVideo:
            commandOutput.stdin.write(imgBytes)

        commandOutput.stdin.close()
        commandOutput.wait()
        print("Ending the process...")
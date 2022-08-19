import os
import piexif
import re
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
import configparser

# class for parsing path setting from config.ini
class directorypass:
    def __init__(self):
        self.sourcepath = self._parsefromconfig("source")
        self.targetpath = self._parsefromconfig("target")

    def _parsefromconfig(self, mode):
        config = configparser.ConfigParser()
        config.read(".\\config.ini")
        if mode == "source":
            return config["PATH"]["source"]
        elif mode == "target":
            return config["PATH"]["target"]

# class for writing exif
class exifwriter:
    def __init__(self, filename, sourcePath, targetPath):
        self.filename = filename
        self.sourcePath = sourcePath
        self.targetPath = targetPath
    
    def WriteExif(filename):
        return True

    def GetDateFromFilename(self):
        Name, _= self.GetNameAndExtension()
        datepattern = "[0-9]{4}-[0-9]{2}-[0-9]{2}"
        timepattern = "[0-9]{2}-[0-9]{2}-[0-9]{2}\.[0-9]{3}"
        datestr = re.match(datepattern, Name)
        return True

    def GetNameAndExtension(self):
        SourceFilePath, _ = self.FilePath()
        return os.path.splitext(os.path.basename(SourceFilePath)),os.path.basename(SourceFilePath)

    def CheckExists(self):
        _, TargetFilePath = self.FilePath()
        if os.path.exists(TargetFilePath.replace(".png",".jpg",1)) == True:
            return True
        else:
            return False

    def FilePath(self):
        return self.sourcePath + self.filename, self.targetPath + self.filename

def main():
    print("start")
    path = directorypass()
    sourcePATH,targetPath = path.sourcepath,path.targetpath
    # Open the file in list
    for file in os.listdir(sourcePATH):
        try:
            kakuchosi = file.split(".")[2]
        except:
            continue
        path, pathwrited = sourcePATH + file, targetPath + file
        img = Image.open(path)
        print("opened file:"+ path)
        # if the file is not a jpg, skip it
        if kakuchosi == "png":
            if os.path.exists(pathwrited.replace(".png",".jpg",1)) == True:
                print("skipped")
                continue
            # Extract time stamp from filename
            nopng = file.split(".png")[0]
            date,year,month,day = nopng.split("_")[2],int(date.split("-")[0]),int(date.split("-")[1]),int(date.split("-")[2])
            time = nopng.split("_")[3]
            hour,mini,sec = int(time.split("-")[0]),int(time.split("-")[1]),int(round(float(time.split("-")[2]),0))
            print(date+ " " +time)
            print("making Exif time stamp")
            # Make time stamp
            exif_dict = {}
            exif_dict['Exif'] = {piexif.ExifIFD.DateTimeOriginal: datetime(year,month,day,hour,mini,0).strftime("%Y:%m:%d %H:%M:%S")}
            exif_bytes = piexif.dump(exif_dict)
            img = img.convert('RGB')
            newpath = targetPath + nopng + ".jpg"
            img.save(newpath, "JPEG", quality=95, exif=exif_bytes)
        # Routine for when jpg or jpeg file in source path, just print exif data in the image file
        elif kakuchosi == "jpg" or kakuchosi == "jpeg":
            try:
                exif_dict = piexif.load(img.info['exif'])
                print(exif_dict)
            except:
                print("no exif data")
                continue
 
if __name__ == '__main__':
    main()
import glob
from os.path import basename
import re
from datetime import datetime
from PIL import Image
import piexif

def get_datetime_from_filename(filename:str):
    pattern = r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}"
    match = re.search(pattern, filename)
    if match:
        time_str = match.group()
        dt_obj = datetime.strptime(time_str, "%Y-%m-%d_%H-%M-%S")
        return dt_obj
    else:
        return None

if __name__ == "__main__":
    print("Start")
    source_path = "./source/"
    target_path = "./converted/"
    file_list = glob.glob(source_path + "*.png")
    exist_list = [basename(name) for name in glob.glob(target_path + "*.jpg")]
    conv_list = [file for file in file_list if basename(file).replace(".png",".jpg") not in exist_list]
    print("File to be converted - " + str(len(conv_list)) + " files")
    for file in conv_list:
        file_name = basename(file)
        created_date = get_datetime_from_filename(file_name)
        output_path = target_path + file_name.replace(".png",".jpg")
        with Image.open(file) as png_image:
            jpg_image = png_image.convert('RGB')
            new_exif_dict = {"Exif":{piexif.ExifIFD.DateTimeOriginal:created_date.strftime("%Y:%m:%d %H:%M:%S")}}
            exif_bytes = piexif.dump(new_exif_dict)
            jpg_image.save(output_path,exif=exif_bytes)
        print(file_name + " - converted")
    print("Finished")
"""
Pic Cron
========
Script for the main functionality of scraping meta-data from pictures and renaming them
Starting out with accessing files from my filesystemw
"""
from pathlib import Path

from PIL import Image, UnidentifiedImageError
from PIL.ExifTags import TAGS


def main():
    """Driver"""
    
    pic_dir = Path(r"E:\NZ Pics\JJ")
    for pic in pic_dir.iterdir():
        try:
            image = Image.open(str(pic))
        except UnidentifiedImageError:
            continue
        
        # extract EXIF data
        exif_data = image.getexif()

        for tag_id in exif_data:
            # get the tag name, instead of human unreadable tag id
            tag = TAGS.get(tag_id, tag_id)
            data = exif_data.get(tag_id)
            # decode bytes 
            if isinstance(data, bytes):
                data = data.decode()
            print(f"{tag:25}: {data}")

if __name__ == "__main__":
    main()
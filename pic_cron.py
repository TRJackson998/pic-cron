"""
Pic Cron
========
Script for the main functionality of scraping meta-data from pictures and renaming them
Starting out with accessing files from my filesystemw

Reference - https://stackoverflow.com/questions/72530975/extract-gps-data-using-python-and-pil-is-failing
"""

from pathlib import Path

from exif import Image
from geopy.geocoders import Nominatim
from plum.exceptions import UnpackError


def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref == "W":
        decimal_degrees = -decimal_degrees
    return decimal_degrees


def main():
    """Driver"""

    pic_dir = Path(r"E:\NZ Pics\JJ")
    for pic in pic_dir.iterdir():
        try:
            image = Image(str(pic))
        except UnpackError:
            continue
        if not image.has_exif:
            continue

        city = ""
        if hasattr(image, "gps_latitude") and hasattr(image, "gps_longitude"):
            lat = decimal_coords(image.gps_latitude, image.gps_latitude_ref)
            lon = decimal_coords(image.gps_longitude, image.gps_longitude_ref)
            geolocator = Nominatim(user_agent="GetLoc")
            location = geolocator.reverse(f"{lat}, {lon}")

            if location:
                address = location.raw["address"]
                city = (
                    address.get("city")
                    or address.get("town")
                    or address.get("village")
                    or address.get("hamlet")
                )
                if not city:
                    city = address.get("county") or address.get("state")
        if city:
            city = city.split(" ")[0]

        image_dt = image.datetime
        new_name = " ".join(s for s in [image_dt, city] if s)
        new_name += pic.suffix
        print(new_name)


if __name__ == "__main__":
    main()

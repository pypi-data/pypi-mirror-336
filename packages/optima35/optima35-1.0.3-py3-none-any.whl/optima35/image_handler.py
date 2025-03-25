from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageQt
import piexif
import piexif.helper
from fractions import Fraction

class ImageProcessor:
    """Functions using pillow are in here."""
    def __init__(self):
        pass

    def open_image(self, path):
        """Open an image from path, returns image object."""
        return Image.open(path)

    def get_image_size(self, image):
        """Simply get image size."""
        return image.size

    def grayscale(self, image):
        """Change to grayscale"""
        return image.convert("L")

    def change_contrast(self, image, change):
        """Change contrast by percent."""
        enhancer = ImageEnhance.Contrast(image)
        new_img = enhancer.enhance(1 + (change/100))
        return new_img

    def change_brightness(self, image, change):
        """Changes brightness by percent"""
        enhancer = ImageEnhance.Brightness(image)
        new_img = enhancer.enhance(1 + (change/100))
        return new_img

    def resize_image(self, image, percent, resample = True):
        """Resize an image by giving a percent."""
        new_size = tuple(int(x * (percent / 100)) for x in image.size)
        resized_image = image.resize(new_size)
        return resized_image

    def add_watermark(self, image, text, font_size_percentage):
        """Addes a watermark to the image using default os font."""
        drawer = ImageDraw.Draw(image)
        imagewidth, imageheight = image.size
        margin = (imageheight / 100) * 2 # margin dynamic, 2% of image size
        font_size = (imagewidth / 100) * font_size_percentage

        try: # Try loading front, if notaviable return unmodified image
            font = ImageFont.load_default(font_size)
        except Exception as e:
            print(f"Error {e}\nloading font for watermark, please ensure font is installed...\n")
            return image

        c, w, textwidth, textheight, = drawer.textbbox(xy = (0, 0), text = text, font = font) # Getting text size, only need the last two values
        x = imagewidth - textwidth - margin
        y = imageheight - textheight - margin

        # thin border
        drawer.text((x-1, y), text, font = font, fill = (64, 64, 64))
        drawer.text((x+1, y), text, font = font, fill = (64, 64, 64))
        drawer.text((x, y-1), text, font = font, fill = (64, 64, 64))
        drawer.text((x, y+1), text, font = font, fill = (64, 64, 64))
        # Adding text in the desired color
        drawer.text((x, y), text, font = font, fill = (255, 255, 255))

        return image

    def save_image(self, image, path, file_type, jpg_quality, png_compressing, optimize, piexif_exif_data):
        # partly optimized by chatGPT
        """
        Save an image to the specified path with optional EXIF data.
        """
        save_params = {"optimize": optimize}
        # Add file-specific parameters
        if file_type == "jpg" or "webp":
            save_params["quality"] = jpg_quality
        elif file_type == "png":
            save_params["compress_level"] = png_compressing
        elif file_type not in ["webp", "jpg", "png"]:
            print(f"Type: {file_type} is not supported.")
            return
        # Add EXIF data if available
        if piexif_exif_data is not None:
            save_params["exif"] = piexif.dump(piexif_exif_data)
            if file_type == "webp":
                print("File format webp does not support all exif features, some information might get lost...\n")
        try:
            image.save(f"{path}.{file_type}", **save_params)
        except Exception as e:
            print(f"Failed to save image: {e}")

    def convert_pil_to_qtimage(self, pillow_image):
        qt_image = ImageQt.ImageQt(pillow_image)
        return qt_image

class ExifHandler:
    """Function using piexif are here."""
    def __init__(self):
        pass

    def get_exif_info(self, image):
        return(piexif.load(image.info['exif']))

    def build_exif_bytes(self, user_data, imagesize):
        """Build a piexif-compatible EXIF dictionary from a dicts."""
        # Mostly made by ChatGPT, some adjustment
        zeroth_ifd = {
            piexif.ImageIFD.Make: user_data["make"].encode("utf-8"),
            piexif.ImageIFD.Model: user_data["model"].encode("utf-8"),
            piexif.ImageIFD.Software: user_data["software"].encode("utf-8"),
            piexif.ImageIFD.Copyright: user_data["copyright_info"].encode("utf-8"),
            piexif.ImageIFD.Artist: user_data["artist"].encode("utf-8"),
            piexif.ImageIFD.ImageDescription: user_data["image_description"].encode("utf-8"),
            piexif.ImageIFD.XResolution: (72, 1),
            piexif.ImageIFD.YResolution: (72, 1),
        }
        exif_ifd = {
            piexif.ExifIFD.LensModel: user_data["lens"].encode("utf-8"),
            piexif.ExifIFD.UserComment: piexif.helper.UserComment.dump(user_data["user_comment"]),
            piexif.ExifIFD.ISOSpeedRatings: int(user_data["iso"].encode("utf-8")),
            piexif.ExifIFD.PixelXDimension: imagesize[0],
            piexif.ExifIFD.PixelYDimension: imagesize[1],
        }
        if "date_time_original" in user_data:
            exif_ifd[piexif.ExifIFD.DateTimeOriginal] = user_data["date_time_original"].encode("utf-8")

        return {"0th": zeroth_ifd, "Exif": exif_ifd}

    def _deg_to_dms(self, decimal_coordinate, cardinal_directions):
        """
        This function converts decimal coordinates into the DMS (degrees, minutes and seconds) format.
        It also determines the cardinal direction of the coordinates.

        :param decimal_coordinate: the decimal coordinates, such as 34.0522
        :param cardinal_directions: the locations of the decimal coordinate, such as ["S", "N"] or ["W", "E"]
        :return: degrees, minutes, seconds and compass_direction
        :rtype: int, int, float, string
        """
        if decimal_coordinate < 0:
            compass_direction = cardinal_directions[0]
        elif decimal_coordinate > 0:
            compass_direction = cardinal_directions[1]
        else:
            compass_direction = ""
        degrees = int(abs(decimal_coordinate))
        decimal_minutes = (abs(decimal_coordinate) - degrees) * 60
        minutes = int(decimal_minutes)
        seconds = Fraction((decimal_minutes - minutes) * 60).limit_denominator(100)
        return degrees, minutes, seconds, compass_direction

    def _dms_to_exif_format(self, dms_degrees, dms_minutes, dms_seconds):
        """
        This function converts DMS (degrees, minutes and seconds) to values that can
        be used with the EXIF (Exchangeable Image File Format).

        :param dms_degrees: int value for degrees
        :param dms_minutes: int value for minutes
        :param dms_seconds: fractions.Fraction value for seconds
        :return: EXIF values for the provided DMS values
        :rtype: nested tuple
        """
        exif_format = (
            (dms_degrees, 1),
            (dms_minutes, 1),
            (int(dms_seconds.limit_denominator(100).numerator), int(dms_seconds.limit_denominator(100).denominator))
        )
        return exif_format

    def add_geolocation_to_exif(self, exif_data, latitude, longitude):
        """
        https://stackoverflow.com/questions/77015464/adding-exif-gps-data-to-jpg-files-using-python-and-piexif
        This function adds GPS values to an image using the EXIF format.
        This fumction calls the functions deg_to_dms and dms_to_exif_format.

        :param image_path: image to add the GPS data to
        :param latitude: the north–south position coordinate
        :param longitude: the east–west position coordinate
        """
        # converts the latitude and longitude coordinates to DMS
        latitude_dms = self._deg_to_dms(latitude, ["S", "N"])
        longitude_dms = self._deg_to_dms(longitude, ["W", "E"])

        # convert the DMS values to EXIF values
        exif_latitude = self._dms_to_exif_format(latitude_dms[0], latitude_dms[1], latitude_dms[2])
        exif_longitude = self._dms_to_exif_format(longitude_dms[0], longitude_dms[1], longitude_dms[2])

        try:
            # https://exiftool.org/TagNames/GPS.html
            # Create the GPS EXIF data
            coordinates = {
                piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
                piexif.GPSIFD.GPSLatitude: exif_latitude,
                piexif.GPSIFD.GPSLatitudeRef: latitude_dms[3],
                piexif.GPSIFD.GPSLongitude: exif_longitude,
                piexif.GPSIFD.GPSLongitudeRef: longitude_dms[3]
            }
            # Update the EXIF data with the GPS information
            exif_data["GPS"] = coordinates

            return exif_data
        except Exception as e:
            print(f"Error: {str(e)}")

    def insert_exif(self, exif_dict, img_path):
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, img_path)

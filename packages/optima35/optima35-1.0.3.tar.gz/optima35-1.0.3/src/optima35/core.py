import re
import os
from datetime import datetime
from optima35.image_handler import ImageProcessor, ExifHandler
from optima35 import __version__

class OptimaManager:
    def __init__(self):
        self.name = "optima35"
        self.version = __version__
        self.image_processor = ImageProcessor()
        self.exif_handler = ExifHandler()

    def _modify_timestamp_in_exif(self, data_for_exif: dict, filename: str):
            """"Takes a dict formated for exif use by piexif and adjusts the date_time_original, changing the minutes and seconds to fit the number of the filname."""
            last_three = filename[-3:len(filename)]
            total_seconds = int(re.sub(r'\D+', '', last_three))
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            time = datetime.strptime(data_for_exif["date_time_original"], "%Y:%m:%d %H:%M:%S") # change date time string back to an time object for modification
            new_time = time.replace(hour=12, minute=minutes, second=seconds)
            data_for_exif["date_time_original"] = new_time.strftime("%Y:%m:%d %H:%M:%S")
            return data_for_exif

    def _process_image(
        self,
        image_input_file: str,
        resize: int = None,
        watermark: str = None,
        font_size: int = 2,
        grayscale: bool = False,
        brightness: float = None,
        contrast: float = None
    ):
    # My Code restructured by ChatGPT, but had to fix bugs
        img = self.image_processor.open_image(image_input_file)
            # Apply transformations
        if resize is not None:
            img = self.image_processor.resize_image(img, percent=resize)
        if watermark is not None:
            img = self.image_processor.add_watermark(img, watermark, font_size)
        if grayscale:
            img = self.image_processor.grayscale(img)
        if brightness is not None:
            img = self.image_processor.change_brightness(img, brightness)
        if contrast is not None:
            img = self.image_processor.change_contrast(img, contrast)
        return img

    def _handle_exif(
        self,
        image,
        file_name,
        dict_for_exif: dict = None,
        gps: tuple[float, float] = None,
        copy_exif: bool = False
    ):
    # My Code restructured by ChatGPT, but had to fix bugs
        # Build or copy EXIF data
        if dict_for_exif:
            if "date_time_original" in dict_for_exif:
                dict_for_exif = self._modify_timestamp_in_exif(dict_for_exif, file_name)
            exif_data = self.exif_handler.build_exif_bytes(
                dict_for_exif, self.image_processor.get_image_size(image)
            )
            if gps:
                exif_data = self.exif_handler.add_geolocation_to_exif(
                    exif_data, gps[0], gps[1]
                )
        elif copy_exif:
            exif_data = self.exif_handler.get_exif_info(image)
        else:
            exif_data = None
        return exif_data

    def process_and_save_image(
        self,
        image_input_file: str,
        image_output_file: str,
        file_type: str = "jpg",
        quality: int = 90,
        compressing: int = 6,
        optimize: bool = False,
        resize: int = None,
        watermark: str = None,
        font_size: int = 2,
        grayscale: bool = False,
        brightness: float = None,
        contrast: float = None,
        dict_for_exif: dict = None,
        gps: tuple[float, float] = None,
        copy_exif: bool = False
    ) -> None:
        """
        Processes an image with the given parameters and saves the output to a file.

        Args:
            image_input_file (str): Path to the input image file.
            image_output_file (str): Path to save the processed image.
            file_type (str): Output image format ('jpg', 'png'). Defaults to 'jpg'.
            quality (int): JPEG quality (1-100). Defaults to 90.
            compressing (int): PNG compression level (0-9). Defaults to 6.
            optimize (bool): Optimize image for smaller file size. Defaults to False.
            resize (int, optional): Resize percentage. Defaults to None.
            watermark (str, optional): Watermark text to add. Defaults to None.
            font_size (int): Font size for the watermark. Defaults to 2.
            grayscale (bool): Convert image to grayscale. Defaults to False.
            brightness (float, optional): Adjust brightness (e.g., 1.2 for 20% brighter). Defaults to None.
            contrast (float, optional): Adjust contrast (e.g., 1.5 for 50% higher contrast). Defaults to None.
            dict_for_exif (dict, optional): EXIF metadata to insert. Defaults to None.
            gps (tuple[float, float], optional): GPS coordinates (latitude, longitude). Defaults to None.
            copy_exif (bool): Copy EXIF metadata from the input image. Defaults to False.

        Returns:
            None
        """
        # My Code restructured by ChatGPT
        processed_img = self._process_image(
            image_input_file,
            resize,
            watermark,
            font_size,
            grayscale,
            brightness,
            contrast,
        )

        # Handle EXIF metadata
        exif_piexif_format = self._handle_exif(
            image = processed_img,
            file_name = image_output_file,
            dict_for_exif = dict_for_exif,
            gps = gps,
            copy_exif = copy_exif
        )

        # Save the image
        self.image_processor.save_image(
            image = processed_img,
            path = image_output_file,
            piexif_exif_data = exif_piexif_format,
            file_type = file_type,
            jpg_quality = quality,
            png_compressing = compressing,
            optimize = optimize,
        )

    def process_image_object(
        self,
        image_input_file: str,
        resize: int = None,
        watermark: str = None,
        font_size: int = 2,
        grayscale: bool = False,
        brightness: float = None,
        contrast: float = None
    ):
        """
        Processes an image with the given parameters and returns the modified image object.

        Args:
            image_input_file (str): Path to the input image file.
            resize (int, optional): Resize percentage. Defaults to None.
            watermark (str, optional): Watermark text to add. Defaults to None.
            font_size (int): Font size for the watermark. Defaults to 2.
            grayscale (bool): Convert image to grayscale. Defaults to False.
            brightness (float, optional): Adjust brightness. Defaults to None.
            contrast (float, optional): Adjust contrast. Defaults to None.

        Returns:
            Image: The processed image object.
        """
        # My Code restructured by ChatGPT
        processed_img = self._process_image(
            image_input_file,
            resize,
            watermark,
            font_size,
            grayscale,
            brightness,
            contrast,
        )
        return self.image_processor.convert_pil_to_qtimage(processed_img)

    def insert_exif_to_image(self, exif_dict: dict, image_path: str, gps: tuple[float, float] = None) -> None:
        """
        Inserts EXIF metadata into an image.

        Args:
            exif_data (dict): A dictionary containing EXIF metadata as key-value pairs (e.g., strings, integers).
            image_path (str): Absolute path to the target image file.
            gps (tuple[float, float], optional): GPS coordinates as a tuple (latitude, longitude). Defaults to None.

        Returns:
            None: The function modifies the image file in place.
        """
        # Restructured by ChatGPT
        image_name, ending = os.path.splitext(os.path.basename(image_path))
        img = self.image_processor.open_image(image_path)
        selected_exif = exif_dict
        if "date_time_original" in exif_dict:
            selected_exif = self._modify_timestamp_in_exif(selected_exif, image_name)

        exif_piexif_format = self.exif_handler.build_exif_bytes(
            selected_exif, self.image_processor.get_image_size(img)
        )

        # GPS data
        if gps is not None:
            latitude = gps[0]
            longitude = gps[1]
            exif_piexif_format = self.exif_handler.add_geolocation_to_exif(exif_piexif_format, latitude, longitude)

        self.exif_handler.insert_exif(exif_dict = exif_piexif_format, img_path = image_path)

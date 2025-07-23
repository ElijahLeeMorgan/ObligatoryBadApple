from PIL import Image
import numpy as np
import os
import logging
from typing import Callable



class BaseImageProcessor:
    logger = logging.getLogger(__name__)
    logger.debug(f"{__name__} class initialized.")

    @staticmethod
    def _check_file(filepath: str) -> bool:
        if not os.path.isfile(filepath):
            BaseImageProcessor.logger.error(f"File not found: {filepath}")
            raise FileNotFoundError(f"File not found: {filepath}")
        if not os.access(filepath, os.R_OK):
            BaseImageProcessor.logger.error(f"File not readable: {filepath}")
            raise PermissionError(f"File not readable: {filepath}")
        if not os.path.splitext(filepath)[1].lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff']:
            BaseImageProcessor.logger.error(f"Unsupported file type: {os.path.splitext(filepath)[1]}")
            raise ValueError(f"Unsupported file type: {os.path.splitext(filepath)[1]}")
        BaseImageProcessor.logger.info(f"File check passed: {filepath}")
        return True

    @staticmethod
    def _check_folder(folder_path: str) -> bool:
        if not os.path.isdir(folder_path):
            BaseImageProcessor.logger.error(f"Folder not found: {folder_path}")
            raise NotADirectoryError(f"Folder not found: {folder_path}")
        if not os.access(folder_path, os.R_OK):
            BaseImageProcessor.logger.error(f"Folder not readable: {folder_path}")
            raise PermissionError(f"Folder not readable: {folder_path}")
        BaseImageProcessor.logger.info(f"Folder check passed: {folder_path}")
        return True

    @staticmethod
    def resize(image: Image.Image, size: tuple[int, int]) -> Image.Image:
        BaseImageProcessor.logger.info(f"Resizing image to {size}px")
        return image.resize(size, Image.Resampling.LANCZOS)

    @staticmethod
    def chunk(image: Image.Image, size: tuple[int, int] = (20, 20)) -> list[Image.Image]:
        BaseImageProcessor.logger.info(f"Chunking image into {size}px pieces")
        width, height = image.size
        chunks = []
        for y in range(0, height, size[1]):
            for x in range(0, width, size[0]):
                box = (x, y, min(x + size[0], width), min(y + size[1], height))
                chunks.append(image.crop(box))
        return chunks

    @staticmethod
    def closest_image(image: Image.Image, candidates: dict[int, Image.Image], size: tuple[int, int] = (20, 20)) -> Image.Image:
        """
        Compare input image to all candidate images and return the closest match.
        Uses Mean Squared Error to determine similarity.
        """
        input_array = np.array(image.convert('L')).astype(np.float32)
        
        best_img = next(iter(candidates.values()))
        best_score = float('inf')
        
        for candidate_value, candidate_img in candidates.items():
            if candidate_img.size != size:
                candidate_img = BaseImageProcessor.resize(candidate_img, size)

            candidate_array = np.array(candidate_img.convert('L')).astype(np.float32)

            mse = np.mean((input_array - candidate_array) ** 2)
            
            if mse < best_score:
                best_score = mse
                best_img = candidate_img
        
        return best_img

    @staticmethod
    def process(filepath: str, process_func: Callable, *args, **kwargs) -> Image.Image:
        BaseImageProcessor._check_file(filepath)

        image = Image.open(filepath)
        return process_func(image, *args, **kwargs)

    @staticmethod
    def mass_process(input_folder_path: str, output_folder_path: str, filetype: str, process_func: Callable, *args, **kwargs):
        BaseImageProcessor._check_folder(input_folder_path)
        BaseImageProcessor._check_folder(output_folder_path)

        for filename in os.listdir(input_folder_path):
            if filename.lower().endswith(filetype):  # Only lowercase for comparison
                filepath = os.path.join(input_folder_path, filename)  # Use original filename

                BaseImageProcessor._check_file(filepath)
                processed_image = BaseImageProcessor.process(filepath, process_func, *args, **kwargs)
                processed_image.save(os.path.join(output_folder_path, f"processed_{filename}"))

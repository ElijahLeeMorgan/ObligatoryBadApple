from PIL import Image
from os import path, listdir
import os

INPUT_FOLDER = "/workspaces/ObligatoryBadApple/textures/dice/vanilla"
OUTPUT_FOLDER = "/workspaces/ObligatoryBadApple/textures/dice/dithered"
SIZE = (40, 40)

for img_path in listdir(INPUT_FOLDER):
    with Image.open(path.join(INPUT_FOLDER, img_path)) as img:
        print(f"Processing {img_path}...")
        input_image = img

        # Resize the image to 16x16 using the Lanczos filter
        resized_image = input_image.resize(SIZE, Image.LANCZOS)
        # Convert the image to a palette-based image with dithering
        dithered_image = resized_image.convert("P", dither=Image.FLOYDSTEINBERG)

        # Ensure the output folder exists
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)

        # Save with the prefix in the filename within the output directory
        output_path = path.join(OUTPUT_FOLDER, f"dithered_{SIZE[0]}x{SIZE[1]}_{img_path}")
        dithered_image.save(output_path)
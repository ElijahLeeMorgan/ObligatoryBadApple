from PIL import Image
from os import path, listdir
import os

INPUT_FOLDER = "/workspaces/ObligatoryBadApple/src/imgProcessing/textures/dice/inverted"
OUTPUT_FOLDER = "/workspaces/ObligatoryBadApple/src/imgProcessing/textures/dice/inverted/dithered/"
SIZE = (20, 20)

for img_path in listdir(INPUT_FOLDER):
    if not img_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        continue
    with Image.open(path.join(INPUT_FOLDER, img_path)) as img:
        print(f"Processing {img_path}...")
        input_image = img

        # Resize the image to 16x16 using the Lanczos filter
        resized_image = input_image.resize(SIZE, Image.LANCZOS) # type: ignore
        # Convert the image to a palette-based image with dithering
        dithered_image = resized_image.convert("P", dither=Image.FLOYDSTEINBERG) # type: ignore

        # Ensure the output folder exists
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)

        # Save with the prefix in the filename within the output directory
        output_path = path.join(OUTPUT_FOLDER, f"dithered_{SIZE[0]}x{SIZE[1]}_{img_path}")
        dithered_image.save(output_path)
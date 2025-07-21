from PIL import Image
from os import path, listdir

INPUT_FOLDER = "../../textures/dice/vanilla/"
OUTPUT_FOLDER = "../../textures/dice/dithered/"

for img_path in listdir(INPUT_FOLDER):
    with Image.open(path.join(INPUT_FOLDER, img_path)) as img:
        print(f"Processing {img_path}...")
        input_image = img

        # Resize the image to 16x16 using the Lanczos filter
        resized_image = input_image.resize((16, 16), Image.LANCZOS)

        # Convert the image to a palette-based image with dithering
        dithered_image = resized_image.convert("P", dither=Image.FLOYDSTEINBERG)

        dithered_image.save(path.join(OUTPUT_FOLDER, img_path))
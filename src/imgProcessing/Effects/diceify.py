from PIL import Image
from ._BaseEffect import BaseImageProcessor

class Diceify(BaseImageProcessor):
    DICE_FOLDER = "/workspaces/ObligatoryBadApple/src/imgProcessing/textures/dice/"
    DICE_IMG: dict[int, Image.Image] = {
        1: Image.open(DICE_FOLDER + "vanilla/dice-six-faces-one.png"),
        2: Image.open(DICE_FOLDER + "vanilla/dice-six-faces-two.png"),
        3: Image.open(DICE_FOLDER + "vanilla/dice-six-faces-three.png"),
        4: Image.open(DICE_FOLDER + "vanilla/dice-six-faces-four.png"),
        5: Image.open(DICE_FOLDER + "vanilla/dice-six-faces-five.png"),
        6: Image.open(DICE_FOLDER + "vanilla/dice-six-faces-six.png"),
        22: Image.open(DICE_FOLDER + "vanilla/dice-six-faces-two-alt.png"),
        33: Image.open(DICE_FOLDER + "vanilla/dice-six-faces-three-alt.png"),
        66: Image.open(DICE_FOLDER + "vanilla/dice-six-faces-six-alt.png"),
        # ======
        10: Image.open(DICE_FOLDER + "inverted/dice-six-faces-one-black.png"),
        20: Image.open(DICE_FOLDER + "inverted/dice-six-faces-two-black.png"),
        30: Image.open(DICE_FOLDER + "inverted/dice-six-faces-three-black.png"),
        40: Image.open(DICE_FOLDER + "inverted/dice-six-faces-four-black.png"),
        50: Image.open(DICE_FOLDER + "inverted/dice-six-faces-five-black.png"),
        60: Image.open(DICE_FOLDER + "inverted/dice-six-faces-six-black.png"),
        202: Image.open(DICE_FOLDER + "inverted/dice-six-faces-two-black-alt.png"),
        303: Image.open(DICE_FOLDER + "inverted/dice-six-faces-three-black-alt.png"),
        606: Image.open(DICE_FOLDER + "inverted/dice-six-faces-six-black-alt.png"),
    }
    
    @staticmethod
    def diceify(image: Image.Image, size: tuple[int, int] = (20, 20)) -> Image.Image:
        
        chunks = Diceify.chunk(image, size)
        diceified_chunks = [Diceify.closest_image(chunk, Diceify.DICE_IMG, size) for chunk in chunks]
        
        # Create a new blank image to paste the dice images into
        width, height = image.size
        new_image = Image.new('RGB', (width, height))
        
        # Paste each dice image back into the new image
        idx = 0
        for y in range(0, height, size[1]):
            for x in range(0, width, size[0]):
                if idx < len(diceified_chunks):
                    new_image.paste(diceified_chunks[idx], (x, y))
                    idx += 1
        
        return new_image



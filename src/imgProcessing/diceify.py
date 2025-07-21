from PIL import Image
import numpy as np

class DiceIfy:
    DICE_IMG = {
        1: Image.open("/workspaces/ObligatoryBadApple/textures/dice/dithered/dice-six-faces-one.png"),
        2: Image.open("/workspaces/ObligatoryBadApple/textures/dice/dithered/dice-six-faces-two.png"),
        3: Image.open("/workspaces/ObligatoryBadApple/textures/dice/dithered/dice-six-faces-three.png"),
        4: Image.open("/workspaces/ObligatoryBadApple/textures/dice/dithered/dice-six-faces-four.png"),
        5: Image.open("/workspaces/ObligatoryBadApple/textures/dice/dithered/dice-six-faces-five.png"),
        6: Image.open("/workspaces/ObligatoryBadApple/textures/dice/dithered/dice-six-faces-six.png"),
    }
    
    def __init__(self):
        pass
    
    @staticmethod
    def _chunk(image: Image.Image, chunk_size_px: int=16) -> list[Image.Image]:
        width, height = image.size
        chunks = []
        for y in range(0, height, chunk_size_px):
            for x in range(0, width, chunk_size_px):
                box = (x, y, min(x + chunk_size_px, width), min(y + chunk_size_px, height))
                chunks.append(image.crop(box))
        return chunks

    @staticmethod
    def _closest_dice(image: Image.Image) -> Image.Image:
        """
        Compare input grayscale image to all dice images and return the closest match.
        Uses Mean Squared Error to determine similarity.
        """
        # Convert input image to grayscale numpy array
        input_array = np.array(image.convert('L')).astype(np.float32)
        
        best_dice_img = DiceIfy.DICE_IMG[1]
        best_score = float('inf')
        
        # Compare with each dice image
        for dice_value, dice_img in DiceIfy.DICE_IMG.items():
            # Convert dice image to grayscale and resize to match input (16x16)
            dice_gray = dice_img.convert('L').resize((16, 16), Image.Resampling.LANCZOS)
            dice_array = np.array(dice_gray).astype(np.float32)
            
            # Calculate Mean Squared Error
            mse = np.mean((input_array - dice_array) ** 2)
            
            # Keep track of the best match
            if mse < best_score:
                best_score = mse
                best_dice_img = dice_img
        
        return best_dice_img



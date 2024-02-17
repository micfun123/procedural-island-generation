import numpy as np
import sys
from PIL import Image
from scipy.ndimage.interpolation import zoom

np.set_printoptions(threshold=sys.maxsize)

# Function to create a circular mask with variable island size
def circular_mask(shape, island_size):
    h, w = shape
    Y, X = np.ogrid[:h, :w]
    center_y, center_x = h / 2, w / 2
    mask = (Y - center_y) ** 2 + (X - center_x) ** 2 <= (min(h, w) / island_size) ** 2
    return mask

def generate_heightmap_and_save_image(image_name, island_size):
    # Generate your heightmap randomly
    arr = np.random.uniform(size=(40, 40))
    # Apply circular gradient multiplier (puts island center at image center) 
    circle_mask = circular_mask(arr.shape, island_size)
    arr *= circle_mask

    # Upscale the array (this step might not be needed depending on your actual data)
    arr = zoom(arr, 15)

    def height_to_color(height):
        water_threshold = 0.2
        sand_threshold = 0.4
        plains_threshold = 0.5
        forest_threshold = 0.7
        if height < water_threshold:
            return (0, 0, 255)  
        elif height < sand_threshold:
            return (255, 255, 102) 
        elif height < plains_threshold:
            return (51, 204, 51) 
        elif height < forest_threshold:
            return (34, 139, 34)
        else:
            return (192, 192, 192)

    # Create an empty image with the same size as the heightmap
    height, width = arr.shape
    img = Image.new('RGB', (width, height))

    # Iterate through the heightmap, setting pixels based on height
    for y in range(height):
        for x in range(width):
            height_value = arr[y, x]
            color = height_to_color(height_value)
            img.putpixel((x, y), color)

    
    img.save(image_name)
    #img.show()


#example
generate_heightmap_and_save_image("custom_heightmap_with_circle_gradient.png", island_size=3)


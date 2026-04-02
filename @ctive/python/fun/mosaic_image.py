ORIGINAL_IMAGE_PATH = "C:/Users/BenkeHargitai/Pictures/Renniversary/original_pictures/"
ORIGINAL_IMAGES = {
    "fun1.jpg": 7,
    "fun2.jpg": 6,
    "fun3.jpg": 5,
    "fun4.jpg": 4,
    "fun5.jpg": 3,
    "fun6.jpg": 2,
    "fun7.png": 1,
}  # List of original images to create mosaics from
SCALES = [2, 2, 2, 1.5, 1.5, 1, 1]
IMAGES_FOLDER_PATH = "C:/Users/BenkeHargitai/Pictures/Renniversary/pics/"

from datetime import datetime

OUTPUT_IMAGE_PATH = "C:/Users/BenkeHargitai/Pictures/Renniversary/mosaics_new/"

SECTION_SIZES = [100, 75, 50, 35, 20] # Different section sizes to create multiple mosaic images with varying levels of detail
RESOLUTION_SCALE = 1  # Scales the original image to increase the grid size (columns & rows). Increase for more detail!

# This function will create a mosaic image by dividing the original image into smaller sections and replacing each section with a corresponding image from the images folder.
def create_mosaic_image(size: int, image: tuple[str, int], scale: float):
    from PIL import Image, ImageOps
    import os

    size = int(size * scale)  # Scale the section size based on the provided scale factor

    # Load the original image, correct EXIF rotation, and scale it up to create more, smaller sections
    original_image = Image.open(f"{ORIGINAL_IMAGE_PATH}{image[0]}")
    original_image = ImageOps.exif_transpose(original_image).convert('RGB')
    new_size = (original_image.width * RESOLUTION_SCALE, original_image.height * RESOLUTION_SCALE)
    
    # PIL compatibility: Image.Resampling.LANCZOS for >= 9.1.0, Image.LANCZOS for older
    resample_filter = getattr(Image, 'Resampling', Image).LANCZOS
    original_image = original_image.resize(new_size, resample_filter)
    
    original_width, original_height = original_image.size

    # Create a new image for the mosaic
    mosaic_image = Image.new('RGB', (original_width, original_height))

    # Get the list of images in the images folder
    image_files = os.listdir(IMAGES_FOLDER_PATH)

    # Pre-process source images: compute average colors and pre-resize
    source_images = []
    print(f"Pre-processing {len(image_files)} source images...")
    for image_file in image_files:
        try:
            image_path = os.path.join(IMAGES_FOLDER_PATH, image_file)
            with Image.open(image_path) as img:
                img_rgb = img.convert('RGB')
                avg_color = img_rgb.resize((1, 1)).getpixel((0, 0))
                img_resized = img_rgb.resize((size, size))
                source_images.append({'color': avg_color, 'image': img_resized})
        except Exception as e:
            print(f"Could not load {image_file}: {e}")

    if not source_images:
        print("No valid source images found. Exiting.")
        return

    print("Building the mosaic...")
    # Loop through each section of the original image
    for y in range(0, original_height, size):
        for x in range(0, original_width, size):
            # Define the box for the current section
            box = (x, y, x + size, y + size)
            section = original_image.crop(box)

            # Calculate the average color of the section
            average_color = section.resize((1, 1)).getpixel((0, 0))

            # Find the best matching image from pre-processed images based on average color
            best_match = None
            best_match_diff = float('inf')

            for src in source_images:
                img_average_color = src['color']
                # Calculate color difference (squared Euclidean distance for speed)
                diff = sum((a - b) ** 2 for a, b in zip(average_color, img_average_color))

                if diff < best_match_diff:
                    best_match_diff = diff
                    best_match = src['image']

            # Paste the best matching image into the mosaic image
            if best_match:
                mosaic_image.paste(best_match, box)

    # Save the mosaic image
    mosaic_image.save(f"{OUTPUT_IMAGE_PATH}mosaic_{image[1]}_{size}px.jpg")
    print(f"Mosaic saved to {OUTPUT_IMAGE_PATH}")

if __name__ == "__main__":
    for (image, scale) in zip(ORIGINAL_IMAGES.items(), SCALES):
        # date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        for size in SECTION_SIZES:
            create_mosaic_image(size, image, scale)

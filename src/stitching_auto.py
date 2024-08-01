import cv2
import numpy as np
import os



def stitch_images(folder_path):
    # obtain image path
    image_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.jpg')]


    # define cropped area and position
    crop_width = int(1080 / len(image_paths))
    crop_height = 1080
    crop_x = 450
    crop_y = 0


    # create canvas
    canvas_width = crop_width * len(image_paths)
    canvas_height = crop_height
    canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.float32)

    # crop and stitch
    offset_x = 0
    for image_path in image_paths:

        image = cv2.imread(image_path).astype(np.float32)

        cropped_image = image[crop_y:crop_y + crop_height, crop_x:crop_x + crop_width]

        canvas[:, offset_x:offset_x + crop_width] += cropped_image

        # refresh stitching position
        offset_x += crop_width
        crop_x += crop_width

    canvas = canvas.astype(np.uint8)


    output_path = os.path.join(folder_path, "stitched_image.jpg")
    cv2.imwrite(output_path, canvas)


if __name__ == '__main__':
    folder_path = 'your_dir'
    stitch_images(folder_path)

try:
    import cv2
except:
    OPENCV = None
import os
from PIL import Image
import numpy as np
from pathlib import Path

def show_img(path):
    img = cv2.imread(path)
    cv2.imshow('show_img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def images_to_video(img_dir, save_path, fps=30):
    import imageio
    supported_formats = (".tif", ".png", ".jpg", ".jpeg")
    # Retrieve the paths of all eligible files in the image folder and sort them by file name
    images = [img for img in os.listdir(img_dir) if img.lower().endswith(supported_formats)]
    images.sort(key=lambda x: x)

    with imageio.get_writer(str(save_path), mode='I', fps=fps) as writer:
        for image in images:
            image_path = os.path.join(img_dir, image)
            img = imageio.imread(image_path)

            # 将图像写入视频
            writer.append_data(img)
    print(f"视频已保存到 {save_path}")


def video_to_images(path, save_path, img_format='jpg'):

    file_name = Path(path).stem

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    cap = cv2.VideoCapture(path)

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        output_image_path = os.path.join(save_path, f"{file_name}_{frame_count:04d}.{img_format}")

        cv2.imwrite(output_image_path, frame)

        frame_count += 1

    cap.release()
    print(f"视频已成功分解为{frame_count}张图片，保存于{save_path}。")


import os
import sys
import argparse
import random
import string
from PIL import Image, ImageOps
from tqdm import tqdm

def pad_image(image, target_ratio, bg_color):
    width, height = image.size
    current_ratio = width / height

    if current_ratio > target_ratio:
        new_height = int(width / target_ratio)
        new_size = (width, new_height)
        new_image = Image.new('RGB', new_size, bg_color)
        paste_y = (new_height - height) // 2
        new_image.paste(image, (0, paste_y))
    else:
        new_width = int(height * target_ratio)
        new_size = (new_width, height)
        new_image = Image.new('RGB', new_size, bg_color)
        paste_x = (new_width - width) // 2
        new_image.paste(image, (paste_x, 0))

    return new_image

def process_images(input_folder, ratio, bg_color, output_size):
    supported_formats = ('.jpg', '.jpeg', '.png', '.webp', '.avif')

    # 删除输入文件夹路径末尾的 "/"
    input_folder = input_folder.rstrip('/')

    # 创建输出文件夹
    random_suffix = ''.join(random.choices(string.ascii_lowercase, k=3))
    output_folder = f"{input_folder}_padded_{random_suffix}"
    os.makedirs(output_folder, exist_ok=True)

    # 获取所有支持的图片文件
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(supported_formats)]
    
    # 使用 tqdm 创建进度条
    for filename in tqdm(image_files, desc="Processing images", unit="image"):
        input_path = os.path.join(input_folder, filename)
        
        with Image.open(input_path) as img:
            # 纠正图片方向
            img = ImageOps.exif_transpose(img)
            
            padded_img = pad_image(img, ratio, bg_color)
            
            if output_size:
                padded_img = padded_img.resize(output_size, Image.LANCZOS)
            
            output_path = os.path.join(output_folder, filename)
            padded_img.save(output_path)
    
    print(f"Processed {len(image_files)} images")
    print(f"Output folder: {output_folder}")

def main():
    parser = argparse.ArgumentParser(description="Pad and resize images in a folder.")
    parser.add_argument("input_folder", help="Path to the input folder containing images")
    parser.add_argument("--ratio", type=float, default=1.0, help="Target aspect ratio (width/height)")
    parser.add_argument("--bg-color", default="#000000", help="Background color in hex format (e.g., #FFFFFF)")
    parser.add_argument("--output-size", type=int, nargs=2, metavar=('WIDTH', 'HEIGHT'), help="Output size after padding")

    args = parser.parse_args()

    if not os.path.isdir(args.input_folder):
        print(f"Error: {args.input_folder} is not a valid directory")
        sys.exit(1)

    try:
        bg_color = tuple(int(args.bg_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    except ValueError:
        print(f"Error: Invalid background color format. Use hex format (e.g., #FFFFFF)")
        sys.exit(1)

    process_images(args.input_folder, args.ratio, bg_color, args.output_size)

if __name__ == "__main__":
    main()
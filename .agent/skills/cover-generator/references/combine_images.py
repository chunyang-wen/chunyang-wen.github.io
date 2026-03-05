from PIL import Image
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("left_path", type=str)
parser.add_argument("right_path", type=str)
parser.add_argument("out_path", type=str)

args, _ = parser.parse_known_args()

left_img = Image.open(args.left_path)
right_img = Image.open(args.right_path)

if left_img.height != right_img.height:
    right_img = right_img.resize((int(right_img.width * left_img.height / right_img.height), left_img.height))

total_width = left_img.width + right_img.width
max_height = max(left_img.height, right_img.height)

new_im = Image.new('RGB', (total_width, max_height))
new_im.paste(left_img, (0, 0))
new_im.paste(right_img, (left_img.width, 0))

os.makedirs(os.path.dirname(args.out_path), exist_ok=True)
new_im.save(args.out_path)
print("Done combining images.")

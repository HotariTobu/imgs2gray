import argparse

from PIL import Image
from typing import List
from wcmatch import glob
from wcmatch.pathlib import Path


def process(input_file_path: Path, output_file_path: Path):
    """process a file

    Args:
        input_file_path (Path): path to input color image file
        output_dir_path (Path): path to output grayscale image file

    Returns:
        bool: True if succeed, otherwise False
    """

    try:
        with Image.open(input_file_path) as color_image:
            grayscale_image = color_image.convert("L")
            grayscale_image.save(output_file_path, color_image.format)

    except Exception as e:
        print(f"Failed to convert image file: {e}")

        return False

    return True


# Parse command-line parameters
parser = argparse.ArgumentParser(
    description="Convert color image files into grayscale image files"
)
parser.add_argument(
    "input_path", type=Path, help="path to the input image files or directory"
)
args = parser.parse_args()

input_path: Path = args.input_path
input_file_paths: List[Path] = []

if input_path.is_dir():
    for input_file_path in input_path.glob(
        "*.{png,jpg,jpeg,gif,bmp}", flags=glob.BRACE
    ):
        input_file_paths.append(input_file_path)
else:
    input_file_paths.append(input_path)

for input_file_path in input_file_paths:
    stem = input_file_path.stem
    output_file_path = input_file_path.with_stem(f"{stem}_gs")
    if output_file_path.exists():
        print("File already exists:", output_file_path)
        conf = input("Overwrite? (Y/n): ")
        if conf != "Y":
            continue

        output_file_path.unlink()

    process(input_file_path, output_file_path)

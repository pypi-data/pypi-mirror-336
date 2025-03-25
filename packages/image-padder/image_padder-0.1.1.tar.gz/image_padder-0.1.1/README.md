[![Publish Python Package](https://github.com/crapthings/py-image-padder/actions/workflows/workflow.yml/badge.svg)](https://github.com/crapthings/py-image-padder/actions/workflows/workflow.yml)

# Image Padder

Image Padder is a command-line tool for batch processing image files. It can pad images to a specified aspect ratio, resize them, and supports custom background colors.

## Features

- Supports jpg, jpeg, png, webp, and avif image formats
- Pads images to a specified aspect ratio (default 1:1)
- Customizable padding background color (default black)
- Optional image resizing
- Batch processing of entire folders
- Processed images saved in a new folder with original filenames

## Installation

Install Image Padder using pip:

```
pip install image-padder
```

## Usage

Basic usage:

```
image-padder <input_folder> [options]
```

Options:
- `--ratio`: Target aspect ratio (width/height). Default is 1.0 (square).
- `--bg-color`: Background color in hex format (e.g., #FFFFFF). Default is #000000 (black).
- `--output-size`: Output size after processing, specified as WIDTH HEIGHT.

Example:

```
image-padder /path/to/image/folder --ratio 1.5 --bg-color "#FFFFFF" --output-size 800 600
```

This command processes all supported images in `/path/to/image/folder`, padding them to a 3:2 aspect ratio with a white background, and resizing to 800x600 pixels.

## Output

Processed images are saved in a new folder at the same level as the input folder. The new folder is named:

```
{original_folder_name}_padded_{random_three_letters}
```

For example, if the input folder is "my_images", the output folder might be "my_images_padded_xyz".

## Development

To set up the development environment:

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/image-padder.git
   cd image-padder
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate
   ```

3. Install development dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Install the package in editable mode:
   ```
   pip install -e .
   ```

## Contributing

We welcome issue reports and pull requests. For major changes, please open an issue first to discuss what you'd like to change.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

# iphone-sync

An open source CLI script for Windows to backup photos from your iPhone

## Features

- Only sync new files
- File verification after copy

## Installation

You can install the package via pip:

```
pip install iphone-sync
```

## Usage

```
iphone-sync PATH_TO_OUTPUT_FOLDER
```

## Example

```
iphone-sync C:\Backup
```

```
🔍 Scanning folders...
📁 202503_a: 100%|██████████████████████| 33/33 [00:05<00:00,  6.47it/s]
✅ All Done!
```

## Future Plans

- Make opencv and pillow dependency optional

## License

This project is licensed under the terms of the MIT license.

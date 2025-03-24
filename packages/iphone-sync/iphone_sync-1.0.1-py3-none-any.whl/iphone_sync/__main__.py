import argparse
import os
from pathlib import Path
from typing import Any
from typing import cast

import win32com.client
from tqdm import tqdm

from iphone_sync.verify import verify_file


def copy_files_from_iphone(destination_folder: Path, verify: bool):
    shell = win32com.client.Dispatch("Shell.Application")

    # Step 1: Get "This PC"
    my_computer = shell.Namespace(17)  # CLSID for "This PC"

    # Step 2: Find the iPhone
    iphone = None
    for item in my_computer.Items():
        if "iPhone" in item.Name:
            iphone = item
            break
    else:
        print("❌ iPhone not found.")
        return

    # Step 3: Open iPhone Storage
    iphone_folder = iphone.GetFolder  # Get internal storage
    if not iphone_folder:
        print("❌ Unable to access iPhone storage.")
        return

    # Step 4: Find and Open "Internal Storage"
    internal_storage = None
    for item in iphone_folder.Items():
        if "Internal Storage" in item.Name:
            internal_storage = item.GetFolder
            break
    else:
        print("❌ Internal Storage not found.")
        return

    # Step 5: List all folders inside "Internal Storage"
    print("🔍 Scanning folders...")
    subfolders: list[tuple[Any, str]] = []
    for subfolder in internal_storage.Items():
        subfolder_name = cast(str, subfolder.Name)
        subfolder_obj = subfolder.GetFolder
        subfolders.append((subfolder_obj, subfolder_name))
    subfolders.sort(key=lambda i: i[1])

    # Step 6: List all files inside "Internal Storage"
    corrupt_file: str | None = None
    pbar = tqdm(subfolders)
    for subfolder_obj, subfolder_name in pbar:
        pbar.set_description(f"📁 {subfolder_name}")
        exist_count = 0
        total_count = 0
        to_copy: list[tuple[Any, str]] = []
        for file_obj in subfolder_obj.Items():
            file_name = cast(str, file_obj.Name)
            exists = (destination_folder / subfolder_name / file_name).exists()
            total_count += 1
            if exists:
                exist_count += 1
            else:
                to_copy.append((file_obj, file_name))

        # Copy the files to destination
        if to_copy:
            to_copy.sort(key=lambda i: i[1])
            pbar_1 = tqdm(to_copy, leave=False)
            for file_obj, file_name in pbar_1:
                pbar_1.set_description(f"💾 {file_name}")
                os.makedirs(destination_folder / subfolder_name, exist_ok=True)
                destination = shell.Namespace(
                    str(destination_folder / subfolder_name)
                )

                destination.CopyHere(file_obj)
                file = destination_folder / subfolder_name / file_name
                if verify:
                    if verify_file(file):
                        corrupt_file = f"{subfolder_name}/{file_name}"
                        try:
                            os.remove(file)
                        except FileNotFoundError:
                            pass
                        break
        if corrupt_file:
            break

    if corrupt_file:
        print(f"❌ Corrupt file found: {corrupt_file}")
    else:
        print("✅ All Done!")


def main():
    # Initialize the parser
    parser = argparse.ArgumentParser(
        description="Parse destination folder argument"
    )
    # Add the destination folder argument
    parser.add_argument(
        "destination_folder",
        type=str,
        help="The destination folder path",
    )
    parser.add_argument(
        "--no-verify",
        action="store_true",
        help="Whether to verify files after copying",
    )
    # Parse the arguments
    args = parser.parse_args()
    destination_folder = Path(args.destination_folder).absolute()
    copy_files_from_iphone(destination_folder, not args.no_verify)


if __name__ == "__main__":
    main()

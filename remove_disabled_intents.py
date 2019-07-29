from pathlib import Path
import json
import tempfile
import zipfile
import shutil
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove disabled intents from a Dialogflow agent zip.")
    parser.add_argument("zip_in", help="Path to input Dialogflow agent zip")
    parser.add_argument("zip_out", help="Output path for modified zip file.")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        with zipfile.ZipFile(args.zip_in, "r") as zip_ref:
            zip_ref.extractall(temp_dir)

        print("Disabled intents:")
        for file in temp_dir.glob("**/intents/*"):
            intent = json.load(file.open('r'))
            if "priority" in intent and intent["priority"] == -1:
                print(intent["name"])
                file.unlink()

        if args.zip_out:
            shutil.make_archive(Path(args.zip_out).stem, 'zip', temp_dir)

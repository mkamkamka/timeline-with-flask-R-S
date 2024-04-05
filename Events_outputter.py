import os
from PIL import Image
import piexif
import json


def convert_date_format(date_str):
    """Convert date string from 'YYYY:MM:DD HH:MM:SS' to the specified JSON format."""
    date_parts = date_str.split(" ")[0].split(":")  # Splits the date string and takes the date part
    return {
        "year": date_parts[0],
        "month": date_parts[1],
        "day": date_parts[2]
    }


def extract_metadata_and_format_date(image_path, filename):
    """Extract date and format it according to the specified structure, including the filename in 'media'."""
    try:
        img = Image.open(image_path)
        exif_data = piexif.load(img.info['exif'])

        if piexif.ImageIFD.DateTime in exif_data['0th']:
            date_taken = exif_data['0th'][piexif.ImageIFD.DateTime].decode('utf-8')
            formatted_date = convert_date_format(date_taken)
            return {
                "start_date": formatted_date,
                "media": {"url": "static/image_png/" + filename[0:-4] + "png"},
                "text": {}
            }
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
    return None


def process_images_in_directory(directory_path):
    """Process all images in the given directory and compile their data under 'events', including filenames in 'media'."""
    events = []
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(directory_path, filename)
            event_data = extract_metadata_and_format_date(image_path, filename)
            if event_data:
                events.append(event_data)

    # Sort events based on start_date
    events.sort(key=lambda x: (x["start_date"]["year"], x["start_date"]["month"], x["start_date"]["day"]))

    overall_structure = {"events": events}
    return overall_structure


# Example usage
directory_path = "static/img/"
data = process_images_in_directory(directory_path)
print(json.dumps(data, indent=4))

# Optionally, save to a JSON file
with open("static/data/events.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

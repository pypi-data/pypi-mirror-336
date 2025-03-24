import os
import re
import requests

API_URL = "http://commit-svc.aiplatform/publish"

def extract_default_image():
    """Extracts the image name from KERNEL_IMAGE if available and formats it."""
    kernel_image = os.getenv("KERNEL_IMAGE", "admin/base_kernel_gpu@sha256:3024")
    image_name = kernel_image.split("/")[1].split("@")[0]  # Extract "base_kernel_gpu"
    return format_name(image_name)

def format_name(name):
    """Ensure the name is lowercase and contains only valid characters."""
    return re.sub(r'[^a-z0-9_]', '_', name.lower())

def validate_image_name(image_name):
    """Validate image name format: lowercase, only alphanumeric and underscores."""
    return bool(re.fullmatch(r'[a-z0-9_]+', image_name))

def validate_tags(tags):
    """Ensure tags are non-empty, lowercase, contain only valid characters, and no spaces."""
    tag_list = [format_name(tag.strip()) for tag in tags.split(";") if tag.strip()]
    return all(re.fullmatch(r'[a-z0-9_]+', tag) for tag in tag_list) and len(tag_list) > 0

def get_username():
    """Retrieve the username from the environment variable KERNEL_AP_USER or prompt for it."""
    username = os.getenv("KERNEL_AP_USER")
    if not username:
        username = input("Enter username (KERNEL_AP_USER not set): ").strip()
    return format_name(username)

def publish_env():
    """Handles the 'aap_utils publish env' command and sends a POST request."""
    username = get_username()
    default_image = extract_default_image()
    
    while True:
        image_name = input(f"Enter image name [{default_image}]: ").strip() or default_image
        image_name = format_name(image_name)
        if validate_image_name(image_name):
            break
        print("Invalid image name. Use only lowercase letters, numbers, or underscores (_).")

    while True:
        tags = input("Enter tags (separated by ';'): ").strip()
        formatted_tags = [format_name(tag) for tag in tags.split(";") if tag.strip()]
        if validate_tags(";".join(formatted_tags)):
            break
        print("Invalid tags. Each tag must be lowercase, contain only letters, numbers, or underscores (_), and no spaces.")

    data = {
        "username": username,
        "imagename": image_name,
        "tags": formatted_tags
    }

    print(f"Publishing environment: {data}")

    try:
        response = requests.post(API_URL, json=data)
        if response.status_code == 200:
            print("✅ Successfully published the environment!")
        else:
            print(f"❌ Failed to publish. Server responded with: {response.status_code}, {response.text}")
    except requests.RequestException as e:
        print(f"❌ Error connecting to the server: {e}")

def main():
    import sys
    if len(sys.argv) > 2 and sys.argv[1] == "publish" and sys.argv[2] == "env":
        publish_env()
    else:
        print("Usage: aap_utils publish env")

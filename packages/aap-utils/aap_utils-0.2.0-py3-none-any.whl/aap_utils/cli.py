import os

def extract_default_image():
    """Extracts the image name from KERNEL_IMAGE if available."""
    kernel_image = os.getenv("KERNEL_IMAGE", "admin/base_kernel_gpu@sha256:3024")
    return kernel_image.split("/")[1].split("@")[0]  # Extract "base_kernel_gpu"

def validate_image_name(image_name):
    """Validate image name format."""
    return bool(image_name and image_name.strip())

def validate_tags(tags):
    """Ensure tags are non-empty and separated by semicolon."""
    tag_list = [tag.strip() for tag in tags.split(";") if tag.strip()]
    return len(tag_list) > 0

def publish_env():
    """Handles the 'aap_utils publish env' command."""
    default_image = extract_default_image()
    
    while True:
        image_name = input(f"Enter image name [{default_image}]: ").strip() or default_image
        if validate_image_name(image_name):
            break
        print("Invalid image name. Please try again.")

    while True:
        tags = input("Enter tags (separated by ';'): ").strip()
        if validate_tags(tags):
            break
        print("Invalid tags. Please enter at least one tag, separated by ';'.")

    print(f"Publishing environment with Image: {image_name}, Tags: {tags}")

def main():
    import sys
    if len(sys.argv) > 2 and sys.argv[1] == "publish" and sys.argv[2] == "env":
        publish_env()
    else:
        print("Usage: aap_utils publish env")

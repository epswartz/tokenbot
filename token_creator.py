import face_recognition
import requests
from PIL import Image, ImageDraw, ImageFilter


def mask_circle_transparent(pil_img, blur_radius, offset=0):
    """
    Given an image, turns that image into a circle around it's center with transparency around it.
    """
    offset = blur_radius * 2 + offset
    mask = Image.new("L", pil_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((offset, offset, pil_img.size[0] - offset, pil_img.size[1] - offset), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

    result = pil_img.copy()
    result.putalpha(mask)

    return result

def create_token(url):
    """
    Given a url string, downloads the image and attempts to crop it around the face.
    Even if there are multiple faces, returns only one of them.

    Returns the image as a PIL image, or a string if there was a problem.
    """

    # For now, only circular borders are supported.
    border = Image.open('./images/borders/circle.png')

    # Download the image
    r = requests.get(url, stream = True)

    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        image = face_recognition.load_image_file(r.raw)
        face_locations = face_recognition.face_locations(image)
        if len(face_locations) > 0:
            face = face_locations[0]
        else:
            # Retry with CNN
            face_locations = face_recognition.face_locations(image, model="CNN")
            if len(face_locations > 0):
                face = face_locations[0]
            else:
                return "No faces found in image."

        face_arr = image[face[0]:face[2],face[3]:face[1]]
        face_img_sq = Image.fromarray(face_arr)
        face_img_ci = mask_circle_transparent(face_img_sq, 1)
        face_img_ci = face_img_ci.resize(border.size)
        face_img_ci.paste(border, (0,0), border)
        return face_img_ci
    else:
        return f"Error when downloading image. Recieved status code: {r.status_code}"




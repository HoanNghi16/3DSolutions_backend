from cloudinary import uploader

def product_image_upload(image):
    result = uploader.upload(image)
    return result
import cloudinary.uploader
import uuid

def upload_image(file, folder):
    public_id = str(uuid.uuid4())
    result = cloudinary.uploader.upload(
        file = file,
        public_id=public_id,
        folder = folder,
        resource_type="image",
    )
    return {
        "url": result["secure_url"],
        "public_id": public_id,
    }
def delete_image(public_id):
    return cloudinary.uploader.destroy(public_id = str(public_id))
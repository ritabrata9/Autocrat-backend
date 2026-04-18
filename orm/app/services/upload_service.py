import cloudinary.uploader

def upload_profile_pic(file, user_id):
    result = cloudinary.uploader.upload(
        file,
        folder="profile_pics",
        public_id=f"user_{user_id}",
        overwrite=True
    )

    url = result["secure_url"]

    return url.replace(
        "/upload/",
        "/upload/w_200,h_200,c_fill,q_auto,f_auto/"
    )
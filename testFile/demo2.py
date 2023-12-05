from deepface import DeepFace
import tempfile

# test
Owner_file_path = "madhavi.jpg"
with open(Owner_file_path, "rb") as img_file:
    Owner_file = img_file.read()

img2_path = "madhavi.jpg"

model_name = "Facenet"
detector_backend = "opencv"
enforce_detection = True
distance_metric = "cosine"
align = True

with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_img:
    temp_img.write(Owner_file)
    temp_img_path = temp_img.name

resp = DeepFace.verify(
    img1_path=temp_img_path,
    img2_path=img2_path,
    model_name=model_name,
    detector_backend=detector_backend,
    enforce_detection=enforce_detection,
    distance_metric=distance_metric,
    align=align,
)
print(resp)

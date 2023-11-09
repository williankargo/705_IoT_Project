# ways to install deepface on Mac M1:
# https://github.com/serengil/deepface/issues/592
# numpy problem: https://stackoverflow.com/questions/50311096/attributeerror-module-numpy-has-no-attribute-version
from deepface import DeepFace

# test
img1_path = "reference.jpg"
img2_path = "reference.jpg"

model_name = "Facenet"

resp = DeepFace.verify(img1_path=img1_path, img2_path=img2_path, model_name=model_name)
print(resp)

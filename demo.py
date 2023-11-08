import threading

# pip3 install opencv-python
import cv2

# git clone https://github.com/serengil/deepface.git                                                                                         22:35:28
# cd deepface
# pip install -e .
from deepface import DeepFace

# # To Capture Face
# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


# # Function to see face is match or not
# face_match = False
# reference_img = cv2.imread("reference.jpg")
# def check_face(frame):
#     global face_match
#     try:
#         if DeepFace.verify(frame, reference_img.copy())["verified"]:
#             face_match = True
#         else:
#             face_match = False
#     except ValueError:
#         face_match = False


# # While loop to detect face.
# counter = 0
# while True:

#     ret, frame = cap.read()
#     if ret:
#         if counter % 30 == 0:
#             try:
#                 threading.Thread(target=check_face, args=(frame.copy(),)).start()
#             except ValueError:
#                 pass
#         counter += 1

#         if face_match:
#             cv2.putText(frame, "MATCH", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
#         else:
#             cv2.putText(frame, "NO MATCH", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

#         cv2.imshow("video", frame)

#     key = cv2.waitKey(1)
#     if key == ord("q"):
#         break

# cv2.destroyAllWindows()

# test
img1_path = "reference.jpg"
img2_path = "reference.jpg"

model_name = "Facenet"

resp = DeepFace.verify(img1_path=img1_path, img2_path=img2_path, model_name=model_name)
print(resp)

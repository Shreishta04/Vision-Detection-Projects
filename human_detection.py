import mediapipe as mp
import cv2
import winsound
import time
import smtplib
import os
from email.message import EmailMessage

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

captured = False
human_detected = False
last_capture_time = 0
capture_interval = 10

FROM_EMAIL = "shreishtamanoj04@gmail.com"
TO_EMAIL = "mca2456@rajagiri.edu"
APP_PASSWORD = "kbml icpt hexc gtqy"

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)
    current_time = time.time()
    if results.pose_landmarks:
        print("Human Detected.")
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        winsound.Beep(1000,100)
        human_detected = True

        if not captured and human_detected:
            timestamp = int(time.time())
            filename = f"human_detected_{timestamp}.png"
            cv2.imwrite(filename, frame)
            print(f"Screenshot saved as {filename}")
            captured = True

            msg = EmailMessage()
            msg["Subject"] = "📷 Human Detected - Screenshot Attached"
            msg["From"] = FROM_EMAIL
            msg["To"] = TO_EMAIL
            msg.set_content("A screenshot was captured upon detecting a human. Please find it attached.")

            with open(filename, "rb") as f:
                file_data = f.read()
                file_name = os.path.basename(filename)
                msg.add_attachment(file_data, maintype="image", subtype="png", filename=file_name)

            try:
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                    smtp.login(FROM_EMAIL, APP_PASSWORD)
                    smtp.send_message(msg)
                print("✅ Email sent successfully!")
            except Exception as e:
                print(f"❌ Failed to send email: {e}")

    else:
        print("Not detected.")
        human_detected = False
        captured = False

    #Send email with photo of the captured image, smtp , from and to email and from mail password
    cv2.imshow('Pose Estimation', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
import os
import cv2
import csv


def TakeImage(l1, l2, haarcasecade_path, trainimage_path, message, err_screen, text_to_speech):
    if (l1 == "") and (l2 == ""):
        t = 'Please Enter your Enrollment Number and Name.'
        text_to_speech(t)
    elif l1 == '':
        t = 'Please Enter your Enrollment Number.'
        text_to_speech(t)
    elif l2 == "":
        t = 'Please Enter your Name.'
        text_to_speech(t)
    else:
        try:
            cam = cv2.VideoCapture(0)
            detector = cv2.CascadeClassifier(haarcasecade_path)
            Enrollment = l1
            Name = l2
            sampleNum = 0
            directory = f"{Enrollment}_{Name}"
            path = os.path.join(trainimage_path, directory)
            # Create directory if it doesn't exist
            os.makedirs(path, exist_ok=True)

            while True:
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    sampleNum += 1
                    # Save the captured image
                    image_path = os.path.join(path, f"{Name}_{Enrollment}_{sampleNum}.jpg")
                    cv2.imwrite(image_path, gray[y:y + h, x:x + w])
                    cv2.imshow("Frame", img)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
                elif sampleNum >= 50:
                    break

            cam.release()
            cv2.destroyAllWindows()

            # Add student details to CSV
            row = [Enrollment, Name]
            with open("StudentDetails/studentdetails.csv", "a+", newline="") as csvFile:
                writer = csv.writer(csvFile, delimiter=",")
                writer.writerow(row)

            res = f"Images Saved for ER No: {Enrollment} Name: {Name}"
            message.configure(text=res)
            text_to_speech(res)

        except FileExistsError:
            F = "Student Data already exists"
            text_to_speech(F)

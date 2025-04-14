import os
import cv2
import csv
import sys
import time
import datetime
import subprocess
import pandas as pd
import customtkinter as ctk


haarcasecade_path = "/Users/yashharitash/Desktop/Attendance-Management-system-using-face-recognition/haarcascade_frontalface_default.xml"
trainimagelabel_path = "/Users/yashharitash/Desktop/Attendance-Management-system-using-face-recognition/TrainingImageLabel/Trainner.yml"
trainimage_path = "TrainingImage/Users/yashharitash/Desktop/Attendance-Management-system-using-face-recognition/TrainingImage"
studentdetail_path = "/Users/yashharitash/Desktop/Attendance-Management-system-using-face-recognition/StudentDetails/studentdetails.csv"
attendance_path = "/Users/yashharitash/Desktop/Attendance-Management-system-using-face-recognition/Attendance"

def subjectChoose(text_to_speech):
    def FillAttendance():
        sub = subject_entry.get()
        now = time.time()
        future = now + 20

        if not sub:
            text_to_speech("Please enter the subject name!")
            notification_label.configure(
                text="Please enter the subject name!",
                fg_color="#e74c3c",
                text_color="white"
            )
            return

        try:
            # Initialize face recognizer
            recognizer = cv2.face.LBPHFaceRecognizer_create()

            try:
                recognizer.read(trainimagelabel_path)
            except:
                error_msg = "Model not found, please train the model first"
                notification_label.configure(
                    text=error_msg,
                    fg_color="#e74c3c",
                    text_color="white"
                )
                text_to_speech(error_msg)
                return

            # Load face detection classifier
            face_cascade = cv2.CascadeClassifier(haarcasecade_path)
            df = pd.read_csv(studentdetail_path)

            # Initialize camera
            cam = cv2.VideoCapture(0)
            if not cam.isOpened():
                error_msg = "Error: Could not open camera."
                notification_label.configure(
                    text=error_msg,
                    fg_color="#e74c3c",
                    text_color="white"
                )
                text_to_speech(error_msg)
                return

            # Prepare attendance tracking
            col_names = ["Enrollment", "Name"]
            attendance = pd.DataFrame(columns=col_names)
            font = cv2.FONT_HERSHEY_SIMPLEX

            while True:
                ret, frame = cam.read()
                if not ret:
                    print("Failed to grab frame")
                    break

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.2, 5)

                for (x, y, w, h) in faces:
                    Id, conf = recognizer.predict(gray[y:y + h, x:x + w])

                    if conf < 37:
                        student_name = df.loc[df["Enrollment"] == Id]["Name"].values[0]
                        student_id = f"{Id}-{student_name}"

                        # Record attendance
                        ts = time.time()
                        date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                        timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")

                        attendance.loc[len(attendance)] = [Id, student_name]
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
                        cv2.putText(frame, student_id, (x, y - 10), font, 0.9, (0, 255, 0), 2)
                    else:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                        cv2.putText(frame, "Unknown", (x, y - 10), font, 0.9, (0, 0, 255), 2)

                if time.time() > future:
                    break

                cv2.imshow("Attendance System - Press ESC to exit", frame)
                if cv2.waitKey(1) == 27:
                    break

            # Save attendance data
            attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
            if not attendance.empty:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                Hour, Minute, Second = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S").split(":")

                subject_path = os.path.join(attendance_path, sub)
                os.makedirs(subject_path, exist_ok=True)

                filename = f"{sub}_{date}_{Hour}-{Minute}-{Second}.csv"
                filepath = os.path.join(subject_path, filename)
                attendance.to_csv(filepath, index=False)

                success_msg = f"Attendance recorded successfully for {sub}"
                notification_label.configure(
                    text=success_msg,
                    fg_color="#27ae60",
                    text_color="white"
                )
                text_to_speech(success_msg)

                # Show attendance in a new window
                show_attendance_table(sub, filepath)
            else:
                notification_label.configure(
                    text="No attendance recorded!",
                    fg_color="#e74c3c",
                    text_color="white"
                )

            cam.release()
            cv2.destroyAllWindows()

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            notification_label.configure(
                text=error_msg,
                fg_color="#e74c3c",
                text_color="white"
            )
            text_to_speech(error_msg)
            print(f"Error: {e}")

    def show_attendance_table(subject, filepath):
        table_window = ctk.CTkToplevel()
        table_window.title(f"Attendance for {subject}")
        table_window.geometry("800x600")

        # Create a frame for the table
        table_frame = ctk.CTkFrame(table_window)
        table_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Add title
        title_label = ctk.CTkLabel(
            table_frame,
            text=f"Attendance Sheet - {subject}",
            font=("Roboto", 20, "bold")
        )
        title_label.pack(pady=10)

        # Create a scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(table_frame)
        scroll_frame.pack(fill="both", expand=True)

        # Read CSV and display data
        try:
            with open(filepath, newline="") as file:
                reader = csv.reader(file)
                headers = next(reader)

                # Create header row
                header_frame = ctk.CTkFrame(scroll_frame)
                header_frame.pack(fill="x")

                for i, header in enumerate(headers):
                    ctk.CTkLabel(
                        header_frame,
                        text=header,
                        font=("Roboto", 14, "bold"),
                        width=150,
                        height=30,
                        fg_color="#3498db",
                        corner_radius=5
                    ).grid(row=0, column=i, padx=5, pady=2)

                # Create data rows
                for row_idx, row in enumerate(reader, start=1):
                    row_frame = ctk.CTkFrame(scroll_frame)
                    row_frame.pack(fill="x")

                    for col_idx, cell in enumerate(row):
                        bg_color = "#f8f9fa" if row_idx % 2 == 0 else "#ffffff"
                        ctk.CTkLabel(
                            row_frame,
                            text=cell,
                            font=("Roboto", 12),
                            width=150,
                            height=30,
                            fg_color=bg_color,
                            corner_radius=5,
                            text_color="#2c3e50"
                        ).grid(row=0, column=col_idx, padx=5, pady=2)

        except Exception as e:
            ctk.CTkLabel(
                scroll_frame,
                text=f"Error loading attendance data: {str(e)}",
                text_color="#e74c3c"
            ).pack()

    def open_attendance_folder():
        sub = subject_entry.get()
        if not sub:
            text_to_speech("Please enter the subject name!")
            notification_label.configure(
                text="Please enter the subject name!",
                fg_color="#e74c3c",
                text_color="white"
            )
            return

        folder_path = os.path.join(attendance_path, sub)
        if os.path.exists(folder_path):
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(folder_path)
                elif os.name == 'posix':  # macOS/Linux
                    subprocess.run(['open', folder_path] if sys.platform == 'darwin' else ['xdg-open', folder_path])
            except Exception as e:
                notification_label.configure(
                    text=f"Error opening folder: {str(e)}",
                    fg_color="#e74c3c",
                    text_color="white"
                )
        else:
            notification_label.configure(
                text=f"No attendance records found for {sub}",
                fg_color="#e74c3c",
                text_color="white"
            )

    # Create the subject window
    subject_window = ctk.CTkToplevel()
    subject_window.title("Select Subject")
    subject_window.geometry("600x400")
    subject_window.resizable(False, False)

    # Main frame
    main_frame = ctk.CTkFrame(subject_window)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Title
    title_label = ctk.CTkLabel(
        main_frame,
        text="Enter Subject Details",
        font=("Roboto", 24, "bold"),
        text_color="#2c3e50"
    )
    title_label.pack(pady=10)

    # Subject entry
    subject_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    subject_frame.pack(pady=20)

    ctk.CTkLabel(
        subject_frame,
        text="Subject Name:",
        font=("Roboto", 16)
    ).grid(row=0, column=0, padx=10, pady=10)

    subject_entry = ctk.CTkEntry(
        subject_frame,
        placeholder_text="e.g. Mathematics",
        font=("Roboto", 16),
        width=250,
        height=40
    )
    subject_entry.grid(row=0, column=1, padx=10, pady=10)

    # Buttons frame
    buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    buttons_frame.pack(pady=20)

    fill_button = ctk.CTkButton(
        buttons_frame,
        text="Take Attendance",
        command=FillAttendance,
        font=("Roboto", 16),
        width=180,
        height=40,
        fg_color="#27ae60",
        hover_color="#219653"
    )
    fill_button.pack(side="left", padx=10)

    sheets_button = ctk.CTkButton(
        buttons_frame,
        text="View Sheets",
        command=open_attendance_folder,
        font=("Roboto", 16),
        width=180,
        height=40,
        fg_color="#3498db",
        hover_color="#2980b9"
    )
    sheets_button.pack(side="left", padx=10)

    # Notification area
    notification_label = ctk.CTkLabel(
        main_frame,
        text="",
        font=("Roboto", 14),
        width=400,
        height=40,
        corner_radius=5
    )
    notification_label.pack(pady=20)
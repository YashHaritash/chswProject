import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import os
import pyttsx3

# Project modules
import show_attendance
import takeImage
import trainImage
import automaticAttedance

ctk.set_appearance_mode("light")  # Light or dark mode
ctk.set_default_color_theme("blue")  # Theme: blue, green, dark-blue


class FaceMarkApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.setup_resources()
        self.configure_window()
        self.create_icons()
        self.build_ui()

    def setup_resources(self):
        self.engine = pyttsx3.init()
        self.haarcascade_path = "haarcascade_frontalface_default.xml"
        self.trainimagelabel_path = "./TrainingImageLabel/Trainner.yml"
        self.trainimage_path = "./TrainingImage"
        if not os.path.exists(self.trainimage_path):
            os.makedirs(self.trainimage_path)

    def configure_window(self):
        self.root.title("FaceMark - Intelligent Attendance System")
        self.root.geometry("1200x750")
        self.root.minsize(1100, 700)

    def create_icons(self):
        # Load and resize icons (replace these with actual high-quality icons)
        self.logo_img = ctk.CTkImage(Image.open("UI_Image/0001.png").resize((60, 60)))
        self.register_icon = ctk.CTkImage(Image.open("UI_Image/register.png").resize((100, 100)))
        self.attendance_icon = ctk.CTkImage(Image.open("UI_Image/attendance.png").resize((100, 100)))
        self.verify_icon = ctk.CTkImage(Image.open("UI_Image/verifyy.png").resize((100, 100)))
        self.exit_icon = ctk.CTkImage(Image.open("UI_Image/exit.png").resize((20, 20)))

    def text_to_speech(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def build_ui(self):
        # Create main container
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header Section
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.header_frame.pack(fill=tk.X, pady=(0, 20))

        # Logo and Title
        ctk.CTkLabel(
            self.header_frame,
            image=self.logo_img,
            text=""
        ).pack(side=tk.LEFT, padx=10)

        ctk.CTkLabel(
            self.header_frame,
            text="FaceMark",
            font=("Roboto", 36, "bold"),
            text_color="#2b5876"
        ).pack(side=tk.LEFT, padx=10)

        # Welcome Message
        ctk.CTkLabel(
            self.main_frame,
            text="AI-Powered Attendance System",
            font=("Roboto", 24),
            text_color="#4e4376"
        ).pack(pady=(0, 40))

        # Features Grid
        self.features_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.features_frame.pack(fill=tk.BOTH, expand=True)

        # Feature Cards
        self.create_feature_card(
            self.features_frame,
            self.register_icon,
            "New Registration",
            "Register new students with facial recognition",
            self.show_registration_window,
            0, 0
        )

        self.create_feature_card(
            self.features_frame,
            self.verify_icon,
            "Take Attendance",
            "Automatically mark attendance using face detection",
            lambda: automaticAttedance.subjectChoose(self.text_to_speech),
            0, 1
        )

        self.create_feature_card(
            self.features_frame,
            self.attendance_icon,
            "View Records",
            "Access and manage attendance records",
            lambda: show_attendance.subjectchoose(),  # ✅ Fixed
            0, 2
        )

        # Exit Button
        ctk.CTkButton(
            self.main_frame,
            text=" Exit System",
            image=self.exit_icon,
            command=self.root.destroy,
            font=("Roboto", 14),
            fg_color="#e74c3c",
            hover_color="#c0392b",
            width=200,
            height=40,
            corner_radius=10
        ).pack(pady=40)

    def create_feature_card(self, parent, icon, title, description, command, row, col):
        card = ctk.CTkFrame(
            parent,
            width=300,
            height=350,
            corner_radius=15,
            border_width=2,
            border_color="#e0e0e0"
        )
        card.grid(row=row, column=col, padx=20, pady=10, sticky="nsew")
        card.grid_propagate(False)

        # Make the card columns expand equally
        parent.grid_columnconfigure(col, weight=1)

        # Card content
        ctk.CTkLabel(
            card,
            image=icon,
            text=""
        ).pack(pady=(30, 10))

        ctk.CTkLabel(
            card,
            text=title,
            font=("Roboto", 20, "bold"),
            text_color="#2c3e50"
        ).pack(pady=(0, 10))

        ctk.CTkLabel(
            card,
            text=description,
            font=("Roboto", 14),
            text_color="#7f8c8d",
            wraplength=250
        ).pack(pady=(0, 20), padx=20)

        ctk.CTkButton(
            card,
            text="Start",
            command=command,
            font=("Roboto", 14),
            width=120,
            height=35,
            corner_radius=8,
            fg_color="#3498db",
            hover_color="#2980b9"
        ).pack(pady=(0, 20))

    def show_registration_window(self):
        window = ctk.CTkToplevel(self.root)
        window.title("Student Registration")
        window.geometry("700x550")
        window.resizable(False, False)

        # Header
        ctk.CTkLabel(
            window,
            text="Register New Student",
            font=("Roboto", 24, "bold"),
            text_color="#2c3e50"
        ).pack(pady=20)

        # Form Frame
        form_frame = ctk.CTkFrame(window, fg_color="transparent")
        form_frame.pack(pady=10, padx=30, fill=tk.BOTH)

        # Form Fields
        ctk.CTkLabel(
            form_frame,
            text="Enrollment Number:",
            font=("Roboto", 14),
            anchor="w"
        ).pack(fill=tk.X, pady=(10, 5))

        enrollment_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Enter enrollment number",
            font=("Roboto", 14),
            height=40,
            corner_radius=8
        )
        enrollment_entry.pack(fill=tk.X, pady=(0, 15))

        ctk.CTkLabel(
            form_frame,
            text="Full Name:",
            font=("Roboto", 14),
            anchor="w"
        ).pack(fill=tk.X, pady=(10, 5))

        name_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Enter student name",
            font=("Roboto", 14),
            height=40,
            corner_radius=8
        )
        name_entry.pack(fill=tk.X, pady=(0, 20))

        # Notification Area
        notification_label = ctk.CTkLabel(
            form_frame,
            text="",
            font=("Roboto", 12),
            text_color="#e74c3c",
            height=30,
            corner_radius=5,
            fg_color="#ffebee"
        )
        notification_label.pack(fill=tk.X, pady=(0, 20))

        # Action Buttons
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(fill=tk.X, pady=(10, 0))

        ctk.CTkButton(
            button_frame,
            text="Capture Images",
            command=lambda: self.take_student_images(
                enrollment_entry.get(),
                name_entry.get(),
                notification_label
            ),
            font=("Roboto", 14),
            height=40,
            corner_radius=8,
            fg_color="#27ae60",
            hover_color="#219653"
        ).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        ctk.CTkButton(
            button_frame,
            text="Train Model",
            command=lambda: self.train_model(notification_label),
            font=("Roboto", 14),
            height=40,
            corner_radius=8,
            fg_color="#9b59b6",
            hover_color="#8e44ad"
        ).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

    def take_student_images(self, enrollment, name, notification_label):
        if not enrollment or not name:
            notification_label.configure(
                text="Error: Both enrollment and name are required!",
                fg_color="#ffebee"
            )
            return

        takeImage.TakeImage(
            enrollment,
            name,
            self.haarcascade_path,
            self.trainimage_path,
            notification_label,
            self.show_error_message,
            self.text_to_speech
        )

    def train_model(self, notification_label):
        trainImage.TrainImage(
            self.haarcascade_path,
            self.trainimage_path,
            self.trainimagelabel_path,
            notification_label,
            self.text_to_speech
        )

    def show_error_message(self, message):
        error_window = ctk.CTkToplevel(self.root)
        error_window.title("Error")
        error_window.geometry("400x200")
        error_window.resizable(False, False)

        ctk.CTkLabel(
            error_window,
            text=message,
            font=("Roboto", 16),
            text_color="#ffffff",
            wraplength=350,
            justify="center",
            fg_color="#e74c3c",
            corner_radius=10
        ).pack(pady=30, padx=20, fill=tk.BOTH, expand=True)

        ctk.CTkButton(
            error_window,
            text="OK",
            command=error_window.destroy,
            font=("Roboto", 14),
            width=100,
            height=35,
            corner_radius=8,
            fg_color="#ffffff",
            text_color="#2c3e50",
            hover_color="#ecf0f1"
        ).pack(pady=(0, 20))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = FaceMarkApp()
    app.run()
import pandas as pd
from glob import glob
import os
import customtkinter as ctk
import csv
import subprocess
import re
import sys
from tkinter import messagebox
from datetime import datetime


def subjectchoose():
    def notify(msg, color="#3498db"):
        notification_label.configure(
            text=msg,
            fg_color=color,
            text_color="white"
        )

    def calculate_attendance():
        subject = subject_entry.get().strip()
        if not subject:
            notify("Please enter the subject name", "#e74c3c")
            return

        try:
            folder_path = os.path.join("Attendance", subject)
            csv_files = glob(os.path.join(folder_path, f"{subject}_*.csv"))
            if not csv_files:
                raise FileNotFoundError(f"No attendance records found for {subject}")

            attendance_records = {}

            for f in csv_files:
                try:
                    df = pd.read_csv(f)
                    if "Enrollment" not in df.columns or "Name" not in df.columns:
                        raise ValueError(f"Invalid format in {os.path.basename(f)}")

                    match = re.search(r"\d{4}-\d{2}-\d{2}", os.path.basename(f))
                    if not match:
                        continue

                    date_str = match.group()
                    date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%d-%b")

                    for _, row in df.iterrows():
                        enroll = str(row["Enrollment"])
                        name = str(row["Name"])
                        if enroll not in attendance_records:
                            attendance_records[enroll] = {"Enrollment": enroll, "Name": name}
                        attendance_records[enroll][date] = 1

                except Exception as e:
                    print(f"Skipping file {f}: {e}")

            if not attendance_records:
                raise ValueError("No valid attendance data found")

            all_dates = {k for v in attendance_records.values() for k in v if k not in ("Enrollment", "Name")}

            for record in attendance_records.values():
                for date in all_dates:
                    record.setdefault(date, 0)

            combined_df = pd.DataFrame(list(attendance_records.values()))
            combined_df = combined_df[["Enrollment", "Name"] + sorted(all_dates)]
            combined_df["Attendance %"] = (combined_df[sorted(all_dates)].mean(axis=1) * 100).round().astype(int)

            os.makedirs(folder_path, exist_ok=True)
            output_path = os.path.join(folder_path, "combined_attendance.csv")
            combined_df.to_csv(output_path, index=False)

            show_attendance_table(subject, output_path)
            notify(f"Attendance calculated for {subject}", "#27ae60")

        except Exception as e:
            notify(f"Error: {str(e)}", "#e74c3c")

    def show_attendance_table(subject, filepath):
        try:
            df = pd.read_csv(filepath)
            table_window = ctk.CTkToplevel()
            table_window.title(f"{subject} Attendance Summary")
            table_window.geometry("1000x700")

            container = ctk.CTkFrame(table_window)
            container.pack(fill="both", expand=True, padx=20, pady=20)

            header_frame = ctk.CTkFrame(container, fg_color="transparent")
            header_frame.pack(fill="x", pady=(0, 20))

            ctk.CTkLabel(
                header_frame,
                text=f"{subject} Attendance Summary",
                font=("Roboto", 22, "bold"),
                text_color="#2c3e50"
            ).pack(side="left")

            export_btn = ctk.CTkButton(
                header_frame,
                text="Export to Excel",
                command=lambda: export_to_excel(filepath),
                width=120,
                height=30,
                fg_color="#2ecc71",
                hover_color="#27ae60"
            )
            export_btn.pack(side="right")

            table_frame = ctk.CTkScrollableFrame(container)
            table_frame.pack(fill="both", expand=True)

            columns = list(df.columns)

            for col_idx, col in enumerate(columns):
                ctk.CTkLabel(
                    table_frame,
                    text=col,
                    font=("Roboto", 14, "bold"),
                    width=150,
                    height=40,
                    fg_color="#3498db",
                    text_color="white",
                    corner_radius=5
                ).grid(row=0, column=col_idx, padx=2, pady=2)

            for row_idx, row in df.iterrows():
                for col_idx, col in enumerate(columns):
                    val = row[col]
                    if isinstance(val, float) and "%" in col and val < 75:
                        color = "#e74c3c"
                    else:
                        color = "#2c3e50"
                    bg = "#f0f0f0" if row_idx % 2 == 0 else "#ffffff"

                    ctk.CTkLabel(
                        table_frame,
                        text=str(val),
                        font=("Roboto", 13),
                        width=150,
                        height=35,
                        fg_color=bg,
                        text_color=color,
                        corner_radius=5
                    ).grid(row=row_idx + 1, column=col_idx, padx=2, pady=2)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to display attendance: {str(e)}")

    def export_to_excel(filepath):
        try:
            df = pd.read_csv(filepath)
            output_path = filepath.replace(".csv", ".xlsx")
            df.to_excel(output_path, index=False)
            messagebox.showinfo("Success", f"Exported to {output_path}")

            if sys.platform == "win32":
                os.startfile(output_path)
            elif sys.platform == "darwin":
                subprocess.run(["open", output_path])
            else:
                subprocess.run(["xdg-open", output_path])
        except Exception as e:
            messagebox.showerror("Export Error", str(e))

    def open_attendance_folder():
        subject = subject_entry.get().strip()
        if not subject:
            notify("Please enter the subject name", "#e74c3c")
            return

        folder_path = os.path.join("Attendance", subject)
        if os.path.exists(folder_path):
            try:
                if sys.platform == "win32":
                    os.startfile(folder_path)
                elif sys.platform == "darwin":
                    subprocess.run(["open", folder_path])
                else:
                    subprocess.run(["xdg-open", folder_path])
            except Exception as e:
                notify(f"Error opening folder: {str(e)}", "#e74c3c")
        else:
            notify(f"No attendance folder found for {subject}", "#e74c3c")

    # UI Window
    subject_window = ctk.CTkToplevel()
    subject_window.title("Attendance Management")
    subject_window.geometry("650x450")
    subject_window.resizable(False, False)

    main_frame = ctk.CTkFrame(subject_window)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    ctk.CTkLabel(
        main_frame,
        text="Attendance Management",
        font=("Roboto", 24, "bold"),
        text_color="#2c3e50"
    ).pack(pady=10)

    entry_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    entry_frame.pack(pady=10)

    ctk.CTkLabel(
        entry_frame,
        text="Subject Name:",
        font=("Roboto", 16)
    ).grid(row=0, column=0, padx=10, pady=10)

    subject_entry = ctk.CTkEntry(
        entry_frame,
        placeholder_text="e.g. Mathematics",
        font=("Roboto", 16),
        width=300,
        height=40
    )
    subject_entry.grid(row=0, column=1, padx=10, pady=10)

    buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    buttons_frame.pack(pady=20)

    ctk.CTkButton(
        buttons_frame,
        text="View Attendance",
        command=calculate_attendance,
        font=("Roboto", 16),
        width=200,
        height=45,
        fg_color="#3498db",
        hover_color="#2980b9"
    ).pack(side="left", padx=10)

    ctk.CTkButton(
        buttons_frame,
        text="Open Folder",
        command=open_attendance_folder,
        font=("Roboto", 16),
        width=200,
        height=45,
        fg_color="#2ecc71",
        hover_color="#27ae60"
    ).pack(side="left", padx=10)

    notification_label = ctk.CTkLabel(
        main_frame,
        text="",
        font=("Roboto", 14),
        width=500,
        height=50,
        corner_radius=8
    )
    notification_label.pack(pady=20)

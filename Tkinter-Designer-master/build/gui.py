from pathlib import Path
from tkinter import Tk, Canvas, Button, Label, StringVar, Entry
from tkinter import ttk
import serial
import serial.tools.list_ports
import threading
import time
import json


last_received_time = time.time()
# Fungsi untuk mendapatkan daftar port serial yang tersedia
def get_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

# Fungsi untuk memperbarui daftar port di dropdown
def refresh_ports():
    ports = get_serial_ports()
    port_menu['values'] = ports
    port_var.set("")  # Reset pilihan agar tidak ada port yang dipilih
    status_label.config(text="Port COM diperbarui.", fg="#FFFFFF")

# Fungsi untuk membaca data serial
def read_serial():
    try:
        while ser.is_open:
            if ser.in_waiting > 0:
                data = ser.readline().decode().strip()
                process_serial_data(data)
            time.sleep(0.1)
    except serial.SerialException as e:
        status_label.config(text=f"Kesalahan membaca serial: {str(e)}", fg="#FF0000")

#metode json
# def process_serial_data(data):
#     global last_received_time
#     try:
#         # Memeriksa apakah data valid diterima
#         if data:
#             last_received_time = time.time()  # Update waktu terakhir data diterima
#             data = data.strip()

#             # Mengecek apakah data dimulai dengan '#' dan diakhiri dengan '$'
#             if data.startswith("#") and data.endswith("$"):
#                 # Menghapus HEADER ('#') dan TAIL ('$') untuk mendapatkan data yang sesungguhnya
#                 data_content = data[1:-1].strip()  # Hilangkan '#' dan '$'
#                 print(f"Data asli: {data_content}")

#                 # Parse JSON data
#                 try:
#                     json_data = json.loads(data_content)  # Menggunakan json.loads untuk mengonversi string JSON menjadi dictionary
#                     print(f"Data JSON: {json_data}")

#                     # Extract values from the JSON
#                     IMU_yaw = json_data.get("IMU_yaw", "N/A")
#                     IMU_pitch = json_data.get("IMU_pitch", "N/A")
#                     IMU_roll = json_data.get("IMU_roll", "N/A")
#                     pwm1 = json_data.get("pwm1", "N/A")
#                     pwm2 = json_data.get("pwm2", "N/A")
#                     pwm3 = json_data.get("pwm3", "N/A")
#                     pwm4 = json_data.get("pwm4", "N/A")
#                     throttle = json_data.get("throttle", "N/A")
#                     visualYaw = json_data.get("visualYaw", "N/A")
#                     visualPitch = json_data.get("visualPitch", "N/A")
#                     visualRoll = json_data.get("visualRoll", "N/A")

#                     # Debug: Cetak hasil parsing
#                     print(f"Yaw: {IMU_yaw}, Pitch: {IMU_pitch}, Roll: {IMU_roll}")
#                     print(f"PWM Motor: {pwm1}, {pwm2}, {pwm3}, {pwm4}")
#                     print(f"Throttle: {throttle}, Visual Yaw: {visualYaw}, Visual Pitch: {visualPitch}, Visual Roll: {visualRoll}")

#                     # Update nilai pada GUI
#                     yaw_label.config(text=f"{IMU_yaw}")
#                     pitch_label.config(text=f"{IMU_pitch}")
#                     roll_label.config(text=f"{IMU_roll}")
#                     pwm1_label.config(text=f"{pwm1}")
#                     pwm2_label.config(text=f"{pwm2}")
#                     pwm3_label.config(text=f"{pwm3}")
#                     pwm4_label.config(text=f"{pwm4}")
#                     throttle_label.config(text=f"T: {throttle}")
#                     visual_yaw_label.config(text=f"Y: {visualYaw}")
#                     visual_pitch_label.config(text=f"P: {visualPitch}")
#                     visual_roll_label.config(text=f"R: {visualRoll}")

#                     # Update visualisasi titik berdasarkan nilai yaw, throttle, pitch, roll
#                     update_visualization(visualYaw, throttle, visualPitch, visualRoll)

#                     # Status sukses
#                     status_label.config(text="Data diterima", fg="#00FF00")
#                 except json.JSONDecodeError as e:
#                     # Jika terjadi kesalahan saat mengonversi data ke JSON
#                     status_label.config(text="Kesalahan parsing JSON.", fg="#FF0000")
#                     print(f"Kesalahan parsing JSON: {e}")

#             else:
#                 # Jika paket data tidak valid
#                 status_label.config(text="Paket data tidak valid.", fg="#FF0000")

#         else:
#             # Cek apakah sudah cukup lama tanpa data (misalnya 5 detik)
#             if time.time() - last_received_time > 5:
#                 status_label.config(text="Komunikasi serial terputus. Menunggu data...", fg="#FF0000")
#             else:
#                 status_label.config(text="Menunggu data...", fg="#FF0000")

#     except Exception as e:
#         # Menangani kesalahan lain selama parsing data
#         status_label.config(text=f"Kesalahan parsing data: {str(e)}", fg="#FF0000")
#         print(f"Kesalahan parsing data: {str(e)}")



def process_serial_data(data):
    global last_received_time
    try:
        # Memeriksa apakah data valid diterima
        if data:
            last_received_time = time.time()  # Update waktu terakhir data diterima
            data = data.strip()

            # Mengecek apakah data dimulai dengan '#' dan diakhiri dengan '$'
            if data.startswith("#") and data.endswith("$"):
                # Menghapus HEADER ('#') dan TAIL ('$') untuk mendapatkan data yang sesungguhnya
                data_content = data[1:-1].strip()  # Hilangkan '#' dan '$'
                print(f"Data asli: {data_content}")

                # Parse data CSV
                try:
                    csv_values = data_content.split(",")  # Pisahkan berdasarkan koma

                    # Pastikan jumlah nilai sesuai dengan ekspektasi (11 elemen dalam data)
                    if len(csv_values) == 11:
                        # Konversi nilai ke tipe data yang sesuai
                        IMU_yaw = float(csv_values[0])  # Gunakan float untuk yaw
                        IMU_pitch = float(csv_values[1])  # Gunakan float untuk pitch
                        IMU_roll = float(csv_values[2])  # Gunakan float untuk roll
                        pwm1 = int(csv_values[3])  # PWM motor 1
                        pwm2 = int(csv_values[4])  # PWM motor 2
                        pwm3 = int(csv_values[5])  # PWM motor 3
                        pwm4 = int(csv_values[6])  # PWM motor 4
                        throttle = int(csv_values[7])  # Throttle
                        visualYaw = int(csv_values[8])  # Visual Yaw
                        visualPitch = int(csv_values[9])  # Visual Pitch
                        visualRoll = int(csv_values[10])  # Visual Roll

                        # Debug: Cetak hasil parsing
                        print(f"Yaw: {IMU_yaw}, Pitch: {IMU_pitch}, Roll: {IMU_roll}")
                        print(f"PWM Motor: {pwm1}, {pwm2}, {pwm3}, {pwm4}")
                        print(f"Throttle: {throttle}, Visual Yaw: {visualYaw}, Visual Pitch: {visualPitch}, Visual Roll: {visualRoll}")

                        # Update nilai pada GUI
                        yaw_label.config(text=f"{IMU_yaw}")
                        pitch_label.config(text=f"{IMU_pitch}")
                        roll_label.config(text=f"{IMU_roll}")
                        pwm1_label.config(text=f"{pwm1}")
                        pwm2_label.config(text=f"{pwm2}")
                        pwm3_label.config(text=f"{pwm3}")
                        pwm4_label.config(text=f"{pwm4}")
                        throttle_label.config(text=f"T: {throttle}")
                        visual_yaw_label.config(text=f"Y: {visualYaw}")
                        visual_pitch_label.config(text=f"P: {visualPitch}")
                        visual_roll_label.config(text=f"R: {visualRoll}")

                        # Update visualisasi titik berdasarkan nilai yaw, throttle, pitch, roll
                        update_visualization(visualYaw, throttle, visualPitch, visualRoll)

                        # Status sukses
                        status_label.config(text="Data diterima", fg="#00FF00")
                    else:
                        # Jika jumlah nilai tidak sesuai
                        status_label.config(text="Data CSV tidak valid.", fg="#FF0000")
                        print("Kesalahan: Jumlah nilai tidak sesuai.")
                except ValueError as e:
                    # Jika terjadi kesalahan konversi ke tipe data
                    status_label.config(text="Kesalahan parsing CSV.", fg="#FF0000")
                    print(f"Kesalahan parsing CSV: {e}")
            else:
                # Jika paket data tidak valid
                status_label.config(text="Paket data tidak valid.", fg="#FF0000")

        else:
            # Cek apakah sudah cukup lama tanpa data (misalnya 5 detik)
            if time.time() - last_received_time > 5:
                status_label.config(text="Komunikasi serial terputus. Menunggu data...", fg="#FF0000")
            else:
                status_label.config(text="Menunggu data...", fg="#FF0000")

    except Exception as e:
        # Menangani kesalahan lain selama parsing data
        status_label.config(text=f"Kesalahan parsing data: {str(e)}", fg="#FF0000")
        print(f"Kesalahan parsing data: {str(e)}")

        
# Variabel untuk status LED
led_state = False

# Fungsi untuk mengirim data ke Arduino
def send_data(state):
    if ser and ser.is_open:  # Pastikan serial terbuka
        def send():
            try:
                data = b'1\n' if state else b'0\n'  # Kirim "1" jika LED ON, "0" jika OFF
                ser.write(data)
                print(f"Data sent: {data.decode().strip()}")  # Debug data yang dikirim
            except Exception as e:
                print(f"Error sending data: {e}")
        # Jalankan pengiriman dalam thread terpisah
        threading.Thread(target=send, daemon=True).start()
    else:
        print("Serial not connected!")

# Fungsi ketika tombol ditekan
def toggle_led():
    global led_state
    led_state = not led_state  # Ganti status LED
    print(f"LED state: {'1' if led_state else '0'}")  # Debug
    send_data(led_state)  # Kirim perintah ke Arduino
    button_arm.config(text="ARM" if led_state else "DISARM")  # Ubah teks tombol
        
# Fungsi untuk membatasi nilai ke dalam rentang [min_value, max_value]
def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

# Fungsi untuk memperbarui visualisasi titik
def update_visualization(yaw, throttle, pitch, roll):
    # Batasi nilai ke rentang [1000, 2000]
    yaw = clamp(yaw, 1000, 2000)
    throttle = clamp(throttle, 2000, 1000)
    pitch = clamp(pitch, 2000, 1000)
    roll = clamp(roll, 1000, 2000)

    # Normalisasi nilai untuk canvas Throttle (T) dan Yaw (Y) (Throttle: Y, Yaw: X)
    yaw_x = (yaw - 1000) / 1000 * canvas_throttle_yaw.winfo_width()  # Yaw pada sumbu X
    throttle_y = (throttle - 1000) / 1000 * canvas_throttle_yaw.winfo_height()  # Throttle pada sumbu Y
    canvas_throttle_yaw.coords(dot_throttle_yaw, yaw_x - 5, throttle_y - 5, yaw_x + 5, throttle_y + 5)

    # Normalisasi nilai untuk canvas Pitch (P) dan Roll (R) (Pitch: Y, Roll: X)
    roll_x = (roll - 1000) / 1000 * canvas_pitch_roll.winfo_width()  # Roll pada sumbu X
    pitch_y = (pitch - 1000) / 1000 * canvas_pitch_roll.winfo_height()  # Pitch pada sumbu Y
    canvas_pitch_roll.coords(dot_pitch_roll, roll_x - 5, pitch_y - 5, roll_x + 5, pitch_y + 5)

# Fungsi untuk menangani pemilihan port dan baud rate
def select_port():
    global ser
    selected_port = port_var.get()
    baud_rate = baudrate_entry.get()

    if selected_port and baud_rate.isdigit():
        try:
            ser = serial.Serial(selected_port, int(baud_rate), timeout=1)
            status_label.config(text=f"Port: {selected_port}, Baud rate: {baud_rate} - Terhubung", fg="#00FF00")
            threading.Thread(target=read_serial, daemon=True).start()  # Mulai thread untuk membaca data serial
        except (serial.SerialException, ValueError) as e:
            status_label.config(text=f"Gagal terhubung ke {selected_port}: {str(e)}", fg="#FF0000")
    elif not baud_rate.isdigit():
        status_label.config(text="Masukkan nilai baud rate yang valid.", fg="#FF0000")
    else:
        status_label.config(text="Tidak ada port yang dipilih.", fg="#FF0000")
        

# Inisialisasi tkinter
window = Tk()
window.geometry("1000x700")
window.configure(bg="#2D2D2D")
window.title("Drone GUI")

# Label untuk memilih port serial
port_label = Label(window, text="Port Serial", bg="#2D2D2D", fg="#FFFFFF", font=("Poppins", 14))
port_label.place(x=20, y=50)

# Dropdown untuk memilih port serial
port_var = StringVar()
ports = get_serial_ports()
port_menu = ttk.Combobox(window, textvariable=port_var, values=ports, state="readonly", font=("Poppins", 12))
port_menu.place(x=20, y=80, width=200, height=30)

# Tombol untuk memperbarui daftar port (refresh)
refresh_button = Button(window, text="⟳", command=refresh_ports, bg="#2D2D2D", fg="#FFFFFF", font=("Poppins", 16), relief="flat")
refresh_button.place(x=230, y=80, width=40, height=30)

# Label untuk baud rate
baudrate_label = Label(window, text="Baudrate", bg="#2D2D2D", fg="#FFFFFF", font=("Poppins", 14))
baudrate_label.place(x=20, y=130)

# Entry untuk baud rate
baudrate_entry = Entry(window, bg="#FFFFFF", fg="#000000", font=("Poppins", 12))
baudrate_entry.place(x=20, y=160, width=200, height=30)

# Tombol untuk mengonfirmasi pilihan port dan baud rate (Connect)
select_button = Button(window, text="Connect", command=select_port, bg="#FF5722", fg="#FFFFFF", font=("Poppins", 12), relief="flat")
select_button.place(x=20, y=210, width=200, height=40)

# Label untuk menampilkan status port dan baud rate yang dipilih
status_label = Label(window, text="Status", bg="#2D2D2D", fg="#FFFFFF", font=("Poppins", 12))
status_label.place(x=20, y=260)

# Fungsi untuk membuat kotak dengan label
def create_box(parent, text, x, y, boxlabel_text):
    # Buat Canvas untuk box
    box = Canvas(parent, width=250, height=50, bg="#3D3D3D", highlightthickness=0)
    box.place(x=x, y=y)

    # Buat Label di atas box (penamaan box)
    header_label = Label(parent,text=boxlabel_text, bg="#2C2C2C", fg="#FF5722", font=("Poppins", 10))
    header_label.place(x=x, y=y - 25)  # Tempatkan di atas box

    # Buat Label di dalam box untuk menampilkan nilai
    label = Label(box, text=text,bg="#3D3D3D", fg="#FFFFFF", font=("Poppins", 18), wraplength=230)
    label.place(relx=0.5, rely=0.5, anchor="center")  # Tempatkan di tengah box

    return header_label, label
# Kolom pertama untuk Yaw, Pitch, dan Roll
yaw_header, yaw_label = create_box(window, "  ", 350, 50, "Yaw")
pitch_header, pitch_label = create_box(window, "  ", 350, 130, "Pitch")
roll_header, roll_label = create_box(window, "  ", 350, 210, "Roll")

# Kolom kedua untuk PWM Motor 1, 2, 3, dan 4
pwm1_header, pwm1_label = create_box(window, " ", 650, 50, "PWM Motor 1")
pwm2_header, pwm2_label = create_box(window, " ", 650, 130, "PWM Motor 2")
pwm3_header, pwm3_label = create_box(window, " ", 650, 210, "PWM Motor 3")
pwm4_header, pwm4_label = create_box(window, " ", 650, 290, "PWM Motor 4")


# Membuat canvas untuk visualisasi Throttle vs Yaw dan Pitch vs Roll
canvas_throttle_yaw = Canvas(window, width=250, height=250, bg="#3D3D3D", highlightthickness=0)
canvas_throttle_yaw.place(x=20, y=400)
canvas_throttle_yaw.create_line(125, 0, 125, 250, fill="white")  # garis vertikal
canvas_throttle_yaw.create_line(0, 125, 250, 125, fill="white")  # garis horizontal
dot_throttle_yaw = canvas_throttle_yaw.create_oval(120, 120, 130, 130, fill="#FF5722")

canvas_pitch_roll = Canvas(window, width=250, height=250, bg="#3D3D3D", highlightthickness=0)
canvas_pitch_roll.place(x=300, y=400)
canvas_pitch_roll.create_line(125, 0, 125, 250, fill="white")  # garis vertikal
canvas_pitch_roll.create_line(0, 125, 250, 125, fill="white")  # garis horizontal
dot_pitch_roll = canvas_pitch_roll.create_oval(120, 120, 130, 130, fill="#FF5722")

# Label untuk Throttle, Visual Yaw, Visual Pitch, Visual Roll
throttle_label = Label(window, text="T: 0", bg="#2D2D2D", fg="#FFFFFF", font=("Poppins", 12))
throttle_label.place(x=20, y=650)
visual_yaw_label = Label(window, text="Y: 0", bg="#2D2D2D", fg="#FFFFFF", font=("Poppins", 12))
visual_yaw_label.place(x=145, y=650)
visual_pitch_label = Label(window, text="P: 0", bg="#2D2D2D", fg="#FFFFFF", font=("Poppins", 12))
visual_pitch_label.place(x=300, y=650)
visual_roll_label = Label(window, text="R: 0", bg="#2D2D2D", fg="#FFFFFF", font=("Poppins", 12))
visual_roll_label.place(x=425, y=650)

# Membuat tombol untuk mengubah status LED
button_arm = Button(window, text="ARM", command=toggle_led, width=22, height=1, bg="#FF5722", fg="white", font=("Poppins", 14), relief="flat")
button_arm.place(x=350, y=290)
arm_label = Label(window, text="Motor Arm", bg="#2D2D2D", fg="#FF5722", font=("Poppins", 12))
arm_label.place(x=350, y=265)


# Jalankan aplikasi
window.mainloop()

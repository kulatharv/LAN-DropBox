# LAN-DropBox
LANShare Hub is a local network file-sharing app with QR code access. Upload, download, and manage files securely, track connected devices, and view logs in real-time. Fast, responsive, and ideal for sharing files across devices without internet.


## ✨ Key Features

- **Upload Files:** Quickly upload files from any LAN-connected device.  
- **Manage Files:** Download, delete, or generate QR codes for each uploaded file.  
- **Connected Devices:** Monitor all devices currently connected to the dashboard.  
- **Logs:** Detailed file upload logs with filename, timestamp, and device IP.  
- **Dashboard QR Code:** Scan QR code to access the dashboard on mobile devices.  

---

## 🛠 Technology Stack

- **Backend:** Python Flask  
- **Frontend:** HTML, CSS, JavaScript  
- **QR Code Generation:** Python `qrcode` library  
- **Data Storage:** JSON files for logs and device tracking  

---

## 🚀 Installation

1. Clone the repository:  
   git clone https://github.com/yourusername/LANShare-Hub.git
   cd LANShare-Hub

Install required packages:
      pip install flask qrcode pillow

Run the application:
    python app.py
    Open your browser using your local IP, e.g., http://192.168.1.5:5000/.
    Scan the Dashboard QR code to connect from mobile devices.

🖥 **Usage**

Upload Files: Use the Upload card to add files.

Manage Files: View all uploaded files, download, delete, or generate QR codes.

Connected Devices: Monitor devices in real-time.

View Logs: Check activity logs for all file uploads.

🖼 Screenshots
<img width="1916" height="903" alt="image" src="https://github.com/user-attachments/assets/a34f176a-ad88-49a5-8f56-d1876bc8bc16" />
<img width="1918" height="648" alt="image" src="https://github.com/user-attachments/assets/2e7f3d1b-e708-409e-bf26-c44d5905b1a0" />
<img width="1919" height="426" alt="image" src="https://github.com/user-attachments/assets/0108ea71-0875-4eb4-b724-f708c3106a60" />






📄 License

This project is licensed under the MIT License.

💡 Notes

Ideal for offices, schools, or personal LAN setups.

No internet required; works entirely on LAN.

Fully responsive, interactive, and easy-to-use UI.


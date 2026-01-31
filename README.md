# Local File Transfer

A simple web-based file transfer application that lets you send files from any device to your computer over WiFi.

## The Problem

I needed to transfer 10+ GB of files between two laptops on the same WiFi network without using USB drives, cloud storage, or third-party apps.

## The Solution

A Python/Flask web server that:
- Runs on your computer
- Provides a web interface accessible from any device on the same network
- Shows upload progress with percentage and file size
- Handles large files (up to 15 GB)
- Preserves file names

## Screenshot

When you open the URL from another device, you'll see a drag-and-drop upload interface with a progress bar.

## Requirements

- Python 3.x
- Flask

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/local-file-transfer.git
   cd local-file-transfer
   ```

2. Install Flask:
   ```bash
   pip install flask
   ```

## Usage

1. Run the server on your computer (the one receiving files):
   ```bash
   python file_server.py
   ```

2. You'll see output like:
   ```
   =======================================================
      FILE TRANSFER SERVER RUNNING
   =======================================================

      Open this URL from OTHER computers on your WiFi:

      >>> http://192.168.x.x:5000

      Files will be saved to:
      C:\Users\YourName\ReceivedFiles
   =======================================================
   ```

3. On your other device, open a browser and go to the URL shown

4. Select files and click Upload

5. Files will appear in the `ReceivedFiles` folder in your home directory

## Features

- Drag and drop file upload
- Progress bar with percentage
- Shows upload size (e.g., "5.2 GB / 10.4 GB")
- Works with any device that has a browser (laptops, phones, tablets)
- No internet required - works entirely on local WiFi

## Firewall Note

If other devices can't connect, you may need to allow Python through your firewall:

```bash
# Windows (run as Administrator)
netsh advfirewall firewall add rule name="File Transfer" dir=in action=allow protocol=TCP localport=5000
```

## Built With

- Python
- Flask
- HTML/CSS/JavaScript
- Claude Code (AI-assisted development)

## License

MIT License - feel free to use and modify.

from flask import Flask, request, render_template_string, jsonify
import os
import socket

app = Flask(__name__)

# Increase max file size (15 GB)
app.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024 * 1024

# Folder where uploaded files will be saved
UPLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "ReceivedFiles")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>File Transfer</title>
    <style>
        * { box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 { color: #333; margin-bottom: 10px; font-size: 28px; }
        .subtitle { color: #666; margin-bottom: 30px; }
        .upload-area {
            border: 3px dashed #ddd;
            padding: 50px;
            text-align: center;
            margin: 20px 0;
            border-radius: 15px;
            transition: all 0.3s ease;
            background: #fafafa;
            cursor: pointer;
        }
        .upload-area:hover { border-color: #667eea; background: #f0f0ff; }
        .upload-area.dragover { border-color: #667eea; background: #e8e8ff; transform: scale(1.02); }
        input[type="file"] { display: none; }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 40px;
            border: none;
            cursor: pointer;
            font-size: 18px;
            border-radius: 30px;
            transition: transform 0.2s, box-shadow 0.2s;
            width: 100%;
        }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4); }
        .btn:disabled { background: #ccc; cursor: not-allowed; transform: none; }
        .success {
            color: #2e7d32;
            padding: 15px 20px;
            background: #e8f5e9;
            margin: 20px 0;
            border-radius: 10px;
            border-left: 4px solid #4caf50;
        }
        .error {
            color: #c62828;
            padding: 15px 20px;
            background: #ffebee;
            margin: 20px 0;
            border-radius: 10px;
            border-left: 4px solid #f44336;
        }
        .info { color: #666; font-size: 14px; margin-top: 5px; }
        .path-info {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 10px;
            margin-top: 30px;
            font-family: monospace;
            font-size: 14px;
            color: #555;
        }
        .icon { font-size: 48px; margin-bottom: 15px; }
        .file-list {
            text-align: left;
            margin-top: 20px;
            max-height: 200px;
            overflow-y: auto;
        }
        .file-item {
            padding: 8px 12px;
            background: #f0f0f0;
            margin: 5px 0;
            border-radius: 5px;
            font-size: 14px;
        }

        /* Progress Bar Styles */
        .progress-container {
            display: none;
            margin: 20px 0;
        }
        .progress-container.active { display: block; }
        .progress-bar-bg {
            width: 100%;
            height: 30px;
            background: #e0e0e0;
            border-radius: 15px;
            overflow: hidden;
        }
        .progress-bar {
            height: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            width: 0%;
            transition: width 0.3s ease;
            border-radius: 15px;
        }
        .progress-text {
            text-align: center;
            margin-top: 10px;
            font-size: 16px;
            color: #333;
        }
        .progress-details {
            text-align: center;
            margin-top: 5px;
            font-size: 14px;
            color: #666;
        }
        .status-message {
            text-align: center;
            padding: 20px;
            font-size: 18px;
            display: none;
        }
        .status-message.active { display: block; }
    </style>
</head>
<body>
    <div class="container">
        <h1>File Transfer</h1>
        <p class="subtitle">Upload files from this device to the server computer</p>

        <div id="statusMessage" class="status-message"></div>

        <form id="uploadForm" enctype="multipart/form-data">
            <div class="upload-area" id="dropArea">
                <div class="icon">+</div>
                <h3>Drag & Drop Files Here</h3>
                <p>or click to browse</p>
                <input type="file" name="files" id="fileInput" multiple>
                <p class="info">You can select multiple files</p>
            </div>
            <div id="fileList" class="file-list"></div>

            <div class="progress-container" id="progressContainer">
                <div class="progress-bar-bg">
                    <div class="progress-bar" id="progressBar"></div>
                </div>
                <div class="progress-text" id="progressText">0%</div>
                <div class="progress-details" id="progressDetails">Preparing upload...</div>
            </div>

            <button type="submit" class="btn" id="uploadBtn">Upload Files</button>
        </form>

        <div class="path-info">
            <strong>Save location:</strong> {{ upload_path }}
        </div>
    </div>

    <script>
        const dropArea = document.getElementById('dropArea');
        const fileInput = document.getElementById('fileInput');
        const fileList = document.getElementById('fileList');
        const uploadForm = document.getElementById('uploadForm');
        const uploadBtn = document.getElementById('uploadBtn');
        const progressContainer = document.getElementById('progressContainer');
        const progressBar = document.getElementById('progressBar');
        const progressText = document.getElementById('progressText');
        const progressDetails = document.getElementById('progressDetails');
        const statusMessage = document.getElementById('statusMessage');

        // Click to browse
        dropArea.addEventListener('click', (e) => {
            if (e.target === dropArea || e.target.parentElement === dropArea) {
                fileInput.click();
            }
        });

        // Drag and drop events
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, preventDefaults, false);
            document.body.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            dropArea.addEventListener(eventName, () => dropArea.classList.add('dragover'));
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, () => dropArea.classList.remove('dragover'));
        });

        dropArea.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            fileInput.files = dt.files;
            updateFileList();
        });

        fileInput.addEventListener('change', updateFileList);

        function formatBytes(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        }

        function updateFileList() {
            const files = fileInput.files;
            if (files.length > 0) {
                let totalSize = 0;
                let html = '<strong>Selected files:</strong>';
                const maxShow = 10;
                for (let i = 0; i < files.length; i++) {
                    totalSize += files[i].size;
                    if (i < maxShow) {
                        html += '<div class="file-item">' + files[i].name + ' (' + formatBytes(files[i].size) + ')</div>';
                    }
                }
                if (files.length > maxShow) {
                    html += '<div class="file-item">... and ' + (files.length - maxShow) + ' more files</div>';
                }
                html += '<div class="file-item"><strong>Total: ' + files.length + ' files, ' + formatBytes(totalSize) + '</strong></div>';
                fileList.innerHTML = html;
            } else {
                fileList.innerHTML = '';
            }
        }

        uploadForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const files = fileInput.files;
            if (files.length === 0) {
                showStatus('Please select files first!', 'error');
                return;
            }

            const formData = new FormData();
            for (let i = 0; i < files.length; i++) {
                formData.append('files', files[i]);
            }

            // Show progress bar
            progressContainer.classList.add('active');
            uploadBtn.disabled = true;
            uploadBtn.textContent = 'Uploading...';
            statusMessage.classList.remove('active');

            const xhr = new XMLHttpRequest();

            // Track upload progress
            xhr.upload.addEventListener('progress', function(e) {
                if (e.lengthComputable) {
                    const percentComplete = Math.round((e.loaded / e.total) * 100);
                    progressBar.style.width = percentComplete + '%';
                    progressText.textContent = percentComplete + '%';
                    progressDetails.textContent = formatBytes(e.loaded) + ' / ' + formatBytes(e.total);
                }
            });

            xhr.addEventListener('load', function() {
                if (xhr.status === 200) {
                    showStatus('Successfully uploaded ' + files.length + ' file(s)!', 'success');
                    fileInput.value = '';
                    fileList.innerHTML = '';
                } else {
                    showStatus('Upload failed. Please try again.', 'error');
                }
                resetProgress();
            });

            xhr.addEventListener('error', function() {
                showStatus('Upload failed. Check your connection.', 'error');
                resetProgress();
            });

            xhr.addEventListener('abort', function() {
                showStatus('Upload cancelled.', 'error');
                resetProgress();
            });

            xhr.open('POST', '/', true);
            xhr.send(formData);
        });

        function showStatus(message, type) {
            statusMessage.textContent = message;
            statusMessage.className = 'status-message active ' + type;
        }

        function resetProgress() {
            progressContainer.classList.remove('active');
            progressBar.style.width = '0%';
            progressText.textContent = '0%';
            progressDetails.textContent = '';
            uploadBtn.disabled = false;
            uploadBtn.textContent = 'Upload Files';
        }
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('files')
        count = 0
        for file in files:
            if file.filename:
                # Preserve folder structure
                filename = file.filename.replace('\\', '/')
                # Remove any leading slashes
                filename = filename.lstrip('/')
                save_path = os.path.join(UPLOAD_FOLDER, filename)
                # Create directory if needed
                dir_path = os.path.dirname(save_path)
                if dir_path:
                    os.makedirs(dir_path, exist_ok=True)
                file.save(save_path)
                count += 1
                print(f"   Received: {filename}")
        return jsonify({'success': True, 'count': count})

    return render_template_string(HTML_TEMPLATE, upload_path=UPLOAD_FOLDER)


def get_local_ip():
    """Get the local IP address of this machine"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


if __name__ == '__main__':
    local_ip = get_local_ip()
    port = 5000

    print("\n" + "=" * 55)
    print("   FILE TRANSFER SERVER RUNNING")
    print("=" * 55)
    print(f"\n   Open this URL from OTHER computers on your WiFi:")
    print(f"\n   >>> http://{local_ip}:{port}")
    print(f"\n   Files will be saved to:")
    print(f"   {UPLOAD_FOLDER}")
    print(f"\n   Press Ctrl+C to stop the server")
    print("=" * 55 + "\n")

    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)

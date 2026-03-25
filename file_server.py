from flask import Flask, request, render_template_string, jsonify, send_from_directory, send_file, abort
import os
import socket
import zipfile
import tempfile

app = Flask(__name__)

# Increase max file size (15 GB)
app.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024 * 1024

# Folder where uploaded files will be saved
UPLOAD_FOLDER = os.path.join(os.getcwd(), "ReceivedFiles")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Folder for files you want to share/send to other devices
SHARE_FOLDER = os.path.join(os.getcwd(), "SharedFiles")
os.makedirs(SHARE_FOLDER, exist_ok=True)

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

        /* Tab Styles */
        .tabs {
            display: flex;
            margin-bottom: 30px;
            border-bottom: 3px solid #eee;
        }
        .tab {
            padding: 12px 30px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            color: #999;
            border-bottom: 3px solid transparent;
            margin-bottom: -3px;
            transition: all 0.3s;
        }
        .tab:hover { color: #667eea; }
        .tab.active {
            color: #667eea;
            border-bottom-color: #667eea;
        }
        .tab-content { display: none; }
        .tab-content.active { display: block; }

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

        /* Download Section Styles */
        .download-list {
            margin-top: 10px;
        }
        .download-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px 15px;
            background: #f8f8f8;
            margin: 8px 0;
            border-radius: 10px;
            border: 1px solid #eee;
            transition: background 0.2s;
        }
        .download-item:hover { background: #f0f0ff; border-color: #667eea; }
        .download-item-info {
            flex: 1;
            min-width: 0;
        }
        .download-item-name {
            font-weight: 600;
            color: #333;
            word-break: break-all;
        }
        .download-item-size {
            font-size: 13px;
            color: #888;
            margin-top: 2px;
        }
        .download-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 8px 20px;
            border: none;
            cursor: pointer;
            font-size: 14px;
            border-radius: 20px;
            text-decoration: none;
            margin-left: 15px;
            white-space: nowrap;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .download-btn:hover { transform: translateY(-1px); box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3); }
        .empty-message {
            text-align: center;
            padding: 40px;
            color: #999;
            font-size: 16px;
        }
        .refresh-btn {
            background: none;
            border: 2px solid #667eea;
            color: #667eea;
            padding: 10px 25px;
            cursor: pointer;
            font-size: 14px;
            border-radius: 20px;
            transition: all 0.2s;
            margin-bottom: 15px;
        }
        .refresh-btn:hover { background: #667eea; color: white; }
        .folder-item {
            cursor: pointer;
        }
        .folder-item .download-item-name { color: #667eea; }
        .folder-icon { margin-right: 8px; }
        .breadcrumb {
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 5px;
            margin-bottom: 15px;
            font-size: 14px;
            color: #666;
        }
        .breadcrumb a {
            color: #667eea;
            text-decoration: none;
            cursor: pointer;
        }
        .breadcrumb a:hover { text-decoration: underline; }
        .breadcrumb span { color: #999; }
    </style>
</head>
<body>
    <div class="container">
        <h1>File Transfer</h1>
        <p class="subtitle">Send and receive files between devices</p>

        <div class="tabs">
            <div class="tab active" onclick="switchTab('upload', this)">Upload to Server</div>
            <div class="tab" onclick="switchTab('download', this)">Download from Server</div>
        </div>

        <div id="statusMessage" class="status-message"></div>

        <!-- UPLOAD TAB -->
        <div id="tab-upload" class="tab-content active">
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
                <strong>Files are saved to:</strong> {{ upload_path }}
            </div>
        </div>

        <!-- DOWNLOAD TAB -->
        <div id="tab-download" class="tab-content">
            <p style="color:#666; margin-bottom:15px;">Files shared by the server computer. Click folders to browse, click "Download" to save files.</p>
            <button class="refresh-btn" onclick="loadFiles(currentPath)">Refresh</button>
            <a id="zipBtn" class="btn" style="display:inline-block; width:auto; padding:12px 30px; font-size:15px; margin-bottom:15px; margin-left:10px; text-decoration:none;" href="/download-zip">Download All as ZIP</a>
            <div id="breadcrumb" class="breadcrumb"></div>
            <div id="downloadList" class="download-list">
                <div class="empty-message">Loading files...</div>
            </div>
            <div class="path-info">
                <strong>Shared from:</strong> {{ share_path }}
            </div>
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

        /* ===== TAB SWITCHING ===== */
        function switchTab(tab, el) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            document.getElementById('tab-' + tab).classList.add('active');
            el.classList.add('active');
            if (tab === 'download') loadFiles('');
        }

        /* ===== DOWNLOAD SECTION ===== */
        var currentPath = '';

        function loadFiles(path) {
            currentPath = path || '';
            var downloadList = document.getElementById('downloadList');
            downloadList.innerHTML = '<div class="empty-message">Loading...</div>';
            updateBreadcrumb();
            // Update ZIP download button
            var zipBtn = document.getElementById('zipBtn');
            zipBtn.href = '/download-zip' + (currentPath ? '?path=' + encodeURIComponent(currentPath) : '');
            zipBtn.textContent = currentPath ? 'Download "' + currentPath.split('/').pop() + '" as ZIP' : 'Download All as ZIP';

            var url = '/files' + (currentPath ? '?path=' + encodeURIComponent(currentPath) : '');

            fetch(url)
                .then(function(r) { return r.json(); })
                .then(function(data) {
                    if (data.items.length === 0) {
                        downloadList.innerHTML = '<div class="empty-message">' +
                            (currentPath ? 'This folder is empty.' : 'No files shared yet.<br><br>Place files or folders in the SharedFiles folder on the server computer.') +
                            '</div>';
                        return;
                    }
                    var html = '';
                    data.items.forEach(function(item) {
                        if (item.type === 'folder') {
                            var folderPath = currentPath ? currentPath + '/' + item.name : item.name;
                            html += '<div class="download-item folder-item" data-folder="' + encodeURIComponent(folderPath) + '">' +
                                '<div class="download-item-info">' +
                                    '<div class="download-item-name"><span class="folder-icon">&#128193;</span>' + escapeHtml(item.name) + '</div>' +
                                    '<div class="download-item-size">Folder</div>' +
                                '</div>' +
                            '</div>';
                        } else {
                            var filePath = currentPath ? currentPath + '/' + item.name : item.name;
                            html += '<div class="download-item">' +
                                '<div class="download-item-info">' +
                                    '<div class="download-item-name">&#128196; ' + escapeHtml(item.name) + '</div>' +
                                    '<div class="download-item-size">' + formatBytes(item.size) + '</div>' +
                                '</div>' +
                                '<a class="download-btn" href="/download/' + encodeURIComponent(filePath) + '">Download</a>' +
                            '</div>';
                        }
                    });
                    downloadList.innerHTML = html;
                })
                .catch(function() {
                    downloadList.innerHTML = '<div class="empty-message">Failed to load file list. Try refreshing.</div>';
                });
        }

        // Handle folder clicks using event delegation (avoids inline JS escaping issues)
        document.addEventListener('click', function(e) {
            var folderItem = e.target.closest('.folder-item');
            if (folderItem && folderItem.dataset.folder) {
                loadFiles(decodeURIComponent(folderItem.dataset.folder));
            }
            var bcLink = e.target.closest('.bc-link');
            if (bcLink && bcLink.dataset.path !== undefined) {
                loadFiles(decodeURIComponent(bcLink.dataset.path));
            }
        });

        function updateBreadcrumb() {
            var bc = document.getElementById('breadcrumb');
            if (!currentPath) {
                bc.innerHTML = '<strong>SharedFiles</strong>';
                return;
            }
            var html = '<a class="bc-link" data-path="">SharedFiles</a>';
            var parts = currentPath.split('/');
            var builtPath = '';
            for (var i = 0; i < parts.length; i++) {
                builtPath += (i > 0 ? '/' : '') + parts[i];
                html += ' <span>/</span> ';
                if (i === parts.length - 1) {
                    html += '<strong>' + escapeHtml(parts[i]) + '</strong>';
                } else {
                    html += '<a class="bc-link" data-path="' + encodeURIComponent(builtPath) + '">' + escapeHtml(parts[i]) + '</a>';
                }
            }
            bc.innerHTML = html;
        }

        function escapeHtml(text) {
            var div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

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
                    var errorMsg = 'Upload failed. ';
                    try {
                        var response = JSON.parse(xhr.responseText);
                        if (response.error) {
                            errorMsg += 'Error: ' + response.error;
                        }
                    } catch(e) {
                        errorMsg += 'Please try again.';
                    }
                    showStatus(errorMsg, 'error');
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
        try:
            files = request.files.getlist('files')
            if not files:
                return jsonify({'success': False, 'error': 'No files received'}), 400

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
            return jsonify({'success': True, 'count': count}), 200
        except Exception as e:
            print(f"   ERROR during upload: {str(e)}")
            return jsonify({'success': False, 'error': str(e)}), 500

    return render_template_string(HTML_TEMPLATE, upload_path=UPLOAD_FOLDER, share_path=SHARE_FOLDER)


@app.route('/files')
def list_files():
    """List files and folders in the shared folder (supports subfolder browsing)"""
    # Get the subfolder path from query parameter (e.g., /files?path=Ms Office 2016)
    sub_path = request.args.get('path', '')

    # Security: prevent path traversal (no .. allowed)
    if '..' in sub_path:
        abort(400)

    browse_dir = os.path.join(SHARE_FOLDER, sub_path)
    browse_dir = os.path.normpath(browse_dir)

    # Make sure we're still inside SHARE_FOLDER
    if not browse_dir.startswith(os.path.normpath(SHARE_FOLDER)):
        abort(403)

    if not os.path.isdir(browse_dir):
        abort(404)

    items = []
    for name in os.listdir(browse_dir):
        full_path = os.path.join(browse_dir, name)
        if os.path.isdir(full_path):
            items.append({
                'name': name,
                'type': 'folder',
                'size': 0
            })
        elif os.path.isfile(full_path):
            items.append({
                'name': name,
                'type': 'file',
                'size': os.path.getsize(full_path)
            })

    # Sort: folders first, then files, alphabetically
    items.sort(key=lambda x: (0 if x['type'] == 'folder' else 1, x['name'].lower()))
    return jsonify({'items': items, 'path': sub_path})


@app.route('/download/<path:filename>')
def download_file(filename):
    """Download a file from the shared folder (supports subfolders)"""
    # Security: prevent path traversal
    if '..' in filename:
        abort(400)

    filepath = os.path.join(SHARE_FOLDER, filename)
    filepath = os.path.normpath(filepath)

    # Make sure we're still inside SHARE_FOLDER
    if not filepath.startswith(os.path.normpath(SHARE_FOLDER)):
        abort(403)

    if not os.path.isfile(filepath):
        abort(404)

    directory = os.path.dirname(filepath)
    basename = os.path.basename(filepath)
    return send_from_directory(directory, basename, as_attachment=True)


@app.route('/download-zip')
def download_zip():
    """Download a folder as a ZIP file"""
    sub_path = request.args.get('path', '')

    # Security: prevent path traversal
    if '..' in sub_path:
        abort(400)

    folder_path = os.path.join(SHARE_FOLDER, sub_path) if sub_path else SHARE_FOLDER
    folder_path = os.path.normpath(folder_path)

    # Make sure we're still inside SHARE_FOLDER
    if not folder_path.startswith(os.path.normpath(SHARE_FOLDER)):
        abort(403)

    if not os.path.isdir(folder_path):
        abort(404)

    # Create zip in a temp file
    zip_name = os.path.basename(folder_path) if sub_path else 'SharedFiles'
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
    tmp_path = tmp.name
    tmp.close()

    print(f"   Zipping folder: {folder_path}")
    with zipfile.ZipFile(tmp_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zf.write(file_path, arcname)
    print(f"   ZIP ready: {zip_name}.zip")

    return send_file(tmp_path, as_attachment=True, download_name=f'{zip_name}.zip')


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
    # Get port from environment variable (for Render) or default to 5000 (for local)
    port = int(os.environ.get('PORT', 5000))

    # Check if running on Render (or other cloud platform)
    is_production = os.environ.get('RENDER') or os.environ.get('PORT')

    if not is_production:
        # Local development mode - show IP address
        local_ip = get_local_ip()
        print("\n" + "=" * 55)
        print("   FILE TRANSFER SERVER RUNNING")
        print("=" * 55)
        print(f"\n   Open this URL from OTHER computers on your WiFi:")
        print(f"\n   >>> http://{local_ip}:{port}")
        print(f"\n   Uploaded files saved to:")
        print(f"   {UPLOAD_FOLDER}")
        print(f"\n   Files available for download from:")
        print(f"   {SHARE_FOLDER}")
        print(f"   (Put files here to share them!)")
        print(f"\n   Press Ctrl+C to stop the server")
        print("=" * 55 + "\n")
    else:
        # Production mode - simple startup
        print(f"Starting File Transfer Server on port {port}...")

    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)

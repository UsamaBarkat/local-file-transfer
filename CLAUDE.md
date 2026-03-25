# File Transfer Application

## Project Overview
A web-based file transfer tool built with Python/Flask. Supports **bidirectional** file transfer (upload and download) with both **local network** and **internet accessibility**. Now deployed live on PythonAnywhere!

## Tech Stack
- **Backend:** Python 3, Flask
- **Frontend:** Vanilla HTML/CSS/JS (inline in `file_server.py` via `render_template_string`)
- **Deployment:** PythonAnywhere (free tier)
- **Production Server:** Gunicorn (for cloud deployment)
- **No database** — files are saved directly to disk
  - **Single unified folder:** `TransferFiles` (used for both upload and download)
  - Local: `E:\AI-300\file-transfer-application\TransferFiles`
  - Cloud: `/home/usamanizamani/local-file-transfer/TransferFiles`

## Project Structure
- `file_server.py` — Single-file application (Flask server + embedded HTML/CSS/JS template)
- `requirements.txt` — Python dependencies (Flask, gunicorn)
- `render.yaml` — Render deployment configuration (not used, kept for reference)
- `README.md` — Project documentation
- `CLAUDE.md` — This file - project context and progress tracking
- `test_upload.txt` — Test file for upload testing
- `.claude/` — Claude Code settings

## Key Design Decisions
- Single-file architecture: entire app lives in `file_server.py` for simplicity and portability
- **Unified folder approach:** Both upload and download use the same `TransferFiles` folder for true bidirectional transfer
  - Laptop 1 uploads → files go to TransferFiles
  - Laptop 2 downloads → reads from TransferFiles (sees Laptop 1's uploads immediately!)
- Flask dev server is intentional — this is a LAN-only tool, not a production web app
- Server binds to `0.0.0.0:5000` to be accessible from other devices on the network
- Auto-detects local IP via UDP socket trick (`get_local_ip()`)
- Tabbed UI: "Upload to Server" and "Download from Server" tabs
- Download section uses `data-` attributes + event delegation (NOT inline onclick) to avoid Python/Jinja2 string escaping issues with backslashes
- ZIP downloads use `tempfile` + `zipfile` to create on-the-fly archives
- Mobile-first responsive design with breakpoints for tablets (768px) and phones (480px)

## Current Features
- **Upload:** Drag & drop or browse files, multi-file support, real-time progress bar, detailed error messages
- **Download:** Browse shared folders with breadcrumb navigation, download individual files, download entire folders as ZIP
- **Bidirectional Transfer:** Files uploaded from any device instantly appear in download list on all devices
- **Folder browsing:** `/files?path=` API supports subfolder navigation with path traversal protection
- **ZIP download:** `/download-zip?path=` zips any folder on-the-fly for one-click download
- **Mobile Responsive:** Fully optimized for phones and tablets with touch-friendly interface
- **Error Handling:** Comprehensive error messages for debugging upload/download issues

## Running Locally
```bash
pip install flask
python file_server.py
```
Access at: `http://your-local-ip:5000`

## Live Deployment
**Live URL:** https://usamanizamani.pythonanywhere.com
- Deployed on PythonAnywhere (free tier)
- Accessible from anywhere in the world
- No installation needed for users - just open the URL in a browser
- Monthly maintenance: Login and click "Run until 1 month from today" button

## Known Limitations
- **PythonAnywhere Free Tier:** Upload size limited to ~100 MB per file (request timeout/memory limits)
  - Local network mode: Supports up to 15 GB (configured in code)
  - Solution: Use local network mode for large files
- No `secure_filename()` on uploaded files
- No chunked upload — large files buffered in memory
- No authentication — anyone with URL can upload/download
- ZIP creation for very large folders may be slow (done synchronously)
- **Cold start:** First visitor after long inactivity may experience 5-15 second delay (PythonAnywhere free tier limitation)

## Development Roadmap

### Phase 1 — Core Features ✅ COMPLETED
- ~~Add file download capability (bidirectional transfer)~~ ✅ DONE
- ~~Folder browsing with breadcrumb navigation~~ ✅ DONE
- ~~ZIP download for entire folders~~ ✅ DONE

### Phase 2 — Internet Accessibility ✅ COMPLETED (March 2026)
- ~~Deploy to internet-accessible platform~~ ✅ DONE
- ~~Choose free hosting (PythonAnywhere vs Render)~~ ✅ DONE - Selected PythonAnywhere
- ~~Configure for cloud deployment~~ ✅ DONE
- ~~Live at: https://usamanizamani.pythonanywhere.com~~ ✅ DONE
- ~~Fix upload errors with comprehensive error handling~~ ✅ DONE
- ~~Enable true bidirectional transfer (unified folder)~~ ✅ DONE
- ~~Add mobile-responsive design~~ ✅ DONE

**Decision Log:**
- Evaluated Render (requires credit card, potential billing risks)
- Chose PythonAnywhere (no credit card, zero billing risk, beginner-friendly)
- Successfully deployed with WSGI configuration
- Tested upload/download from 2 devices (portfolio demo ready)
- Discovered ~100 MB file size limit on PythonAnywhere free tier
- Mobile optimization crucial for portfolio demonstrations

### Phase 3 — Security & Performance Improvements (PLANNED)
- Add password protection (optional authentication)
- Add `secure_filename()` for uploaded files
- Add chunked/streaming uploads (support 50+ GB files)
- Add file expiry (auto-delete old files)
- Add upload size limits per file
- Add email notifications for uploads

### Phase 4 — UI/UX Enhancements (PLANNED)
- Add delete button for uploaded files
- Custom branding (logo, colors, user's name)
- Dark mode toggle
- File preview capabilities (images, PDFs, videos)
- Upload progress for individual files in multi-file uploads

### Phase 5 (Optional) — Advanced Features
- User accounts with individual storage
- File sharing with expiring links
- Package as `.exe` for Windows (standalone app)
- WebRTC peer-to-peer transfer option

## Deployment Details

### PythonAnywhere Configuration
- **Platform:** PythonAnywhere Free Tier
- **URL:** https://usamanizamani.pythonanywhere.com
- **Username:** usamanizamani
- **Python Version:** 3.10
- **Web Framework:** Flask
- **WSGI Config:** `/var/www/usamanizamani_pythonanywhere_com_wsgi.py`
- **Project Path:** `/home/usamanizamani/local-file-transfer/`
- **Storage Limit:** 512 MB
- **Maintenance Required:** Monthly "Run until 1 month from today" button click

### Deployment Files Added
- `requirements.txt` - Lists Flask==3.0.0 and gunicorn==21.2.0
- `render.yaml` - Render configuration (created but not used, kept for reference)
- Modified `file_server.py` to support both local and cloud environments:
  - Uses `os.getcwd()` instead of `os.path.expanduser("~")` for cloud compatibility
  - Detects production mode via environment variables
  - Simplified startup messages for cloud deployment

### Key Changes for Cloud Deployment
1. **Folder paths:** Changed from home directory (`~`) to current working directory for cloud compatibility
2. **Port handling:** Reads `PORT` environment variable for cloud platforms
3. **Production detection:** Checks for `RENDER` or `PORT` env vars to simplify output
4. **WSGI setup:** Created proper WSGI configuration for PythonAnywhere

### Deployment Process Summary
1. Researched hosting options (Render vs PythonAnywhere)
2. Chose PythonAnywhere (no credit card requirement, zero billing risk)
3. Created account and cloned GitHub repository
4. Configured WSGI file with correct paths
5. Fixed import errors (ModuleNotFoundError)
6. Successfully deployed and tested

## User Notes
- User: Usama (usamabarkat on GitHub, usamanizamani on PythonAnywhere)
- User is a beginner with no IT/AI background — keep explanations simple and step-by-step
- Guide through decisions, explain the "why" behind changes
- User prefers zero-risk solutions (chose PythonAnywhere over Render to avoid credit card requirement)

## Portfolio Demo Guide

### Use Case
This project serves as a **portfolio piece** to demonstrate full-stack development skills:
- Backend: Python/Flask API development
- Frontend: Vanilla JavaScript, responsive CSS
- Deployment: Cloud hosting configuration (PythonAnywhere/WSGI)
- Real-world functionality: Actual file transfer between devices

### Demo Script
**1. Introduction:**
> "I built a web-based file transfer tool with bidirectional upload/download capabilities. It's deployed live and accessible from anywhere."

**2. Show the Live Site:**
- Open: https://usamanizamani.pythonanywhere.com
- Point out: Clean UI, mobile-responsive design

**3. Demonstrate File Transfer:**
- **Laptop 1:** Upload a photo/document (< 100 MB)
- **Laptop 2 (or phone):** Show it appearing in download list
- **Download it** to complete the round-trip transfer

**4. Highlight Technical Features:**
- "Uses Flask backend with RESTful API"
- "Single-file architecture for simplicity"
- "Deployed on PythonAnywhere with WSGI configuration"
- "Mobile-responsive design with CSS media queries"
- "Real-time upload progress with XMLHttpRequest"

**5. Discuss Trade-offs:**
- "Free tier has ~100 MB upload limit"
- "For larger files, I designed a local network mode using WiFi speeds (like USB transfer)"
- "Shows understanding of deployment constraints and optimization strategies"

### File Size Recommendations for Demo
- ✅ **Best:** Images (1-10 MB), Documents (< 5 MB), Small videos (< 50 MB)
- ⚠️ **Risky:** Large videos (> 100 MB) may timeout on PythonAnywhere
- 💡 **Alternative:** For large file demo, run locally and show WiFi-speed transfer

### Pre-Demo Checklist
- [ ] Open site 5-10 minutes before demo (wake up from cold start)
- [ ] Test upload/download to ensure it's working
- [ ] Have demo files ready (< 100 MB each)
- [ ] Charge phone for mobile demonstration
- [ ] Prepare GitHub repo link: https://github.com/UsamaBarkat/local-file-transfer

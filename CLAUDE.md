# File Transfer Application

## Project Overview
A web-based file transfer tool built with Python/Flask. Supports **bidirectional** file transfer (upload and download) with both **local network** and **internet accessibility**. Now deployed live on PythonAnywhere!

## Tech Stack
- **Backend:** Python 3, Flask
- **Frontend:** Vanilla HTML/CSS/JS (inline in `file_server.py` via `render_template_string`)
- **Deployment:** PythonAnywhere (free tier)
- **Production Server:** Gunicorn (for cloud deployment)
- **No database** — files are saved directly to disk
  - Local: Uploads saved to `~/ReceivedFiles`, files shared from `~/SharedFiles`
  - Cloud: Uploads saved to `/home/usamanizamani/local-file-transfer/ReceivedFiles`

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
- Flask dev server is intentional — this is a LAN-only tool, not a production web app
- Server binds to `0.0.0.0:5000` to be accessible from other devices on the network
- Auto-detects local IP via UDP socket trick (`get_local_ip()`)
- Tabbed UI: "Upload to Server" and "Download from Server" tabs
- Download section uses `data-` attributes + event delegation (NOT inline onclick) to avoid Python/Jinja2 string escaping issues with backslashes
- ZIP downloads use `tempfile` + `zipfile` to create on-the-fly archives

## Current Features
- **Upload:** Drag & drop or browse files, multi-file support, real-time progress bar
- **Download:** Browse shared folders with breadcrumb navigation, download individual files, download entire folders as ZIP
- **Folder browsing:** `/files?path=` API supports subfolder navigation with path traversal protection
- **ZIP download:** `/download-zip?path=` zips any folder on-the-fly for one-click download

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
- No `secure_filename()` on uploaded files
- No chunked upload — large files buffered in memory
- No authentication — anyone on the network can upload/download
- ZIP creation for very large folders may be slow (done synchronously)

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

**Decision Log:**
- Evaluated Render (requires credit card, potential billing risks)
- Chose PythonAnywhere (no credit card, zero billing risk, beginner-friendly)
- Successfully deployed with WSGI configuration

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
- Mobile-responsive improvements
- File preview capabilities

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

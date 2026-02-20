# File Transfer Application

## Project Overview
A local network file transfer web tool built with Python/Flask. Allows transferring large files (up to 15 GB) between laptops on the same WiFi network via a browser-based UI.

## Tech Stack
- **Backend:** Python 3, Flask
- **Frontend:** Vanilla HTML/CSS/JS (inline in `file_server.py` via `render_template_string`)
- **No database** — files are saved directly to disk at `~/ReceivedFiles`

## Project Structure
- `file_server.py` — Single-file application (Flask server + embedded HTML/CSS/JS template)
- `README.md` — Project documentation
- `test_upload.txt` — Test file for upload testing

## Key Design Decisions
- Single-file architecture: entire app lives in `file_server.py` for simplicity and portability
- Flask dev server is intentional — this is a LAN-only tool, not a production web app
- Server binds to `0.0.0.0:5000` to be accessible from other devices on the network
- Auto-detects local IP via UDP socket trick (`get_local_ip()`)

## Running
```bash
pip install flask
python file_server.py
```

## Known Limitations
- No `secure_filename()` on uploaded files
- No chunked upload — large files buffered in memory
- No authentication — anyone on the network can upload

## Future Roadmap (Planned)
The goal is to evolve this into a full internet-accessible file transfer tool. Planned approach in phases:

### Phase 1 — Improve Current Tool
- Add chunked/streaming uploads (support 50 GB+ files)
- Add file download capability (bidirectional transfer)
- Add `secure_filename()` and security fixes
- Polish the UI for ease of use

### Phase 2 — Internet Accessibility
- Use ngrok (free tunnel) to expose local server to the internet
- Anyone with the link can access — no local network restriction

### Phase 3 — Standalone Packaging
- Package as `.exe` so end users don't need Python/Flask installed

### Phase 4 (Optional) — Cloud or P2P
- Evaluate cloud deployment or WebRTC peer-to-peer for always-on access

## User Notes
- User is a beginner with no IT/AI background — keep explanations simple and step-by-step
- Guide through decisions, explain the "why" behind changes

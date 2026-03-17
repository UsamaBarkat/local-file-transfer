# Quick Reference Guide

## Your Live App

**URL:** https://usamanizamani.pythonanywhere.com

Share this URL with friends/family to let them upload/download files!

---

## Monthly Maintenance (IMPORTANT!)

Every month, you need to keep your app alive:

1. Go to: https://www.pythonanywhere.com
2. Log in with username: `usamanizamani`
3. Click **"Web"** tab
4. Click the green button: **"Run until 1 month from today"**
5. Done! Your app will run for another month.

**📧 Reminder:** PythonAnywhere will email you 1 week before expiry.

---

## How to Share Files

### Method 1: Let Others Upload TO You
1. Share your URL: https://usamanizamani.pythonanywhere.com
2. They open it in their browser
3. They upload files
4. Files are saved to your server

### Method 2: Share Files FROM You to Others
1. Log into PythonAnywhere: https://www.pythonanywhere.com
2. Click **"Files"** tab
3. Navigate to: `local-file-transfer` → `SharedFiles`
4. Click **"Upload a file"** button
5. Upload your files
6. Share your URL with people
7. They click "Download from Server" tab
8. They download your files!

---

## Quick Links

| What | Link |
|------|------|
| Your Live App | https://usamanizamani.pythonanywhere.com |
| PythonAnywhere Login | https://www.pythonanywhere.com |
| GitHub Repository | https://github.com/UsamaBarkat/local-file-transfer |
| Your GitHub Profile | https://github.com/UsamaBarkat |

---

## Storage Limits

- **Total Storage:** 512 MB
- **Check Usage:** PythonAnywhere → Files tab → see disk usage at top
- **Clean Up:** Delete old files from `ReceivedFiles` folder when full

---

## Troubleshooting

### App Not Loading?
1. Check if it's been more than 1 month (click the monthly button)
2. Wait 60 seconds (might be waking up)
3. Check error log: PythonAnywhere → Web tab → Error log

### Can't Upload Files?
1. Check if storage is full (512 MB limit)
2. Try smaller files first
3. Check error log

### Forgot Password?
- Use password reset on PythonAnywhere login page

---

## Common Tasks

### Delete Uploaded Files
1. PythonAnywhere → Files tab
2. Go to: `local-file-transfer/ReceivedFiles`
3. Click file → Delete

### Check Who Uploaded
- Currently no tracking (add this feature later?)

### Change App Settings
- Edit `file_server.py` locally
- Push to GitHub
- PythonAnywhere → Web tab → Reload

---

## Security Notes

⚠️ **Currently:** Anyone with the URL can upload/download (no password)

**Recommendations:**
- Only share URL with trusted people
- Don't post URL publicly
- Monitor storage regularly

**Future:** Add password protection for better security

---

## Project Files Explained

| File | Purpose |
|------|---------|
| `file_server.py` | Main application code |
| `requirements.txt` | Python dependencies |
| `CLAUDE.md` | Project context & history |
| `MEMORY.md` | Session progress tracking |
| `DEPLOYMENT_HISTORY.md` | Detailed deployment steps |
| `QUICK_REFERENCE.md` | This file - quick help guide |
| `README.md` | Project documentation |

---

## Need Help?

1. Check `MEMORY.md` for what we've done
2. Check `DEPLOYMENT_HISTORY.md` for deployment details
3. Check error logs on PythonAnywhere
4. Ask Claude for help!

---

## Future Features to Add

Want to add these? Ask Claude!

- [ ] Password protection
- [ ] Delete button for files
- [ ] File expiry (auto-delete old files)
- [ ] Custom colors/branding
- [ ] Email notifications
- [ ] File preview
- [ ] Upload size limits

---

**Last Updated:** March 17, 2026
**Status:** ✅ App is live and working!

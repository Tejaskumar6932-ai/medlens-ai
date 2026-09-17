"""
MedLens GitHub Auto-Deployer
Uploads all project files directly to GitHub using the REST API.
No Git installation required!

Usage:
    python github_deploy.py <YOUR_GITHUB_TOKEN> <YOUR_GITHUB_USERNAME>

Get a token at: https://github.com/settings/tokens/new
  - Select scopes: 'repo' (full access)
"""

import sys
import os
import base64
import json
import requests

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

REPO_NAME = "medlens-ai"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Files and folders to include
INCLUDE_EXTENSIONS = {'.py', '.html', '.css', '.js', '.txt', '.yaml', '.md', '.svg'}
EXCLUDE_DIRS = {'__pycache__', '.git', 'node_modules', '.env'}

def get_all_files():
    """Walk the medlens directory and collect all deployable files."""
    files = {}
    for root, dirs, filenames in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext in INCLUDE_EXTENSIONS or filename in {'Procfile', 'Dockerfile'}:
                full_path = os.path.join(root, filename)
                rel_path = os.path.relpath(full_path, BASE_DIR).replace("\\", "/")
                files[rel_path] = full_path
    return files

def create_repo(token, username):
    """Create the GitHub repository."""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Check if repo already exists
    r = requests.get(f"https://api.github.com/repos/{username}/{REPO_NAME}", headers=headers)
    if r.status_code == 200:
        print(f"✅ Repo already exists: https://github.com/{username}/{REPO_NAME}")
        return True
    
    # Create new repo
    data = {
        "name": REPO_NAME,
        "description": "MedLens - AI Medical Prescription & Lab Report Decoder (Hackathon Project)",
        "private": False,
        "auto_init": False
    }
    r = requests.post("https://api.github.com/user/repos", headers=headers, json=data)
    if r.status_code == 201:
        print(f"✅ Repository created: https://github.com/{username}/{REPO_NAME}")
        return True
    else:
        print(f"❌ Failed to create repo: {r.status_code} - {r.text}")
        return False

def upload_file(token, username, file_path, content_path):
    """Upload a single file to GitHub via the Contents API."""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    with open(content_path, 'rb') as f:
        content = base64.b64encode(f.read()).decode('utf-8')
    
    # Check if file exists to get its SHA (needed for updates)
    url = f"https://api.github.com/repos/{username}/{REPO_NAME}/contents/{file_path}"
    existing = requests.get(url, headers=headers)
    
    data = {
        "message": f"Add {file_path}",
        "content": content
    }
    
    if existing.status_code == 200:
        data["sha"] = existing.json()["sha"]
        data["message"] = f"Update {file_path}"
    
    r = requests.put(url, headers=headers, json=data)
    if r.status_code in (200, 201):
        return True
    else:
        print(f"  ⚠️  Failed to upload {file_path}: {r.status_code}")
        return False

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        print("\nExample:")
        print("  python github_deploy.py ghp_yourTokenHere yourusername")
        sys.exit(1)
    
    token = sys.argv[1]
    username = sys.argv[2]
    
    print("="*60)
    print("  🚀 MedLens GitHub Auto-Deployer")
    print("="*60)
    
    # Step 1: Create repo
    print(f"\n📦 Creating repository '{REPO_NAME}' on GitHub...")
    if not create_repo(token, username):
        sys.exit(1)
    
    # Step 2: Upload all files
    files = get_all_files()
    print(f"\n📁 Uploading {len(files)} files...\n")
    
    success = 0
    for rel_path, full_path in files.items():
        print(f"  ⬆️  {rel_path}", end=" ... ", flush=True)
        if upload_file(token, username, rel_path, full_path):
            print("✅")
            success += 1
        
    print(f"\n{'='*60}")
    print(f"✅ Uploaded {success}/{len(files)} files successfully!")
    print(f"\n🔗 Your GitHub repo: https://github.com/{username}/{REPO_NAME}")
    print(f"\n🌐 Next step — Deploy to Render (free):")
    print(f"  1. Go to https://render.com and sign up with GitHub")
    print(f"  2. New → Web Service → Select '{REPO_NAME}' repo")
    print(f"  3. Build Command:  pip install -r requirements.txt")
    print(f"  4. Start Command:  uvicorn server:app --host 0.0.0.0 --port $PORT")
    print(f"  5. Click Create → Wait 2 mins → Live URL! 🎉")
    print("="*60)

if __name__ == "__main__":
    main()

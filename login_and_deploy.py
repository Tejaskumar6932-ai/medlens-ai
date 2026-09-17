import subprocess
import time
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

GH_EXE = r'C:\Program Files\GitHub CLI\gh.exe'

def run():
    print("="*60)
    print("  Starting GitHub Login via Device Flow")
    print("="*60)
    
    # Start gh auth login
    proc = subprocess.Popen(
        [GH_EXE, 'auth', 'login', '-h', 'github.com', '-p', 'https', '-s', 'repo', '-w'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    # Read output to get the one-time code
    code = None
    url = "https://github.com/login/device"
    start_time = time.time()
    
    while time.time() - start_time < 10:
        line = proc.stderr.readline()
        if not line:
            line = proc.stdout.readline()
        if line:
            print(line.strip())
            if "One-time code" in line:
                # Extract code between parentheses
                parts = line.split("(")
                if len(parts) > 1:
                    code = parts[1].split(")")[0].strip()
                    break
        time.sleep(0.2)
    
    if code:
        print("\n" + "#"*60)
        print(f"  >>> YOUR ONE-TIME CODE IS:  {code}  <<<")
        print(f"  >>> OPEN: https://github.com/login/device <<<")
        print("#"*60 + "\n")
        sys.stdout.flush()
    
    # Wait for completion (up to 5 minutes)
    proc.wait(timeout=300)
    print("GitHub login finished with code:", proc.returncode)
    
    if proc.returncode == 0:
        print("Successfully logged into GitHub!")
        # Fetch token
        t_proc = subprocess.run([GH_EXE, 'auth', 'token'], capture_output=True, text=True)
        token = t_proc.stdout.strip()
        
        # Run github_deploy.py
        medlens_dir = os.path.dirname(os.path.abspath(__file__))
        deploy_script = os.path.join(medlens_dir, 'github_deploy.py')
        deploy_proc = subprocess.run(
            [sys.executable, deploy_script, token, 'Tejaskumar6932-ai'],
            capture_output=True,
            text=True
        )
        print(deploy_proc.stdout)
        print(deploy_proc.stderr)
    else:
        print("Login failed or timed out.")

if __name__ == '__main__':
    run()

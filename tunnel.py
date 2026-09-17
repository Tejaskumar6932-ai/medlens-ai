"""
MedLens Live Tunnel
Generates an instant public HTTPS URL for your MedLens app
so judges or friends can open it on their phones right now.
"""
import subprocess
import sys

print("="*60)
print("  🚀 Starting MedLens Live Public Tunnel...")
print("="*60)
print("Connecting via secure tunnel. You will receive a public HTTPS link...")
print("Press Ctrl+C to stop sharing.\n")

try:
    cmd = ["ssh", "-R", "80:localhost:8000", "nokey@localhost.run"]
    subprocess.run(cmd)
except KeyboardInterrupt:
    print("\nTunnel stopped.")
except Exception as e:
    print(f"Error starting tunnel: {e}")

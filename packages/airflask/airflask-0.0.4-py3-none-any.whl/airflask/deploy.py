import os
import subprocess
import socket

def get_public_ip():
    """Get the public IP of the server."""
    try:
        return subprocess.check_output(["curl", "-s", "https://checkip.amazonaws.com"]).decode().strip()
    except Exception:
        return "Unknown (check your network settings)"

def run_deploy(app_path):
    """Deploy a Flask app with Gunicorn and Nginx on a Linux VPS."""
    
    app_name = os.path.basename(os.path.abspath(app_path))
    service_file = f"/etc/systemd/system/{app_name}.service"
    nginx_conf = f"/etc/nginx/sites-available/{app_name}"
    nginx_link = f"/etc/nginx/sites-enabled/{app_name}"
    
    print(f"📦 Deploying {app_name}...")

    # 1️⃣ Install required packages
    print("🔧 Installing dependencies...")
    subprocess.run(["sudo", "apt", "update"])
    subprocess.run(["sudo", "apt", "install", "-y", "python3-venv", "python3-pip", "nginx"])

    # 2️⃣ Set up virtual environment
    venv_path = os.path.join(app_path, "venv")
    print("🐍 Creating virtual environment...")
    subprocess.run(["python3", "-m", "venv", venv_path])
    
    # 3️⃣ Install dependencies inside venv
    print("📦 Installing Flask and Gunicorn...")
    subprocess.run([f"{venv_path}/bin/pip", "install", "flask", "gunicorn"], cwd=app_path)

    # 4️⃣ Create Gunicorn systemd service
    service_config = f"""[Unit]
Description=Gunicorn instance to serve {app_name}
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory={app_path}
ExecStart={venv_path}/bin/gunicorn --workers 3 --bind unix:{app_path}/{app_name}.sock wsgi:app

[Install]
WantedBy=multi-user.target
"""
    with open("service_file.tmp", "w") as f:
        f.write(service_config)
    subprocess.run(["sudo", "mv", "service_file.tmp", service_file])
    subprocess.run(["sudo", "systemctl", "daemon-reload"])
    subprocess.run(["sudo", "systemctl", "start", app_name])
    subprocess.run(["sudo", "systemctl", "enable", app_name])

    # 5️⃣ Set up Nginx
    nginx_config = f"""server {{
    listen 80;
    server_name _;
    location / {{
        include proxy_params;
        proxy_pass http://unix:{app_path}/{app_name}.sock;
    }}
}}"""
    with open("nginx_conf.tmp", "w") as f:
        f.write(nginx_config)
    subprocess.run(["sudo", "mv", "nginx_conf.tmp", nginx_conf])
    subprocess.run(["sudo", "ln", "-s", nginx_conf, nginx_link])
    subprocess.run(["sudo", "systemctl", "restart", "nginx"])

    # 6️⃣ Get server IP and print it
    ip_address = get_public_ip()
    print(f"✅ Deployment completed! App is live at: http://{ip_address}")


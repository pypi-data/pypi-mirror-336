from fabric import Connection, task
import os
from pathlib import Path
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
import tempfile

load_dotenv()

# Configuration dictionary (renamed to CONFIG to avoid confusion)
CONFIG = {
    "host": os.getenv("HOST"),
    "user": os.getenv("USER"), 
    "app_name": os.getenv("APP_NAME"),
    "domain": os.getenv("DOMAIN"),
    "repo_url": os.getenv("REPO_URL"),
    "project_path": os.getenv("PROJECT_PATH"),
    "venv_path": os.getenv("VENV_PATH"),
    "branch": os.getenv("BRANCH"),
    "github_deploy_key": os.getenv("GITHUB_DEPLOY_KEY"),
    "port": os.getenv("PORT", "8766"),  # Default to 8766 if not specified
}

# Set up Jinja2 environment
template_env = Environment(loader=FileSystemLoader("templates"))

# Helper function to get a connection
def get_connection():
    return Connection(
        host=CONFIG["host"],
        user=CONFIG["user"],
        connect_kwargs={"key_filename": os.path.expanduser("~/.ssh/MEGA_PC")},
    )

# Helper function to wrap commands with SSH agent
def ssh_agent_run(conn, command):
    return conn.run(
        f"eval $(ssh-agent -s) && ssh-add '{CONFIG['github_deploy_key']}' && {command}",
        hide=True,
    )

# Helper function to check the /health endpoint
def check_health_endpoint(conn):
    print(f"🩺 Checking /health endpoint at https://{CONFIG['domain']}/health...")
    result = conn.run(
        f"curl -s -o /dev/null -w '%{{http_code}}' https://{CONFIG['domain']}/health",
        warn=True,
    )
    if result.ok and result.stdout.strip() == "200":
        print(f"✅ Health check passed: HTTP 200 OK")
    else:
        print(
            f"⚠️ Health check failed: HTTP {result.stdout.strip() if result.stdout else 'unknown'}"
        )
        raise Exception(
            f"Health endpoint check failed for https://{CONFIG['domain']}/health"
        )

# Helper function to render and upload templates
def render_and_upload_template(conn, template_name, dest_path):
    template = template_env.get_template(template_name)
    rendered_content = template.render(**CONFIG)
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(rendered_content.encode("utf-8"))
        temp_file_path = temp_file.name
    try:
        conn.put(temp_file_path, dest_path)
    finally:
        os.unlink(temp_file_path)

@task
def setup(c):
    """Initial setup: clones repo, sets up virtual env, configures services, sets up SSL, and checks health."""
    print(f"🛠️ Setting up {CONFIG['app_name']} on {CONFIG['host']}...")
    conn = get_connection()

    conn.sudo(
        f"mkdir -p {CONFIG['project_path']} && chown {CONFIG['user']}:{CONFIG['user']} {CONFIG['project_path']}"
    )

    app_path = f"/var/www/{CONFIG['app_name']}"
    conn.sudo(f"mkdir -p {app_path}")
    conn.sudo(f"chown -R www-data:www-data {app_path}")

    if not conn.run(f"test -d {CONFIG['project_path']}/.git", warn=True).ok:
        print("📥 Cloning repository...")
        project_parent = str(Path(CONFIG["project_path"]).parent)
        ssh_agent_run(
            conn,
            f"cd \"{project_parent.replace('\\', '/')}\" && git clone {CONFIG['repo_url']} \"{Path(CONFIG['project_path']).name}\"",
        )

    if not conn.run(f"test -f {CONFIG['venv_path']}/bin/activate", warn=True).ok:
        print("🐍 Creating virtual environment...")
        conn.run(f"python3 -m venv '{CONFIG['venv_path']}'")

    deploy(c)

    print("🔒 Checking and installing Certbot...")
    if not conn.run("command -v certbot", warn=True).ok:
        conn.sudo("apt-get update")
        conn.sudo("apt-get install -y certbot python3-certbot-nginx")

    cert_path = f"/etc/letsencrypt/live/{CONFIG['domain']}"
    if not conn.run(f"test -d {cert_path}", warn=True).ok:
        print(f"🔐 Generating SSL certificate for {CONFIG['domain']}...")
        conn.sudo(
            f"certbot --nginx -d {CONFIG['domain']}"
        )
    else:
        print(
            f"ℹ️ SSL certificate already exists for {CONFIG['domain']}, skipping Certbot setup."
        )

    print("🔌 Enabling service...")
    conn.sudo(f"systemctl enable {CONFIG['app_name']}")

    check_health_endpoint(conn)

    print("✅ Setup completed!")

@task
def deploy(c):
    """Deploys code, installs dependencies, links configs, restarts services, and checks health."""
    print(f"🚀 Deploying {CONFIG['app_name']} to {CONFIG['host']}...")
    conn = get_connection()

    nginx_dest = f"/etc/nginx/sites-enabled/{CONFIG['domain']}"
    systemd_dest = f"/etc/systemd/system/{CONFIG['app_name']}.service"

    with conn.cd(CONFIG["project_path"]):
        print("📥 Pulling latest code...")
        conn.run(f"git config --global --add safe.directory {CONFIG['project_path']}")
        ssh_agent_run(conn, f"git fetch origin {CONFIG['branch']} -v")
        ssh_agent_run(conn, f"git checkout {CONFIG['branch']}")
        ssh_agent_run(conn, f"git pull origin {CONFIG['branch']} -v")

        print("📦 Installing dependencies...")
        conn.run(
            f"source '{CONFIG['venv_path']}/bin/activate' && pip install -r requirements.txt"
        )

    app_path = f"/var/www/{CONFIG['app_name']}"
    conn.sudo(f"mkdir -p '{app_path}'")
    conn.sudo(f"chown -R www-data:www-data '{app_path}'")

    print("🔗 Linking configuration files...")
    print("Rendering and uploading Nginx configuration...")
    nginx_source = f"{CONFIG['project_path']}/nginx/{CONFIG['domain']}"
    conn.sudo(f"mkdir -p '{CONFIG['project_path']}/nginx'")
    render_and_upload_template(conn, "nginx_config.j2", nginx_source)
    conn.sudo(f"ln -sf '{nginx_source}' '{nginx_dest}'")
    print(f"✅ Nginx configuration linked: {nginx_dest}")

    print("Testing Nginx configuration...")
    result = conn.sudo("nginx -t", warn=True)
    if result.failed:
        print("⚠️ Nginx configuration test failed!")
        raise Exception("Nginx configuration test failed")

    print("Rendering and uploading systemd service...")
    systemd_source = f"{CONFIG['project_path']}/systemd/{CONFIG['app_name']}.service"
    conn.sudo(f"mkdir -p '{CONFIG['project_path']}/systemd'")
    render_and_upload_template(conn, "systemd_service.j2", systemd_source)
    conn.sudo(f"ln -sf '{systemd_source}' '{systemd_dest}'")
    print(f"✅ Systemd service linked: {systemd_dest}")

    print("Reloading systemd daemon...")
    conn.sudo("systemctl daemon-reload")
    print("✅ Systemd daemon reloaded")

    print("🔄 Restarting services...")
    conn.sudo(f"systemctl restart {CONFIG['app_name']}")
    conn.sudo("systemctl reload nginx")

    print("🔍 Checking service status...")
    conn.sudo(f"systemctl status {CONFIG['app_name']} --no-pager")

    check_health_endpoint(conn)

    print("✅ Deployment completed!")

@task
def env_task(c):  # Renamed to avoid shadowing built-in `env`
    """Upload .env file to the server."""
    conn = get_connection()
    conn.put('.env', f'{CONFIG["project_path"]}/app/.env')
    conn.sudo(f'chown {CONFIG["user"]}:{CONFIG["user"]} {CONFIG["project_path"]}/app/.env')
    conn.sudo(f'chmod 600 {CONFIG["project_path"]}/app/.env')

@task
def logs(c):
    """View application logs."""
    conn = get_connection()
    conn.sudo(f'journalctl -u {CONFIG["app_name"]} -f')
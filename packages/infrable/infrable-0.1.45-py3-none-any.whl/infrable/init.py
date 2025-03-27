from pathlib import Path

INFRA_PY = '''
import typer
from infrable import Host, Meta, Service, Switch, concurrentcontext, files, paths, readfile
from modules import mycloud

# To quickly find the configuration file template on GitHub
template_prefix = "https://github.com/username/repository/blob/main"


# Environments/ ----------------------------------------------------------------
dev = "dev"
beta = "beta"
prod = "prod"

environments = {dev, beta, prod}
env = Switch(environments, init=dev)
current_env = env()
# /Environments ----------------------------------------------------------------


# Clouds/ ----------------------------------------------------------------------
cloud = mycloud.MyCloud(secret_api_key=readfile("secrets/mycloud/secret_api_key"))
cloud.typer = mycloud.workflows
# /Clouds ----------------------------------------------------------------------


# Hosts/ -----------------------------------------------------------------------
dev_host = Host(fqdn="dev.example.com", ip="127.0.0.1")
beta_host = Host(fqdn="beta.example.com", ip="127.0.0.2")
prod_host = Host(fqdn="prod.example.com", ip="127.0.0.3")

managed_hosts = env(
    dev=[dev_host],
    beta=[beta_host],
    prod=[prod_host],
)
# /Hosts -----------------------------------------------------------------------


# Services/ --------------------------------------------------------------------
web = Service(
    host=env.strict(dev=dev_host, beta=beta_host, prod=prod_host),
    meta=Meta(secret_key=readfile("secrets/web/secret_key")),
    port=8080,
)

nginx = Service(port=80, host=web.host)
# /Services --------------------------------------------------------------------


# Tasks/ -----------------------------------------------------------------------
nginx.typer = typer.Typer(help="Nginx specific tasks.")
@nginx.typer.command(name="reload")
def reload_nginx():
    """[TASK] Reload nginx: infrable nginx reload"""

    assert nginx.host, "Service must have a host to reload"

    # Run: sudo nginx -t
    nginx.host.remote().sudo.nginx("-t")

    # Run: sudo systemctl reload nginx
    nginx.host.remote().sudo.systemctl.reload.nginx()
# Tasks/ -----------------------------------------------------------------------

# Workflows/ -----------------------------------------------------------------------
deploy = typer.Typer(help="Deployment workflows.")
@deploy.command(name="nginx")
def deploy_nginx():
    """[WORKFLOW] Deploy nginx files: infrable deploy nginx"""

    # Deploy the Nginx configuration files
    files.deploy(paths.templates / "nginx")

    # Test the Nginx configuration and reload the service concurrently
    cmd = "sudo nginx -t && sudo systemctl reload nginx && echo success || echo failed"
    fn = lambda host: (host, host.remote().sudo(cmd))
    with concurrentcontext(fn, files.affected_hosts()) as results:
        for host, result in results:
            print(f"{host}: {result}")
# /Workflows -----------------------------------------------------------------------
'''.strip()

NGINX_PROXY_PARAMS_TEMPLATE = """
# vim: syn=nginx

# ---
# src: {{ template_prefix }}/{{ _template.src }}
# dest: {{ nginx.host }}:/etc/nginx/proxy_params
# chmod: 644
# chown: root:root
# ---
proxy_set_header Host $http_host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
""".strip()

NGINX_WEB_TEMPLATE = """
# vim: syn=nginx

# ---
# src: {{ template_prefix }}/{{ _template.src }}
# dest: {{ nginx.host }}:/etc/nginx/sites-enabled/web
# chmod: 644
# chown: root:root
# ---

server {
    listen {{ nginx.port }};
    listen [::]:{{ nginx.port }};

    server_name {{ nginx.host.fqdn }} www.{{ nginx.host.fqdn }};

    location / {
        proxy_pass http://127.0.0.1:{{ web.port }};
        include proxy_params;
    }

    location /robots.txt {
        root /var/www/html;
    }
}
""".strip()

NGINX_ROBOTS_TXT_TEMPLATE = """
#!/usr/bin/env bash

# vim: syn=sh

# ---
# src: {{ template_prefix }}/{{ _template.src }}
# dest: {{ nginx.host }}:/root/init/robots.txt.sh
# execute: true
# ---

set -euxo pipefail

if [ ! -d /var/www/html ]; then
    mkdir -p /var/www/html
fi

cat > /var/www/html/robots.txt <<EOF
User-agent: *
Disallow: {% if current_env != prod %}/{% endif %}
EOF
"""

HOSTNAME_TEMPLATE = """
# vim: syn=ansible.vim

# ---
# src: {{ template_prefix }}/{{ _template.src }}
# dest:
#   {% for host in managed_hosts %}
#   {% if host.fqdn %}
#   - loc: {{ host }}:/etc/hostname
#     ctx:
#       hostname: {{ host.fqdn.split(".")[0] }}
#   {% endif %}
#   {% endfor %}
# chmod: 644
# chown: root:root
# ---
{{ hostname }}
""".strip()

MYCLOUD_MODULE = '''
from dataclasses import dataclass
from typer import Typer
from infrable import Host, infra

@dataclass
class MyCloud:
    """MyCloud Python library."""

    secret_api_key: str
    typer: Typer | None = None

    def provision_ubuntu_host(self, fqdn: str):
        ip = self.api.create_ubuntu_host(fqdn)
        return MyCloudUbuntuHost(fqdn=fqdn, ip=ip)

@dataclass
class MyCloudUbuntuHost(Host):
    """MyCloud's customized Ubuntu server."""

    def setup(self):
        self.install_mycloud_agent()

    def install_mycloud_agent(self):
        raise NotImplementedError

workflows = Typer()

@workflows.command()
def provision_ubuntu_host(fqdn: str, setup: bool = True):
    """[WORKFLOW] Provision Ubuntu host."""

    # Get the MyCloud instance from infra.py
    cloud = next(iter(infra.item_types[MyCloud].values()))

    # Provision the host
    host = cloud.provision_ubuntu_host(fqdn)
    if setup:
        host.setup()

    name = fqdn.split(".")[0].replace("-", "_")
    print("Add the host to the infra.py file.")
    print(f"{name} = {repr(host)}")
'''.strip()

FILES = {
    "infra.py": INFRA_PY,
    "templates/hostname/hostname.j2": HOSTNAME_TEMPLATE,
    "templates/nginx/proxy_params.j2": NGINX_PROXY_PARAMS_TEMPLATE,
    "templates/nginx/web.j2": NGINX_WEB_TEMPLATE,
    "templates/nginx/robots.txt.sh.j2": NGINX_ROBOTS_TXT_TEMPLATE,
    "modules/mycloud.py": MYCLOUD_MODULE,
}


def init():
    for filename, content in FILES.items():
        path = Path(filename)
        if path.exists() and path.read_text().strip():
            print(f"Skipping {path}, Exists.")
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.strip())
        print(f"Created {path}.")

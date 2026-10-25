# /// script
# dependencies = [
#     "python-on-whales",
#     "python-dotenv",
#     "pyorca @ git+https://github.com/mathakim29/pyorca.git",
# ]
# ///

from pyorca import Orca


def deploy(orca: Orca):
    # 1. Ensure required local directories exist
    orca.ensure_dirs(["./public", "./server", "./app"])

    # 2. Include MySQL database service
    orca.include({
        "image": "mysql:8.0",
        "name": "mysql",
        "restart": "unless-stopped",
        "publish": [("3306", "3306")],
        "envs": {
            "MYSQL_ROOT_PASSWORD": "app",
            "MYSQL_DATABASE": "app",
            "MYSQL_USER": "app",
            "MYSQL_PASSWORD": "app",
        },
        "detach": True,
    })

    # 3. Wait for MySQL to accept connections
    orca.wait_for_port("localhost", 3306, timeout=30)

    # 4. Build the FrankenPHP image with PHP extensions
    orca.docker.build(".", file="Dockerfile", tags=orca.image_tag)

    # 5. Run your main Svelte/FrankenPHP application container
    orca.run({
        "restart": "unless-stopped",
        "publish": [
            ("8020", "80"),
            ("8443", "443"),
            ("3000", "3000"),
        ],
        "volumes": [
            ("./public", "/app/public", "Z"),
            ("./server", "/app/server", "Z"),
            ("./app", "/app/frontend", "Z"),
            ("node_modules", "/tmp/build/node_modules"),
            ("caddy_data", "/data"),
            ("caddy_config", "/config"),
        ],
        "envs": {
            "SERVER_NAME": "localhost",
            "DB_DRIVER": "mysql",
            "DB_HOST": "mysql",
            "DB_NAME": "app",
            "DB_USER": "app",
            "DB_PASSWORD": "app",
        },
        "detach": True,
        "command": [
            "sh",
            "-c",
            (
                "S='bun /app/setup.ts -i /app/frontend -o /app/dist -t' && "
                "$S && (watchexec -w /app -- $S > /app/watchexec.log 2>&1 &) && "
                "exec frankenphp run --config /etc/caddy/Caddyfile"
            ),
        ],
    })


if __name__ == "__main__":
    orca = Orca(app_name="app", image_tag="sveltephp:latest")
    
    # Keep explicit ports since you have standard web mappings
    orca.AUTOPORT = False

    # CLI Management Commands:
    #   uv run init.py up      -> starts network, MySQL, builds image, and launches app
    #   uv run init.py status  -> checks container health
    #   uv run init.py logs    -> streams app logs
    #   uv run init.py down    -> tears down stack
    orca.cli(deploy)
import jwt
import os
import requests
import subprocess
import time
import yaml


def load_config_file():
    print("\U000023f3 Loading config file 'config.yaml'")
    with open("config.yaml", "r") as stream:
        try:
            config = yaml.safe_load(stream)
            print("\U0000231B Loaded config file")
        except yaml.YAMLError as exc:
            print(f"\U00002620 {exc}")

    return config


def fetch_pubkey(config):
    pubkey_url = f"{config['zuul_protocol']}://{config['zuul_host']}/api/tenant/{config['tenant_name']}/key/{config['repo_name']}.pub"
    print(f"\U00002B07  Fetching public repo RSA key from {pubkey_url}")
    r = requests.get(pubkey_url, allow_redirects=True)
    open('key.pub', 'wb').write(r.content)
    print("\U00002705 Fetched public repo RSA key")
    return "key.pub"


def generate_jwt(config):
    print("\U0001F551 Generate JWT")
    return jwt.encode(
        {
            'sub': config['username'],
            'iss': 'zuul_secret_script',
            'aud': 'zuul.services.betacloud.xyz',
            'iat': int(time.time()),
            'exp': int(time.time() + 9),
            # this should only be required when performing other actions
            # 'zuul': {
            #     'admin': [config['tenant_name']]
            # }
        },
        config['zuul_secret'],
        algorithm='HS256'
    )


def generate_zuul_config(config, jwt_token):
    print("\U0001F5D2  Generate temporary zuul config")
    with open(".zuul.conf", "a") as stream:
        stream.write(f"[{config['tenant_name']}]\n")
        stream.write(f"url={config['zuul_host']}\n")
        stream.write(f"tenant={config['tenant_name']}\n")
        stream.write(f"auth_token={jwt_token}\n")

    return ".zuul.conf"


def run_client(config, zuul_config):
    print("\U0001F3CE  Running zuul client")
    result = subprocess.run(
        [
            "zuul-client",
            "-c", zuul_config,
            "--use-config", config['tenant_name'],
            "encrypt",
            "--public-key", "key.pub",
            "--tenant", config['tenant_name'],
            "--project", config['repo_name'],
            "--secret-name", config['secret_name'],
            "--field-name", config['field_name'],
            "--infile", config['input_file']
        ],
        capture_output=True,
        text=True
    )
    return result


def remove_file(file):
    os.remove(file)
    print(f"\U0001F4A5 Removed {file}")


def main():
    config = load_config_file()
    pubkey = fetch_pubkey(config)
    jwt_token = generate_jwt(config)
    zuul_config = generate_zuul_config(config, jwt_token)
    result = run_client(config, zuul_config)
    remove_file(pubkey)
    remove_file(zuul_config)
    print(result.stdout)


if __name__ == "__main__":
    main()

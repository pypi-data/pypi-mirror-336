[![Datalayer](https://assets.datalayer.tech/datalayer-25.svg)](https://datalayer.io)

[![Become a Sponsor](https://img.shields.io/static/v1?label=Become%20a%20Sponsor&message=%E2%9D%A4&logo=GitHub&style=flat&color=1ABC9C)](https://github.com/sponsors/datalayer)

# 🪐 🐳 Jupyter Docker

> Manage Docker from Jupyter.

Jupyter Docker allows you to manage Docker from JupyterLab.

Users view the current Docker Images, Containers, Volumes, Networks and Secret, start a Container from an Image and stop running Containers.

## Check your Docker

For macOS, you have to allow the default Docker socket to be used (requires password):

- https://github.com/gh640/wait-for-docker/issues/12#issuecomment-1551456057: One needs to enable "Enable default Docker socket (Requires password)" in "Advanced" section in Docker Desktop settings to make a symbolic link /var/run/docker.sock on startup.

- https://github.com/gh640/wait-for-docker/issues/12#issuecomment-1564061886: Also the item "Docker Inc" in System Settings → General → Login Items → Allow in the Background needs to be enabled (it's enabled by default).

Read also:

- https://github.com/docker/docker-py/issues/3059
- https://github.com/gh640/wait-for-docker/issues/12

## Develop

```bash
pip install -e .[test]
jupyter labextension develop . --overwrite
jupyter labextension list
jupyter server extension list
yarn jupyterlab
```

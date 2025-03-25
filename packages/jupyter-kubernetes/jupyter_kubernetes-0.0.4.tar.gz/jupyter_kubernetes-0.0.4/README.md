[![Datalayer](https://assets.datalayer.tech/datalayer-25.svg)](https://datalayer.io)

[![Become a Sponsor](https://img.shields.io/static/v1?label=Become%20a%20Sponsor&message=%E2%9D%A4&logo=GitHub&style=flat&color=1ABC9C)](https://github.com/sponsors/datalayer)

# 🪐 ☸️ Jupyter Kubernetes

> Manage Kubernetes from Jupyter.

Jupyter Kubernetes is a JupyterLab that allows you to manage Kubernetes from Jupyter. Users can visually access the Kurbernetes objects.

It is like the official [Kubernetes Dashboard](https://github.com/kubernetes/dashboard) (developed with Angular.js) but as React.js components and JupyterLab extension.

```bash
pip install -e .[test]
jupyter labextension develop . --overwrite
jupyter labextension list
jupyter server extension list
yarn jupyterlab
```

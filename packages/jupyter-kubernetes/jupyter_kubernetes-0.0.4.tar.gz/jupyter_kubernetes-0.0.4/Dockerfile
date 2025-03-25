# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

FROM python:3.11

RUN mkdir /opt/jupyter-kubernetes

WORKDIR /opt/jupyter-kubernetes

RUN pip install kazoo

COPY jupyter_kubernetes /opt/jupyter_kubernetes
RUN pip install -e ./jupyter_kubernetes

WORKDIR /opt/jupyter-kubernetes/editor

EXPOSE 9300

CMD ["python", "-m", "jupyter_kubernetes"]

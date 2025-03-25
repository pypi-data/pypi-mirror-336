# Copyright (c) Datalayer, Inc. https://datalayer.io
# Distributed under the terms of the MIT License.

FROM python:3.11

RUN mkdir /opt/jupyter-contents

WORKDIR /opt/jupyter-contents

RUN pip install kazoo

COPY jupyter_contents /opt/jupyter_contents
RUN pip install -e ./jupyter_contents

# COPY frontplane/dist.html /opt/jupyter-contents/index.html

WORKDIR /opt/jupyter-contents/editor

EXPOSE 9300

CMD ["python", "-m", "jupyter_contents"]

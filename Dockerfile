FROM prefecthq/prefect:3.4.19-python3.12
COPY requirements.txt /opt/prefect/prefect-demos/requirements.txt
RUN uv pip install -r /opt/prefect/prefect-demos/requirements.txt
COPY . /opt/prefect/prefect-demos/
WORKDIR /opt/prefect/prefect-demos/

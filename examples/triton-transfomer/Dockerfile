FROM python:3.9-slim AS runtime

# RUN apt-get update && apt-get install -y wget
# RUN wget -q https://repo.anaconda.com/miniconda/Miniconda3-py39_4.11.0-Linux-x86_64.sh -O ~/miniconda.sh
# RUN bash ~/miniconda.sh -b -p $HOME/miniconda
WORKDIR /usr/src

COPY . .
RUN --mount=type=cache,target=/root/.cache pip install --upgrade pip && pip install -r requirements.txt

# RUN pip install -e ./transfomer

RUN useradd kserve -m -u 1000 -d /home/kserve
USER 1000
CMD ["python", "-m", "model"]
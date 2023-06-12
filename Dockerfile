# Start your image with a node base image

FROM python:3.8-slim-buster

WORKDIR /app



# Copy local directories to the current local directory of our docker image (/app)


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python3", "GUI/GUI.py"]
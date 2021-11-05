This repo is to serve the deployment of the trained Named Entity Recognition (NER) model.

I added a minimal flask test application, to test the port forwarding, because I was not able to determine if the fastAPI project was working as intended.

Use the following 2 commands to build and run the prediction container accoridingly, to check that the container is running use `docker ps`

`docker build . -t NER-Service` 

- the build step will copy the whole `/app/` directory inside the container
- update pip to the latest version
- install the specified requirements from the `.txt`
- set entrypoint to run: `python flask_test.py` <= change the last line to use your app.py again
`docker run -p 5000:5000 NER-Service`
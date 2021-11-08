This repo is for the purpose of the deployment of the trained Named Entity Recognition (NER) model.

Use the following 2 commands to build and run the prediction container accoridingly, to check that the container is running use `docker ps`

`docker build . -t NER-Service` 

- the build step will copy the whole `/app/` directory inside the container
- update pip to the latest version
- install the specified requirements from the `.txt`
- set entrypoint to run: `python app.py` 
`docker run -p 5000:5000 NER-Service`
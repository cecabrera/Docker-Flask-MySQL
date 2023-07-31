# Web application using Flask and SQLite3, and deployment using docker-compose in Digital Ocean

Based on:
- [Aplicación web basada en Flask y MySQL, y despliegue con Docker y docker-compose en Digital Ocean](https://jaimesendraberenguer.medium.com/aplicaci%C3%B3n-web-basada-en-flask-y-mysql-y-despliegue-con-docker-y-docker-compose-en-digital-ocean-4754a400d4e3)
- [Blog post about creating a flask-mysql app with docker](https://stavshamir.github.io/python/dockerizing-a-flask-mysql-app-with-docker-compose/)
- [Building a Flask app with Docker | Learning Flask Ep. 24](https://pythonise.com/series/learning-flask/building-a-flask-app-with-docker-compose)

In this _Post_, I will take an existing simple web application based on ```Flask``` and ```sqlite3```, and deploy it with ```Docker``` and ```docker-compose```.

This repo is a fork from this repo: 

[jaisenbe58r/Docker-Flask-MySQL](https://github.com/jaisenbe58r/Docker-Flask-MySQL)

Project structure:
```
Project/
├── flask
│   ├── sql
│   │   ├── create
│   │   │   ├── data.sql
│   │   │   ├── department.sql
│   │   │   ├── hired_employees.sql
│   │   │   └── jobs.sql
│   │   ├── requirement1.py
│   │   └── requirement2.py
│   ├── src
│   │   ├── db
│   │   │   ├── init_db.py
│   │   │   ├── select_db.py
│   │   ├── requirements
│   │   │   ├── df_requirement1.py
│   │   │   └── df_requirement2.py
│   │   ├── readSQL.py
│   │   └── upload_csv.py
│   │── static
│   │   ├── css
│   │   ├── Excel
│   │   │   ├── departments.csv
│   │   │   ├── hired_employees.csv
│   │   │   └── jobs.csv
│   │   ├── js
│   │   └── myfont
│   ├── templates
│   │   ├── ExcelUpload.html
│   │   ├── requirement1.html
│   │   ├── requirement2.html
│   │   └── view_excel.html
│   ├── app.ini
│   ├── MyData.db
│   ├── requirements.txt
│   └── run.py
├── nginx
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml
├── README.md
├── start.sh
```

- ```flask/sql```: contains `SQL` queries to `create` and `select`
- ```flask/src```: contains the source code for Python modules (functions)
- ```flask/static/Excel```: contains the CSV files uploaded in the app
- ```flask/static/templates```: contains the HTML templates run by every endpoint

The Docker image for flask will be built from an existing image, python:3, which corresponds to a lightweight python3 image. Choose the working port, in this case, 56734, first, make sure you have an open port available to use in the configuration. To check if there is an available port, run the following command

    ```cmd
    sudo nc localhost 56734 < /dev/null; echo $?
    ```

    If the result of the previous command is 1, the port will be available and can be used. Otherwise, you will need to select a different port and repeat the procedure.

- The requirements.txt file is copied into the container so that it can be executed, and then the requirements.txt file is analyzed to install the specified dependencies. We will also copy the entire working directory of the repository into the image to later share it as an external volume.

- A working directory is created, and the entire repository is copied into it.

The ```app.ini``` file will contain the uWSGI configurations for our application. uWSGI is a deployment option for Nginx that serves as both a protocol and an application server. The application server can provide the uWSGI, FastCGI, and HTTP protocols.


```ini
[uwsgi]
wsgi-file = run.py
; This is the name of the variable
; in our script that will be called
callable = app
; We use the port 8080 which we will
; then expose on our Dockerfile
socket = :8080
; Set uWSGI to start up 5 workers
processes = 4
threads = 2
master = true
chmod-socket = 660
vacuum = true
die-on-term = true
```

This code defines the module from which the Flask application will be served, in this case, it is the ```run.py``` file. The ```callable``` option instructs uWSGI to use the instance of the app exported by the main application. The ```master``` option allows your application to keep running, reducing downtime even when the entire application is reloaded.

### Building the Nginx Image in Docker

Before implementing the construction of the Nginx container image, we will create our configuration file that will tell Nginx how to route traffic to uWSGI in our other container. The ```nginx.conf``` file will replace the ```/etc/nginx/conf.d/default.conf``` that the Nginx container implicitly includes. [Read more about Nginx conf files here.](http://nginx.org/en/docs/beginners_guide.html)

```conf
server {
    listen 80;
    location / {
        include uwsgi_params;
        uwsgi_pass flask:8080;
    }
}
```

The line ```uwsgi_pass flask:8080``` is using "flask" as the host to route the traffic. This is because we will configure ```docker-compose``` to connect our Flask and Nginx containers using ```flask``` as the hostname.

Our Dockerfile for Nginx will simply inherit the latest image of [Nginx from the Docker registry](https://hub.docker.com/_/nginx/), remove the default configuration file, and add the configuration file we just created during the build. We will name the file ```Dockerfile-nginx```.

```Dockerfile
# Dockerfile-nginx
FROM nginx:latest
# Nginx will listen on this port
# EXPOSE 80
# Remove the default config file that
# /etc/nginx/nginx.conf includes
RUN rm /etc/nginx/conf.d/default.conf
# We copy the requirements file in order to install
# Python dependencies
COPY nginx.conf /etc/nginx/conf.d/
```

### Creando el orquestador de contenedores docker-compose.yml

The file ```docker-compose.yml``` is created in the root directory of our project.:

```yml
version: "3.7"
services:
  flask:
    build: ./flask
    container_name: flask
    restart: always
    environment:
      - APP_NAME=MyFlaskApp
    expose:
      - 8080
```

```nginx``` service:

```yml
  nginx:
    build: ./nginx
    container_name: nginx
    restart: always
    ports:
      - "8003:80"
```

This small section tells ```docker-compose``` to map port ```8003``` of your local machine to port ```80``` of the Nginx container (which is the default port served by Nginx).

As implemented in the ```nginx.conf```, we route traffic from Nginx to uWSGI and vice versa by sending data through the ```flask``` as the hostname. This section creates a virtual hostname ```flask``` in our ```nginx``` container and configures the network so that we can route incoming data to our uWSGI application living in a different container.


## Deploy the app


The script ```start.sh``` is a shell script that will allow us to execute the construction of ```docker-compose.yml```, so that the containers run in the background mode.

```bash
#!/bin/bash
docker-compose up -d
```

The first line is called the _shebang_. It specifies that this is a bash file and will be executed as commands. The ```-d``` flag is used to start a container in daemon mode or as a background process.

To test the creation of Docker images and containers from the resulting images, run the following command:

```shell
sudo bash start.sh
```

Ahora ya puede visitar su aplicación en http://```your-domain:8003``` desde un navegador externo al servidor para ver la la aplicación en ejecución.

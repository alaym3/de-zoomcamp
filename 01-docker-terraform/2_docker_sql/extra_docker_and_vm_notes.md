docker run -it --entrypoint=bash python:3.9

Simple file that just uses python and installs pandas, with bash entrypoint:

FROM python:3.9

RUN pip install pandas

ENTRYPOINT ["bash"]

docker build -t test:pandas .
docker run -it test:pandas

Arguments test
import pandas as pd
import sys

print(sys.argv)

day = sys.argv[1]

print(f'Job finished successfully for day {day}.')

docker run -it test:pandas 2023-01-01

ssh-keygen -t rsa -f ~/.ssh/de_gcp -C am -b 2048

Your identification has been saved in /Users/alainamartinez/.ssh/de_gcp
Your public key has been saved in /Users/alainamartinez/.ssh/de_gcp.pub

- put public key on gcp

- create VM and find the external IP - 104.155.28.182. use the private key and your user.
  ssh -i ~/.ssh/de_gcp am@104.155.28.182

log in and configure the instance - download everything we need.

- download anaconda - use sudo . copy link wget https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-x86_64.sh
- download docker

need to add Host to ssh config file
Host de-zoomcamp
HostName 104.155.28.182
User am
IdentityFile ~/.ssh/de_gcp

so now all i have to do is type ssh de-zoomcamp and i am in.

source .bashrc will restart the ssh so you dont need to login and out.

we can use vscode to connect to the VM!. extension remote ssh. bottom left we can click the remote thing and remote ssh connect to host, choose de-zoomcamp.

add user to be able to run docker without sudo

download docker compose - need to make a new bin directory where all the executaibles will be.
https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-linux-x86_64 -O docker-compose

execution ability:
chmod +x docker-compose

to make it executable everywhere, not just bin, need to add it to the .bashrc executable.
export PATH="${HOME}/bin:${PATH}"

(base) am@de-zoomcamp:~/data-engineering-zoomcamp$ git branch -a

- main
  remotes/origin/HEAD -> origin/main
  remotes/origin/main
  remotes/origin/week1
  (base) am@de-zoomcamp:~/data-engineering-zoomcamp$ git checkout -b remotes/origin/week1

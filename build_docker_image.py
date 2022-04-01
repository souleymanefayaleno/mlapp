###############################################################################################
#                                Import libraries                                             #
###############################################################################################

import os


###############################################################################################
#                                definition of script functions                               #
###############################################################################################

def create_docker_image():
    # Install pre-requisites
    os.system("sudo yum update")
    os.system("sudo yum install tar")
    os.system("tar --version")

    # Download ubuntu:latest docker image
    os.system("sudo docker pull ubuntu:latest")

    # Create a Dockerfile for the frontend image and add its content
    os.system("sudo touch Dockerfile")
    os.system("sudo chmod 777 Dockerfile")
    os.system('echo "RUN apt-get update" >> Dockerfile')
    os.system('echo "FROM ubuntu:latest" >> Dockerfile')
    os.system('echo "RUN apt-get install -y python3-pip python3-dev" >> Dockerfile')
    os.system('echo "RUN cd /usr/local/bin" >> Dockerfile')
    os.system('echo "RUN ln -s /usr/bin/python3 python" >> Dockerfile')
    os.system('echo "RUN pip3 install --no-cache-dir tensorflow" >> Dockerfile')
    os.system('echo "RUN pip3 install streamlit" >> Dockerfile')
    os.system('echo "RUN pip3 install scikit-learn" >> Dockerfile')
    os.system('echo "RUN pip3 install matplotlib" >> Dockerfile')
    os.system('echo "RUN pip3 install seaborn" >> Dockerfile')
    os.system('echo "RUN pip3 install pandas" >> Dockerfile')
    os.system('echo "RUN pip3 install numpy" >> Dockerfile')
    os.system('echo "RUN pip3 install boto3" >> Dockerfile')

    os.system('echo "WORKDIR  ec2-user" >> Dockerfile')

    os.system('echo "COPY main.py ." >> Dockerfile')

    os.system('echo "EXPOSE 8501" >> Dockerfile')
    os.system('echo "CMD ["python3", "main.py"]" >> Dockerfile')

    os.system('echo "ENTRYPOINT ["python3 streamlit run", "main.py"]" >> Dockerfile')

    # Build docker image
    os.system("sudo docker build -t mlapp .")


###############################################################################################
#                                script execution                                             #
###############################################################################################

if __name__ == "__main__":
    create_docker_image()

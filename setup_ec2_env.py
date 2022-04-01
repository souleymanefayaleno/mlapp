###############################################################################################
#                                import of script libraries                                   #
###############################################################################################
import os


###############################################################################################
#                                definition of script functions                               #
###############################################################################################

# Install Docker function

def install_docker():
    # Apply all updates in the instance
    os.system("sudo yum update -y")

    # Install the most recent Docker Community Edition package.
    os.system("sudo amazon-linux-extras install docker")

    # Start the Docker service.
    os.system("sudo service docker start")

    # Add the ec2-user to the docker group so, you can execute Docker commands without using sudo.
    os.system("sudo usermod -a -G docker ec2-user")

    # Verify that the ec2-user can run Docker commands without sudo.
    os.system("sudo docker info")


# Install the prerequisites in the new environment

def prerequisites():
    # Install boto3
    os.system("pip3 install boto3")

    # Install AWS CLI
    os.system("pip3 install awscli")

    # Les the environment images
    os.system("sudo docker image ls")


###############################################################################################
#                                script execution                                             #
###############################################################################################


if __name__ == "__main__":
    install_docker()
    prerequisites()

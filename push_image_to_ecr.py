###############################################################################################
#                                import of script libraries                                   #
###############################################################################################

import os


###############################################################################################
#                                definition of script functions                               #
###############################################################################################

# Build frontend image function

def tag_images():
    # Tag frontend image for ecr repository
    os.system("sudo docker tag vof:latest 403344839207.dkr.ecr.us-east-1.amazonaws.com/production_repository:vof-v1")

    # Tag backend image for ecr repository
    os.system("sudo docker tag vob:latest 403344839207.dkr.ecr.us-east-1.amazonaws.com/production_repository:vob-v1")


# Push images function

def push_images():
    # Configure credentials
    os.system("aws configure")

    # Get the encrypted password
    os.system("aws ecr get-login --region us-east-1")

    # Connect to the ecr repository
    os.system(
        "aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 403344839207.dkr.ecr.us-east-1.amazonaws.com")

    # Push frontend image to herman_apps_repo
    os.system("docker push 403344839207.dkr.ecr.us-east-1.amazonaws.com/production_repository:vof-v1")

    # Push backend image to herman_apps_repo
    os.system("docker push 403344839207.dkr.ecr.us-east-1.amazonaws.com/production_repository:vob-v1")


###############################################################################################
#                                script execution                                             #
###############################################################################################


if __name__ == "__main__":
    tag_images()
    push_images()

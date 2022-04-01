###############################################################################################
#                                import of script libraries                                   #
###############################################################################################
import os

import boto3


###############################################################################################
#                                definition of script functions                               #
###############################################################################################

# Connect to an iam user account:
def connect_an_iam_user():
    os.system("pip3 install boto3")  # installing boto3 last version
    os.system("pip3 install awscli")  # installing awscli last version
    os.system("aws configure")  # connecting IAM user


# Create an ECR repository:
def create_ecr_repository():
    # Creating a client instance
    client = boto3.client('ecr')

    # Creating ECR repository
    response = client.create_repository(
        repositoryName='mlapp_repo'
    )
    print(response)


# Create a vpc:
def create_vpc():
    # Initiate ec2 instance for the vpc
    ec2 = boto3.resource('ec2')

    # create VPC
    vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')

    # assign a name to our VPC
    vpc.create_tags(Tags=[{"Key": "Name", "Value": "mlapp_vpc"}])

    vpc.wait_until_available()

    # enable public dns hostname so that we can SSH into it later
    ec2Client = boto3.client('ec2')
    ec2Client.modify_vpc_attribute(VpcId=vpc.id, EnableDnsSupport={'Value': True})
    ec2Client.modify_vpc_attribute(VpcId=vpc.id, EnableDnsHostnames={'Value': True})

    # create an internet gateway and attach it to VPC
    internetgateway = ec2.create_internet_gateway()
    vpc.attach_internet_gateway(InternetGatewayId=internetgateway.id)

    # create a route table and a public route
    routetable = vpc.create_route_table()
    route = routetable.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=internetgateway.id)
    print(route)

    # Security group to allow SSH connection
    securitygroup1 = ec2.create_security_group(GroupName='ONLY SSH', Description='only allow SSH traffic',
                                               VpcId=vpc.id,
                                               TagSpecifications=[{'ResourceType': 'security-group',
                                                                   'Tags': [
                                                                       {
                                                                           'Key': 'Name',
                                                                           'Value': 'sshSG'
                                                                       }, ]
                                                                   }]
                                               )
    securitygroup1.authorize_ingress(CidrIp='0.0.0.0/0',
                                     IpProtocol='tcp',
                                     FromPort=22,
                                     ToPort=8501,
                                     )

    # create subnet1 and associate it with route table
    subnet1 = ec2.create_subnet(CidrBlock='10.0.0.0/24', VpcId=vpc.id,
                                TagSpecifications=[{'ResourceType': 'subnet',
                                                    'Tags': [{"Key": "Name",
                                                              "Value": "mlapp_subnet1"
                                                              }]
                                                    }]
                                )
    routetable.associate_with_subnet(SubnetId=subnet1.id)

    # create a file to store the key locally
    outfile = open('ec2keypair.pem', 'w')

    # call the boto ec2 function to create a key pair
    key_pair = ec2.create_key_pair(KeyName='keypair000')

    # capture the key and store it in a file
    KeyPairOut = str(key_pair.key_material)
    outfile.write(KeyPairOut)

    # Create an EC2 instance and launch AWS Linux 2:
    instances = ec2.create_instances(
        ImageId='ami-0c02fb55956c7d316',
        InstanceType='t2.micro',
        MinCount=1,
        MaxCount=1,
        NetworkInterfaces=[{
            'SubnetId': subnet1.id,
            'DeviceIndex': 0,
            'AssociatePublicIpAddress': True,
            'Groups': [securitygroup1.group_id]
        }],
        KeyName='keypair000',
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'mlapp_instance'
                    },
                ]
            },
        ]
    )

    # waiting for instance
    instances[0].wait_until_running()

    # reload the instance object
    instances[0].reload()

    # getting the instance public address
    public_ip = instances[0].public_ip_address

    # returning the instance public address
    return public_ip


# transfer script files and docker images inside ec2 instance
def transfer_files(public_ip):
    KeyPairPath = "C:/Users/soule/OneDrive/Bureau/Thesis_files/Dev_And_ML/stack-overflow-developer-survey-2021/ec2keypair.pem"

    # change directory to C:/Users/soule/OneDrive/Bureau/Script/
    # os.system("cd " + KeyPairPath)

    # Copy the new directory content to the AWS EC2 instance
    os.system(
        "scp -i " + KeyPairPath + " C:/Users/soule/OneDrive/Bureau/Thesis_files/Dev_And_ML/stack-overflow-developer-survey-2021/setup_ec2_env.py ec2-user@" + public_ip + ":/home/ec2-user/")

    os.system(
        "scp -i " + KeyPairPath + " C:/Users/soule/OneDrive/Bureau/Thesis_files/Dev_And_ML/stack-overflow-developer-survey-2021/push_image_to_ecr.py ec2-user@" + public_ip + ":/home/ec2-user/")

    os.system(
        "scp -i " + KeyPairPath + " C:/Users/soule/OneDrive/Bureau/Thesis_files/Dev_And_ML/stack-overflow-developer-survey-2021/build_docker_image.py ec2-user@" + public_ip + ":/home/ec2-user/")

    os.system(
        "scp -i " + KeyPairPath + " C:/Users/soule/OneDrive/Bureau/Thesis_files/Dev_And_ML/stack-overflow-developer-survey-2021/main.py ec2-user@" + public_ip + ":/home/ec2-user/")


# connect to the created ec2 instance
def connect_to_ec2_instance(public_ip):
    # Ask for the KeyPair Path in the local machine (example: C:\Users\soule\OneDrive\Bureau\Script\ec2keypair.pem)
    KeyPairPath = "C:/Users/soule/OneDrive/Bureau/Thesis_files/Dev_And_ML/stack-overflow-developer-survey-2021/ec2keypair.pem"

    # Connect to ec2 using ssh
    os.system("ssh -i " + KeyPairPath + " ec2-user@" + public_ip)


###############################################################################################
#                                script execution                                             #
###############################################################################################

if __name__ == "__main__":
    # connect_an_iam_user()

    # create_ecr_repository()

    # public_address = create_vpc()

    # Print the IP Address in terminal
    # print("\n\n The instance public address is :", public_address)

    # Connecting to AWS EC2 instance
    public_address = '34.229.12.170'

    # Print files transfer message
    transfer_files(public_address)
    print("\n\n Files transfer done!")

    # print("\n\n Connecting to AWS EC2 instance ...")
    # connect_to_ec2_instance(public_address)

###############################################################################################
#                                import of script libraries                                   #
###############################################################################################

import boto3

import json


###############################################################################################
#                                definition of script functions                               #
###############################################################################################
#   Create an AWS ECS Fargate Cluster

def create_fargate_cluster():
    client = boto3.client("ecs", region_name="us-east-1")

    response = client.create_cluster(clusterName="production_cluster")

    print(json.dumps(response, indent=4))

    return client


# List all cluster that are created

def list_all_cluster():
    client = boto3.client("ecs", region_name="us-east-1")

    paginator = client.get_paginator('list_clusters')

    response_iterator = paginator.paginate(
        PaginationConfig={
            'PageSize': 100
        })

    for each_page in response_iterator:
        for each_arn in each_page['clusterArns']:
            print(each_arn)


# Describe all cluster

def describe_all_cluster():
    client = boto3.client("ecs", region_name="us-east-1")

    paginator = client.get_paginator('list_clusters')

    response_iterator = paginator.paginate(
        PaginationConfig={
            'PageSize': 100
        })

    for each_page in response_iterator:
        for each_arn in each_page['clusterArns']:
            response = client.describe_clusters(clusters=[each_arn])
            print(json.dumps(response, indent=4))


# Delete cluster
def delete_cluster():
    client = boto3.client("ecs", region_name="us-east-1")

    response = client.delete_cluster(cluster="production_cluster")

    print(json.dumps(response, indent=4))


# Register task definitions :

def task_definition():
    client = boto3.client("ecs", region_name="us-east-1")

    response = client.register_task_definition(
        family='backend_task',
        taskRoleArn='arn:aws:iam::403344839207:role/ecsTaskExecutionRole',
        # create an executionRoleArn by using AWS Management Console
        executionRoleArn='arn:aws:iam::403344839207:role/ecsTaskExecutionRole',
        containerDefinitions=[
            {
                "name": "backend_container",
                "image": "403344839207.dkr.ecr.us-east-1.amazonaws.com/production_repository:vob-v1",
                "cpu": 123,
                "portMappings": [{
                    'containerPort': 80,
                    'hostPort': 80,
                    'protocol': 'tcp'
                }],
                "essential": True,
                "environment": [],
                "mountPoints": [],
                "volumesFrom": [],
                "logConfiguration": {
                    "logDriver": "awslogs",
                    "options": {
                        "awslogs-group": "/ecs/AWSSampleApp",
                        "awslogs-region": "us-east-1",
                        "awslogs-stream-prefix": "ecs"
                    }
                }
            }
        ],
        networkMode="awsvpc",
        requiresCompatibilities=[
            "FARGATE"
        ],
        cpu="256",
        memory="512")

    print(json.dumps(response, indent=4, default=str))


# List all task definition family

def list_all_task_definition_family():
    client = boto3.client("ecs", region_name="us-east-1")

    paginator = client.get_paginator('list_task_definition_families')

    response_iterator = paginator.paginate(
        PaginationConfig={
            'PageSize': 100
        }
    )

    for each_page in response_iterator:
        print(each_page['families'])


# List all task definition

def list_all_task_definition():
    client = boto3.client("ecs", region_name="us-east-1")

    paginator = client.get_paginator('list_task_definitions')

    response_iterator = paginator.paginate(
        PaginationConfig={
            'PageSize': 100
        }
    )

    for each_page in response_iterator:
        for each_task in each_page['taskDefinitionArns']:
            print(each_task)


# Describe all task definition

def describe_all_task_definition():
    client = boto3.client("ecs", region_name="us-east-1")

    paginator = client.get_paginator('list_task_definitions')

    response_iterator = paginator.paginate(
        PaginationConfig={
            'PageSize': 100
        }
    )

    for each_page in response_iterator:
        for each_task_definition in each_page['taskDefinitionArns']:
            response = client.describe_task_definition(taskDefinition=each_task_definition)
            print(json.dumps(response, indent=4, default=str))


# Deregister all task definition
def deregister_all_task_definition():
    client = boto3.client("ecs", region_name="us-east-1")

    paginator = client.get_paginator('list_task_definitions')

    response_iterator = paginator.paginate(
        PaginationConfig={
            'PageSize': 100
        }
    )

    for each_page in response_iterator:
        for each_task_definition in each_page['taskDefinitionArns']:
            response = client.deregister_task_definition(
                taskDefinition=each_task_definition)
            print(json.dumps(response, indent=4, default=str))


# Create Service

def create_service():
    # Create a boto3 client instance
    client = boto3.client("ecs", region_name="us-east-1")

    # Service configuration
    response = client.create_service(cluster='production_cluster',
                                     serviceName='production_service',
                                     taskDefinition='production_task',
                                     desiredCount=2,
                                     networkConfiguration={
                                         'awsvpcConfiguration': {
                                             'subnets': [
                                                 'subnet-03f52c7579fc4de5f',
                                                 'subnet-025145dffcd766d84',
                                             ],
                                             'assignPublicIp': 'ENABLED',
                                             'securityGroups': ['sg-0624392149d48c52f']
                                         }
                                     },

                                     )
    # Print the created service
    print(json.dumps(response, indent=4, default=str))


# List all service

def list_all_service():
    client = boto3.client("ecs", region_name="us-east-1")

    clusters = client.list_clusters()

    cluster_name = clusters['clusterArns'][0]

    paginator = client.get_paginator('list_services')

    response_iterator = paginator.paginate(
        cluster=cluster_name,
        PaginationConfig={
            'PageSize': 100
        }
    )

    for each_page in response_iterator:
        for each_arn in each_page['serviceArns']:
            print(each_arn)


# Describe all services

def describe_all_service():
    client = boto3.client("ecs", region_name="us-east-1")

    cluster_name = "production_cluster"

    paginator = client.get_paginator('list_services')

    response_iterator = paginator.paginate(
        cluster=cluster_name,
        PaginationConfig={
            'PageSize': 100
        }
    )

    for each_page in response_iterator:
        for each_arn in each_page['serviceArns']:
            response = client.describe_services(
                services=[
                    each_arn
                ]
            )
            print(json.dumps(response, indent=4, default=str))


# Update all service
def update_all_service():
    client = boto3.client("ecs", region_name="us-east-1")

    cluster_name = "production_cluster"

    paginator = client.get_paginator('list_services')

    response_iterator = paginator.paginate(
        cluster=cluster_name,
        PaginationConfig={
            'PageSize': 100
        }
    )

    for each_page in response_iterator:
        for each_arn in each_page['serviceArns']:
            response = client.update_service(
                service=each_arn,
                desiredCount=2
            )
            print(json.dumps(response, indent=4, default=str))


# Delete service
def delete_service():
    client = boto3.client("ecs", region_name="us-east-1")

    cluster_name = "production_cluster"

    paginator = client.get_paginator('list_services')

    response_iterator = paginator.paginate(
        cluster=cluster_name,
        PaginationConfig={
            'PageSize': 100
        }
    )

    for each_page in response_iterator:
        for each_arn in each_page['serviceArns']:
            response = client.delete_service(
                service=each_arn,
                force=True)
            print(json.dumps(response, indent=4, default=str))


# Run task
def run_task():
    client = boto3.client("ecs", region_name="us-east-1")

    ec2 = boto3.resource('ec2')

    response = client.run_task(
        taskDefinition='backend_task',
        launchType='FARGATE',
        cluster='demoCluster',
        platformVersion='LATEST',
        count=1,
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': [
                    'subnet-02d9075d1f3b844ef',
                    'subnet-01541c86b3c9a44c3',
                    'subnet-0cc4eb043d4d295d0',
                ],
                'assignPublicIp': 'ENABLED',
                'securityGroups': ["sg-00a6e058ae5f83053"]
            }
        }
    )

    print(json.dumps(response, indent=4, default=str), ec2)


# Stop task
def stop_task():
    client = boto3.client("ecs", region_name="us-east-1")

    paginator = client.get_paginator('list_tasks')

    response_iterator = paginator.paginate(
        PaginationConfig={
            'PageSize': 100
        }
    )

    for each_page in response_iterator:
        for each_task in each_page['taskArns']:
            response = client.stop_task(task=each_task)
            print(json.dumps(response, indent=4, default=str))


# Create Application Load Balancer
def create_application_load_balancer():
    client = boto3.client('elb')  # initiate the elastic load balancer creation instance

    # Creation and configuration of elastic load balancer instance
    response = client.create_load_balancer(
        LoadBalancerName='MyALB',
        Listeners=[
            {
                'Protocol': 'HTTP',
                'LoadBalancerPort': 80,
                'InstanceProtocol': 'HTTP',
                'InstancePort': 443,
            },
        ],

        Subnets=[
            'subnet-03f52c7579fc4de5f',
        ],
        SecurityGroups=[
            'sg-0624392149d48c52f',
        ]
    )

    print(response)  # Show the result.


###############################################################################################
#                                script execution                                             #
###############################################################################################

if __name__ == "__main__":
    # Fargate cluster creation, and description
    # create_fargate_cluster()
    # list_all_cluster()
    # describe_all_cluster()

    # Task definition creation, and description
    # task_definition()
    # list_all_task_definition_family()
    # list_all_task_definition_family()
    # describe_all_task_definition()

    # Service creation, and description
    # create_service()
    # list_all_service()

    # create_target_grp()
    # create_application_load_balancer()
    # create_efs()

    # Run, and describe task level
    run_task()

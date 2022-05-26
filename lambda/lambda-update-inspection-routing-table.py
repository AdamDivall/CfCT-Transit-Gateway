import boto3
import os
import cfnresponse
from botocore.exceptions import ClientError

network_fw_client=boto3.client('network-firewall')
ec2_client=boto3.client('ec2')

inspection_vpc_tgw_route_tables=os.environ['INSPECTION_VPC_TGW_RTBS']
firewall_arn=os.environ['NETWORK_FIREWALL_ARN']

def lambda_handler(event, context):
    if (event['RequestType'] == 'Create' or event['RequestType'] == 'Update'):
        try:
            route_table_list=inspection_vpc_tgw_route_tables.split(",")
            try:
                fw_endpoints=network_fw_client.describe_firewall(
                    FirewallArn=firewall_arn
                )['FirewallStatus']['SyncStates']
            except ClientError as e:
                print(f"Unable to Describe Network Firewall: {firewall_arn}. Error: {e}.")
            for table in route_table_list:
                try:
                    associated_subnet_id=ec2_client.describe_route_tables(
                        RouteTableIds=[
                            table
                        ]
                    )['RouteTables'][0]['Associations'][0]['SubnetId']
                except ClientError as e:
                    print(f"Unable to Describe Route Table: {table}. Error: {e}.")
                try:
                    subnet_az=ec2_client.describe_subnets(
                        SubnetIds=[
                            associated_subnet_id
                        ]
                    )['Subnets'][0]['AvailabilityZone']
                except ClientError as e:
                    print(f"Unable to Describe Subnet: {subnet_az}. Error: {e}.")
                if subnet_az in fw_endpoints:
                    gwlb_endpoint=fw_endpoints[subnet_az]['Attachment']['EndpointId']
                    try:
                        ec2_client.create_route(
                            DestinationCidrBlock="0.0.0.0/0",
                            VpcEndpointId=gwlb_endpoint,
                            RouteTableId=table
                        )
                        print(f"Added Route to 0.0.0.0/0 via {gwlb_endpoint} in Route Table {table}.")
                    except ClientError as e:
                        print(f"Unable to Add Route to Routing Table: {table}. Error: {e}.")
            cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
        except ClientError as e: 
            print(e.response['Error']['Message']) 
            cfnresponse.send(event, context, cfnresponse.FAILED, e.response)
    elif event['RequestType'] == 'Delete':
        try:
            route_table_list=inspection_vpc_tgw_route_tables.split(",")
            for table in route_table_list:
                try:
                    ec2_client.delete_route(
                        DestinationCidrBlock="0.0.0.0/0",
                        RouteTableId=table
                    )
                except ClientError as e:
                    print(f"Unable to Delete Route from Routing Table: {table}. Error: {e}.")
            cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
        except ClientError as e: 
            print(e.response['Error']['Message']) 
            cfnresponse.send(event, context, cfnresponse.FAILED, e.response)
import boto3
import os
import cfnresponse
from botocore.exceptions import ClientError

ec2_client=boto3.client('ec2')

tgw_id=os.environ['TGW_ID']
tgw_rtb_firewall_id=os.environ['TGW_RTB_FW_ID']
tgw_rtb_spoke_id=os.environ['TGW_RTB_SPOKE_ID']

def lambda_handler(event, context):
    if (event['RequestType'] == 'Create' or event['RequestType'] == 'Update'):
        try:
            response=ec2_client.modify_transit_gateway(
                TransitGatewayId=tgw_id,
                Options={
                    'DefaultRouteTableAssociation': 'enable',
                    'AssociationDefaultRouteTableId': tgw_rtb_spoke_id,
                    'DefaultRouteTablePropagation': 'enable',
                    'PropagationDefaultRouteTableId': tgw_rtb_firewall_id
                }
            )
            print(response)
            cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
        except ClientError as e: 
            print(f"Unable to Modify Transit Gateway: {tgw_id}. Error: {e}.") 
            cfnresponse.send(event, context, cfnresponse.FAILED, e.response)
    elif event['RequestType'] == 'Delete':
        try:
            response=ec2_client.modify_transit_gateway(
                TransitGatewayId=tgw_id,
                Options={
                    'DefaultRouteTableAssociation': 'disable',
                    'DefaultRouteTablePropagation': 'disable'
                }
            )
            print(response)
            cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
        except ClientError as e: 
            print(f"Unable to Modify Transit Gateway: {tgw_id}. Error: {e}.") 
            cfnresponse.send(event, context, cfnresponse.FAILED, e.response)

import boto3
import os
import cfnresponse
from botocore.exceptions import ClientError

ec2_client=boto3.client('ec2')
tgw_attachment_ids=os.environ['TGW_ATTACHMENT_IDS']

def lambda_handler(event, context):
    if (event['RequestType'] == 'Create' or event['RequestType'] == 'Update'):
        tgw_attachment_id_list=tgw_attachment_ids.split(",")
        for attachment_id in tgw_attachment_id_list:
            try:
                appliance_mode=ec2_client.modify_transit_gateway_vpc_attachment(
                    TransitGatewayAttachmentId=attachment_id,
                    Options={
                        'ApplianceModeSupport': 'enable'
                    }
                )['TransitGatewayVpcAttachment']['Options']['ApplianceModeSupport']
                print(f"Appliance Mode for the Inspection VPC Transit Gateway Attachment is set to {appliance_mode}.")
                cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
            except ClientError as e: 
                print(f"Unable to Modify Transit Gateway Attacment ID: {attachment_id}. Error: {e}.") 
                cfnresponse.send(event, context, cfnresponse.FAILED, e.response)
    elif event['RequestType'] == 'Delete':
        tgw_attachment_id_list=tgw_attachment_ids.split(",")
        for attachment_id in tgw_attachment_id_list:
            try:
                appliance_mode=ec2_client.modify_transit_gateway_vpc_attachment(
                    TransitGatewayAttachmentId=attachment_id,
                    Options={
                        'ApplianceModeSupport': 'disable'
                    }
                )['TransitGatewayVpcAttachment']['Options']['ApplianceModeSupport']
                print(f"Appliance Mode for the Inspection VPC Transit Gateway Attachment is set to {appliance_mode}.")
                cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
            except ClientError as e: 
                print(f"Unable to Modify Transit Gateway Attacment ID: {attachment_id}. Error: {e}.") 
                cfnresponse.send(event, context, cfnresponse.FAILED, e.response)

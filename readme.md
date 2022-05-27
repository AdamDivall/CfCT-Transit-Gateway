# Integrating Transit Gateway with Customizations for Control Tower 

The CloudFormation Template and Lambda Function(s) have been created based on the associated [blog post](https://aws.amazon.com/blogs/networking-and-content-delivery/deployment-models-for-aws-network-firewall/).

## Architecture Overview

![alt](./diagrams/TGW.png)

## Pre-Requisites and Installation

### Pre-Requisites

There is an overarching assumption that you already have [Customisation for Control Tower](https://aws.amazon.com/solutions/implementations/customizations-for-aws-control-tower/) deployed within your Control Tower Environment.

1.  Ensure that Resource Access Manager (RAM) has been enabled for Trusted Access in the Organisation since we leverage RAM to share the Transit Gateway Across the Organisation.
2.  Clone the GitHub Repo to your local device.
3.  Create an S3 Bucket where you'll then upload the `cfnresponse.zip` file to. Create a prefix within the S3 Bucket named `lambda-layers` and upload the `cfnresponse.zip` to that prefix.

### Installation

1.  Copy the CloudFormation Template `network-core.yaml` should be added to the `/templates` folder for use with Customisations for Control Tower.
2.  Copy the CloudFormation Parameters `network-core.json` should be added to `/parameters` folder for use with Customisations for Control Tower.
3.  Update the CloudFormation Parameters `network-core.json` with the required details:
    * **OrganizationId:** This is the AWS Organization ID that is used to share the Transit Gateway out to the entire AWS Organization.
    * **pManagementAccountId:** This is the AWS Account ID of the Account that has been designated as the Network Account.
    * **pInspectionVpcCidr:** This is the CIDR range that will be used for the Inspection VPC that will conduct East/West Traffic Inspection.
    * **pInspectionVpcFwSubnetACidr:**  This is the CIDR range that will be used for the Inspection VPC Firewall Subnet in Availability Zone A where AWS Network Firewall will deploy its Gateway Load Balancer Endpoint.
    * **pInspectionVpcFwSubnetBCidr:** This is the CIDR range that will be used for the Inspection VPC Firewall Subnet in Availability Zone B where AWS Network Firewall will deploy its Gateway Load Balancer Endpoint.
    * **pInspectionVpcFwSubnetCCidr:** This is the CIDR range that will be used for the Inspection VPC Firewall Subnet in Availability Zone C where AWS Network Firewall will deploy its Gateway Load Balancer Endpoint.
    * **pInspectionVpcTgwSubnetACidr:** This is the CIDR range that will be used for the Inspection VPC Transit Gateway Subnet in Availability Zone A where specific Routes will need to be added to point to the corresponding Gateway Load Balancer Endpoint for the Availability Zone.
    * **pInspectionVpcTgwSubnetBCidr:** This is the CIDR range that will be used for the Inspection VPC Transit Gateway Subnet in Availability Zone B where specific Routes will need to be added to point to the corresponding Gateway Load Balancer Endpoint for the Availability Zone.
    * **pInspectionVpcTgwSubnetCCidr:** This is the CIDR range that will be used for the Inspection VPC Transit Gateway Subnet in Availability Zone C where specific Routes will need to be added to point to the corresponding Gateway Load Balancer Endpoint for the Availability Zone.
    * **pEgressVpcCidr:** This is the CIDR range that will be used for the Egress VPC that will conduct Egress Traffic Inspection.
    * **pEgressVpcFwSubnetACidr:** This is the CIDR range that will be used for the Egress VPC Firewall Subnet in Availability Zone A where AWS Network Firewall will deploy its Gateway Load Balancer Endpoint.
    * **pEgressVpcFwSubnetBCidr:** This is the CIDR range that will be used for the Egress VPC Firewall Subnet in Availability Zone B where AWS Network Firewall will deploy its Gateway Load Balancer Endpoint.
    * **pEgressVpcFwSubnetCCidr:**  This is the CIDR range that will be used for the Egress VPC Firewall Subnet in Availability Zone C where AWS Network Firewall will deploy its Gateway Load Balancer Endpoint.
    * **pEgressVpcTgwSubnetACidr:** This is the CIDR range that will be used for the Egress VPC Transit Gateway Subnet in Availability Zone A with a specific route for the Supernet added via the corresponding Gateway Load Balancer Endpoint for the Availability Zone.
    * **pEgressVpcTgwSubnetBCidr:** This is the CIDR range that will be used for the Egress VPC Transit Gateway Subnet in Availability Zone B with a specific route for the Supernet added via the corresponding Gateway Load Balancer Endpoint for the Availability Zone.
    * **pEgressVpcTgwSubnetCCidr:** This is the CIDR range that will be used for the Egress VPC Transit Gateway Subnet in Availability Zone C with a specific route for the Supernet added via the corresponding Gateway Load Balancer Endpoint for the Availability Zone.
    * **pEgressVpcPublicSubnetACidr:** This is the CIDR range that will be used for the Egress VPC Public Subnet in Availability Zone A where a NAT Gateway will be deployed.
    * **pEgressVpcPublicSubnetBCidr:** This is the CIDR range that will be used for the Egress VPC Public Subnet in Availability Zone B where a NAT Gateway will be deployed.
    * **pEgressVpcPublicSubnetCCidr:** This is the CIDR range that will be used for the Egress VPC Public Subnet in Availability Zone C where a NAT Gateway will be deployed.
    * **pCloudWatchLogsRetentionPeriodLambda:** This is the retention period in days that is associated with all CloudWatch Log Groups for Lambda Functions.
    * **pCloudWatchLogsRetentionPeriodNetworkFw:** This is the retention period in days that is associated with all CloudWatch Log Groups for Network Firewalls.
    * **pS3SourceBucketLambdaLayer:** This is the name of the Amazon S3 bucket where the Lambda Layer has been uploaded to.
    * **pEnvironmentName:** 

    The above values should be configured within the `network-core.json`:

    ```json
    [
        {
            "ParameterKey": "OrganizationId",
            "ParameterValue": ""
        },
        {
            "ParameterKey": "pManagementAccountId",
            "ParameterValue": ""
        },
        {
            "ParameterKey": "pInspectionVpcCidr",
            "ParameterValue": "100.64.0.0/16"
        },  
        {
            "ParameterKey": "pInspectionVpcFwSubnetACidr",
            "ParameterValue": "100.64.0.0/28"
        },
        {
            "ParameterKey": "pInspectionVpcFwSubnetBCidr",
            "ParameterValue": "100.64.0.16/28"
        },
        {
            "ParameterKey": "pInspectionVpcFwSubnetCCidr",
            "ParameterValue": "100.64.0.32/28"
        },
        {
            "ParameterKey": "pInspectionVpcTgwSubnetACidr",
            "ParameterValue": "100.64.0.48/28"
        },  
        {
            "ParameterKey": "pInspectionVpcTgwSubnetBCidr",
            "ParameterValue": "100.64.0.64/28"
        },
        {
            "ParameterKey": "pInspectionVpcTgwSubnetCCidr",
            "ParameterValue": "100.64.0.80/28"
        },
        {
            "ParameterKey": "pEgressVpcCidr",
            "ParameterValue": "10.10.0.0/16"
        },
        {
            "ParameterKey": "pEgressVpcFwSubnetACidr",
            "ParameterValue": "10.10.0.0/28"
        },
        {
            "ParameterKey": "pEgressVpcFwSubnetBCidr",
            "ParameterValue": "10.10.0.16/28"
        },  
        {
            "ParameterKey": "pEgressVpcFwSubnetCCidr",
            "ParameterValue": "10.10.0.32/28"
        },
        {
            "ParameterKey": "pEgressVpcTgwSubnetACidr",
            "ParameterValue": "10.10.0.48/28"
        },
        {
            "ParameterKey": "pEgressVpcTgwSubnetBCidr",
            "ParameterValue": "10.10.0.64/28"
        },
        {
            "ParameterKey": "pEgressVpcTgwSubnetCCidr",
            "ParameterValue": "10.10.0.80/28"
        },  
        {
            "ParameterKey": "pEgressVpcPublicSubnetACidr",
            "ParameterValue": "10.10.1.0/24"
        },
        {
            "ParameterKey": "pEgressVpcPublicSubnetBCidr",
            "ParameterValue": "10.10.2.0/24"
        },
        {
            "ParameterKey": "pEgressVpcPublicSubnetCCidr",
            "ParameterValue": "10.10.3.0/24"
        },
        {
            "ParameterKey": "pTgwAwsVpcNetworkSupernet",
            "ParameterValue": "10.0.0.0/8"
        },  
        {
            "ParameterKey": "pCloudWatchLogsRetentionPeriodLambda",
            "ParameterValue": "7"
        },
        {
            "ParameterKey": "pCloudWatchLogsRetentionPeriodNetworkFw",
            "ParameterValue": "3"
        },  
        {
            "ParameterKey": "pS3SourceBucketLambdaLayer",
            "ParameterValue": ""
        },
        {
            "ParameterKey": "pEnvironmentName",
            "ParameterValue": "Production"
        }
    ]
    ```

4.  Update the `manifest.yaml` and configure the `deployment_targets` and `regions` accordingly based on your needs. The deployment target should be the Network Account.

    ```yaml 
    - name: Core-Network
      description: "CloudFormation Template to Setup Transit Gateway and Configure Network Firewall for East/West Inspection and Egress Inspection"
      resource_file: templates/network-core.yaml
      parameter_file: parameters/network-core.json
      deploy_method: stack_set
      deployment_targets:
        accounts:
          - # Either the 12-digit Account ID or the Logical Name for the Network Account
      regions:
        - # AWS Region where the Transit Gateway should be deployed in.
    ```
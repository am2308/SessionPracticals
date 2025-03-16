import json
import boto3
import logging

# Initialize AWS clients
securityhub = boto3.client('securityhub')
s3 = boto3.client('s3')
ec2 = boto3.client('ec2')
secretsmanager = boto3.client('secretsmanager')

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Get the finding ID from the event payload
    finding_id = event.get("finding_id")
    
    if not finding_id:
        logger.error("No finding_id provided in event payload.")
        return {"status": "Error", "message": "No finding_id provided."}
    
    # Get finding details from Security Hub
    try:
        response = securityhub.get_findings(
            Filters={'Id': [{'Value': finding_id, 'Comparison': 'EQUALS'}]}
        )
        findings = response['Findings']
        if not findings:
            logger.error("No findings found for the provided finding_id.")
            return {"status": "Error", "message": "No findings found."}
        
        finding = findings[0]
        finding_type = finding['Types'][0]
        resource_id = finding['Resources'][0]['Id']
        
        # Determine remediation based on finding type
        if "S3BucketPublic" in finding_type:
            return remediate_public_s3_bucket(resource_id)
        elif "SecurityGroupOpen" in finding_type:
            return remediate_security_group(resource_id)
        elif "SecretsManagerRotationDisabled" in finding_type:
            return remediate_secret_rotation(resource_id)
        else:
            logger.warning(f"Remediation not defined for finding type: {finding_type}")
            return {"status": "NoAction", "message": f"Unknown finding type: {finding_type}"}
    except Exception as e:
        logger.error(f"Error retrieving finding details: {str(e)}")
        return {"status": "Error", "message": str(e)}

def remediate_public_s3_bucket(bucket_name):
    """Remediate S3 bucket by setting it to private."""
    try:
        # Set bucket ACL to private
        s3.put_bucket_acl(Bucket=bucket_name, ACL='private')
        
        # Remove any public bucket policy if exists
        s3.delete_bucket_policy(Bucket=bucket_name)
        
        logger.info(f"Bucket {bucket_name} remediated to be private.")
        return {"status": "Success", "message": f"Bucket {bucket_name} set to private."}
    except Exception as e:
        logger.error(f"Failed to remediate S3 bucket: {str(e)}")
        return {"status": "Error", "message": str(e)}

def remediate_security_group(security_group_id):
    """Remove public ingress rules from a security group."""
    try:
        # Describe security group rules
        sg_rules = ec2.describe_security_groups(GroupIds=[security_group_id])
        ip_permissions = sg_rules['SecurityGroups'][0]['IpPermissions']
        
        # Filter for public access (0.0.0.0/0) and revoke those permissions
        public_permissions = [perm for perm in ip_permissions if any(
            ip_range['CidrIp'] == '0.0.0.0/0' for ip_range in perm.get('IpRanges', [])
        )]
        
        if public_permissions:
            ec2.revoke_security_group_ingress(
                GroupId=security_group_id,
                IpPermissions=public_permissions
            )
            logger.info(f"Public rules removed from Security Group {security_group_id}.")
            return {"status": "Success", "message": f"Public rules removed from {security_group_id}."}
        else:
            logger.info(f"No public rules found in Security Group {security_group_id}.")
            return {"status": "NoAction", "message": "No public rules to remediate."}
    except Exception as e:
        logger.error(f"Failed to remediate security group: {str(e)}")
        return {"status": "Error", "message": str(e)}

def remediate_secret_rotation(secret_arn):
    """Enable or reset secret rotation in AWS Secrets Manager."""
    try:
        # Check if rotation is already enabled
        secret = secretsmanager.describe_secret(SecretId=secret_arn)
        rotation_enabled = secret.get('RotationEnabled', False)
        
        if rotation_enabled:
            # Trigger immediate rotation
            secretsmanager.rotate_secret(SecretId=secret_arn)
            logger.info(f"Triggered immediate rotation for secret {secret_arn}.")
            return {"status": "Success", "message": f"Triggered immediate rotation for {secret_arn}."}
        else:
            # Enable rotation with a 30-day rotation interval by default
            secretsmanager.enable_secret_rotation(SecretId=secret_arn, RotationRules={"AutomaticallyAfterDays": 30})
            logger.info(f"Enabled rotation for secret {secret_arn} with a 30-day interval.")
            return {"status": "Success", "message": f"Enabled rotation for {secret_arn}."}
    except Exception as e:
        logger.error(f"Failed to remediate Secrets Manager rotation: {str(e)}")
        return {"status": "Error", "message": str(e)}

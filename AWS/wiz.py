import json
import boto3
import logging
import os

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS Clients
s3 = boto3.client('s3')
securityhub = boto3.client('securityhub')

def remediate_s3_public_access(bucket_name):
    """ Removes public access from the S3 bucket """
    try:
        # Block public access
        s3.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }
        )
        logger.info(f"Public access blocked for bucket: {bucket_name}")
        return True
    except Exception as e:
        logger.error(f"Failed to block public access for {bucket_name}: {e}")
        return False

def enforce_s3_encryption(bucket_name):
    """ Enforce default encryption on the S3 bucket """
    try:
        s3.put_bucket_encryption(
            Bucket=bucket_name,
            ServerSideEncryptionConfiguration={
                'Rules': [{
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'AES256'
                    }
                }]
            }
        )
        logger.info(f"Encryption enforced on bucket: {bucket_name}")
        return True
    except Exception as e:
        logger.error(f"Failed to enforce encryption on {bucket_name}: {e}")
        return False

def update_security_hub_finding(finding_id):
    """ Mark the Security Hub finding as 'RESOLVED' """
    try:
        securityhub.batch_update_findings(
            FindingIdentifiers=[{"Id": finding_id, "ProductArn": "arn:aws:securityhub:::product/aws/securityhub"}],
            Note={"Text": "Remediation applied successfully", "UpdatedBy": "S3SecurityLambda"},
            Workflow={"Status": "RESOLVED"}
        )
        logger.info(f"Marked finding {finding_id} as RESOLVED in Security Hub")
    except Exception as e:
        logger.error(f"Failed to update Security Hub finding {finding_id}: {e}")

def lambda_handler(event, context):
    """ Lambda function entry point """
    try:
        logger.info("Lambda triggered for S3 Security remediation")

        # Get Security Hub findings
        response = securityhub.get_findings(
            Filters={"ResourceType": [{"Value": "AwsS3Bucket", "Comparison": "EQUALS"}]},
            MaxResults=10
        )
        
        findings = response.get("Findings", [])
        if not findings:
            logger.info("No S3 security vulnerabilities found.")
            return {"message": "No vulnerabilities detected"}

        for finding in findings:
            bucket_name = finding["Resources"][0]["Id"].split(":")[-1]
            finding_id = finding["Id"]
            logger.info(f"Found security issue in bucket: {bucket_name}")

            # Remediation Steps
            remediation_applied = False

            if "s3-bucket-public-read-prohibited" in finding["ProductFields"].get("ControlId", ""):
                remediation_applied = remediate_s3_public_access(bucket_name)

            if "s3-bucket-server-side-encryption-enabled" in finding["ProductFields"].get("ControlId", ""):
                remediation_applied = enforce_s3_encryption(bucket_name)

            if remediation_applied:
                update_security_hub_finding(finding_id)

        return {"message": "S3 security remediation completed"}

    except Exception as e:
        logger.error(f"Lambda execution failed: {e}")
        return {"error": str(e)}

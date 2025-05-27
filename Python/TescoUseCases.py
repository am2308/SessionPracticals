### Log Parsing
#!/usr/bin/env python3
"""
Log analyzer script - procedural approach with functional elements
"""

import re
import argparse
import logging
from collections import defaultdict
import gzip
import json
from datetime import datetime
import os
import boto3

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('log_analyzer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

def parse_log_file(file_path, pattern):
    """Parse log file and return error counts"""
    error_counts = defaultdict(int)
    open_func = gzip.open if file_path.endswith('.gz') else open
    
    try:
        with open_func(file_path, 'rt', encoding='utf-8') as f:
        
            for line in f:
                try:
                    if match := re.search(pattern, line):
                        error_counts[match.group()] += 1
                except UnicodeDecodeError:
                    logger.warning(f"Encoding issue in line: {line[:100]}...")
                    continue
                    
        logger.info(f"Found {sum(error_counts.values())} errors in {file_path}")
        return dict(error_counts)
        
    except Exception as e:
        logger.error(f"Failed to process {file_path}: {str(e)}")
        raise

def upload_to_s3(file_path, bucket_name):
    """Upload file to S3"""
    try:
        s3 = boto3.client('s3')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        s3_key = f"logs/{timestamp}/{os.path.basename(file_path)}"
        s3.upload_file(file_path, bucket_name, s3_key)
        logger.info(f"Uploaded to s3://{bucket_name}/{s3_key}")
    except Exception as e:
        logger.error(f"S3 upload failed: {str(e)}")
        raise

def main():
    parser = argparse.ArgumentParser(description='Log analyzer')
    parser.add_argument('file_path', help='Log file path')
    parser.add_argument('--pattern', default=r'ERROR|WARN', help='Regex pattern')
    parser.add_argument('--upload', action='store_true', help='Upload to S3')
    parser.add_argument('--bucket', help='S3 bucket name')
    args = parser.parse_args()

    try:
        counts = parse_log_file(args.file_path, args.pattern)
        print(f"Error counts: {counts}")
        print(json.dumps(counts, indent=2))
        
        if args.upload and args.bucket:
            upload_to_s3(args.file_path, args.bucket)
            
    except Exception as e:
        logger.critical(f"Script failed: {str(e)}")
        exit(1)

if __name__ == '__main__':
    main()

### AWS Provisioning
'''
#!/usr/bin/env python3
"""
AWS infrastructure provisioning - functional approach
"""

import boto3
import argparse
import logging
import json
import sys
from botocore.exceptions import ClientError

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger()

def create_ec2_instance(region, ami_id, instance_type, key_name):
    """Launch EC2 instance"""
    try:
        ec2 = boto3.client('ec2', region_name=region)
        response = ec2.run_instances(
            ImageId=ami_id,
            InstanceType=instance_type,
            KeyName=key_name,
            MinCount=1,
            MaxCount=1
        )
        instance_id = response['Instances'][0]['InstanceId']
        logger.info(f"Launched instance {instance_id}")
        return instance_id
    except ClientError as e:
        logger.error(f"AWS error: {e.response['Error']['Message']}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise

def create_s3_bucket(bucket_name, region):
    """Create S3 bucket"""
    try:
        s3 = boto3.client('s3', region_name=region)
        location = {'LocationConstraint': region}
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration=location
        )
        logger.info(f"Created bucket {bucket_name} in {region}")
    except ClientError as e:
        logger.error(f"AWS error: {e.response['Error']['Message']}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise

def main():
    parser = argparse.ArgumentParser(description='AWS provisioning')
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # EC2 commands
    ec2_parser = subparsers.add_parser('ec2')
    ec2_parser.add_argument('--region', required=True)
    ec2_parser.add_argument('--ami', required=True)
    ec2_parser.add_argument('--type', default='t3.micro')
    ec2_parser.add_argument('--key', required=True)
    
    # S3 commands
    s3_parser = subparsers.add_parser('s3')
    s3_parser.add_argument('--region', required=True)
    s3_parser.add_argument('--name', required=True)
    
    args = parser.parse_args()

    try:
        if args.command == 'ec2':
            instance_id = create_ec2_instance(
                args.region, args.ami, args.type, args.key
            )
            print(f"Instance ID: {instance_id}")
            
        elif args.command == 's3':
            create_s3_bucket(args.name, args.region)
            
    except Exception as e:
        logger.critical(f"Provisioning failed: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
'''

### API Health Check
'''
#!/usr/bin/env python3
"""
API health check with alerting - procedural approach
"""

import requests
import logging
import time
import smtplib
from email.message import EmailMessage
import os
import argparse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger()

def check_api_endpoint(url):
    """Check API endpoint health"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return True, response.elapsed.total_seconds()
    except requests.exceptions.RequestException as e:
        logger.warning(f"API check failed: {str(e)}")
        return False, 0

def send_alert(subject, message):
    """Send email alert"""
    try:
        msg = EmailMessage()
        msg.set_content(message)
        msg['Subject'] = subject
        msg['From'] = os.getenv('ALERT_EMAIL_FROM')
        msg['To'] = os.getenv('ALERT_EMAIL_TO')
        
        with smtplib.SMTP(os.getenv('SMTP_SERVER'), 587) as smtp:
            smtp.starttls()
            smtp.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASS'))
            smtp.send_message(msg)
        logger.info("Alert email sent")
    except Exception as e:
        logger.error(f"Failed to send alert: {str(e)}")

def monitor_api(url, interval, threshold):
    """Monitor API endpoint"""
    failures = 0
    
    while True:
        is_healthy, latency = check_api_endpoint(url)
        
        if not is_healthy:
            failures += 1
            if failures >= threshold:
                send_alert(
                    f"API CRITICAL: {url}",
                    f"API failed {failures} consecutive times"
                )
                failures = 0  # Reset after alert
        else:
            failures = 0
            logger.info(f"API healthy. Latency: {latency:.2f}s")
            
        time.sleep(interval)

def main():
    parser = argparse.ArgumentParser(description='API Monitor')
    parser.add_argument('url', help='API endpoint URL')
    parser.add_argument('--interval', type=int, default=60, help='Check interval (seconds)')
    parser.add_argument('--threshold', type=int, default=3, help='Failure threshold')
    args = parser.parse_args()

    try:
        logger.info(f"Starting API monitor for {args.url}")
        monitor_api(args.url, args.interval, args.threshold)
    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user")
    except Exception as e:
        logger.critical(f"Monitor failed: {str(e)}")
        exit(1)

if __name__ == '__main__':
    main()
'''

### System Metrics Collector
#!/usr/bin/env python3
"""
System metrics collector and CloudWatch uploader
"""

import psutil
import boto3
import time
from datetime import datetime
import logging
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

def collect_metrics():
    """Collect system performance metrics"""
    metrics = {}
    
    # CPU metrics
    metrics['cpu_percent'] = psutil.cpu_percent(interval=1)
    metrics['cpu_count'] = psutil.cpu_count()
    
    # Memory metrics
    mem = psutil.virtual_memory()
    metrics['mem_total'] = mem.total / (1024**3)  # GB
    metrics['mem_used'] = mem.used / (1024**3)
    metrics['mem_percent'] = mem.percent
    
    # Disk metrics
    disk = psutil.disk_usage('/')
    metrics['disk_total'] = disk.total / (1024**3)
    metrics['disk_used'] = disk.used / (1024**3)
    metrics['disk_percent'] = disk.percent
    
    # Network metrics
    net = psutil.net_io_counters()
    metrics['bytes_sent'] = net.bytes_sent
    metrics['bytes_recv'] = net.bytes_recv
    
    return metrics

def send_to_cloudwatch(metrics, namespace, dimensions):
    """Send metrics to AWS CloudWatch"""
    cloudwatch = boto3.client('cloudwatch')
    
    metric_data = []
    timestamp = datetime.utcnow()
    
    for name, value in metrics.items():
        metric_data.append({
            'MetricName': name,
            'Dimensions': dimensions,
            'Timestamp': timestamp,
            'Value': value,
            'Unit': 'Percent' if '%' in name else 'Count'
        })
    
    try:
        cloudwatch.put_metric_data(
            Namespace=namespace,
            MetricData=metric_data
        )
        logger.info(f"Sent {len(metric_data)} metrics to CloudWatch")
    except Exception as e:
        logger.error(f"CloudWatch upload failed: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='System metrics collector')
    parser.add_argument('--interval', type=int, default=60, 
                       help='Collection interval in seconds')
    parser.add_argument('--namespace', default='SystemMetrics',
                       help='CloudWatch namespace')
    args = parser.parse_args()

    dimensions = [{'Name': 'Host', 'Value': 'ProductionServer'}]
    
    try:
        while True:
            metrics = collect_metrics()
            print(metrics)  # Print metrics to console
            #send_to_cloudwatch(metrics, args.namespace, dimensions)
            
            if args.interval <= 0:  # Run once if interval is 0 or negative
                break
                
            time.sleep(args.interval)
    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user")

if __name__ == '__main__':
    main()
### Excel to MySQL Data Pipeline
'''
#!/usr/bin/env python3
"""
Excel to MySQL data pipeline with pandas
"""

import pandas as pd
import mysql.connector
from mysql.connector import Error
import argparse
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

def read_excel(file_path, sheet_name=None):
    """Read Excel file into pandas DataFrame"""
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        logger.info(f"Read {len(df)} rows from Excel file")
        return df
    except Exception as e:
        logger.error(f"Excel read failed: {str(e)}")
        raise

def clean_data(df):
    """Clean and prepare data for database"""
    # Convert date columns
    print(df.columns)
    for col in df.select_dtypes(include=['object']):
        try:
            df[col] = pd.to_datetime(df[col])
        except (ValueError, TypeError):
            pass
    
    # Fill missing values
    df = df.fillna('NULL')
    
    return df

def load_to_mysql(df, table_name):
    """Load DataFrame to MySQL database"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        
        cursor = connection.cursor()
        
        # Create table if not exists
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {', '.join(f'`{col}` TEXT' for col in df.columns)}
        )
        """
        cursor.execute(create_table_sql)
        
        # Insert data
        for _, row in df.iterrows():
            placeholders = ', '.join(['%s'] * len(row))
            columns = ', '.join(f'`{col}`' for col in df.columns)
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, tuple(row))
        
        connection.commit()
        logger.info(f"Loaded {len(df)} rows to MySQL table {table_name}")
        
    except Error as e:
        logger.error(f"MySQL error: {str(e)}")
        raise
    finally:
        if connection.is_connected():
            connection.close()

def main():
    parser = argparse.ArgumentParser(description='Excel to MySQL loader')
    parser.add_argument('file_path', help='Excel file path')
    parser.add_argument('--sheet', help='Sheet name (if multiple sheets)')
    parser.add_argument('--table', required=True, help='MySQL table name')
    args = parser.parse_args()

    try:
        # Extract
        df = read_excel(args.file_path, args.sheet)
        
        # Transform
        df = clean_data(df)
        print(df.columns)
        
        # Load
        #load_to_mysql(df, args.table)
        
        logger.info("Data pipeline completed successfully")
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")

if __name__ == '__main__':
    main()
'''
### HTTP Error Code Analyzer
#!/usr/bin/env python3
"""
HTTP error code analyzer from log files
"""

import re
import argparse
import logging
from collections import Counter
import gzip

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

def parse_log_file(file_path):
    """Parse log file and count HTTP status codes"""
    http_error_pattern = r'\s(\d{3})\s'
    counter = Counter()
    open_func = gzip.open if file_path.endswith('.gz') else open
    
    try:
        with open_func(file_path, 'rt', encoding='utf-8') as f:
            for line in f:
                match = re.search(http_error_pattern, line)
                if match:
                    status_code = match.group(1)
                    print(status_code)
                    if status_code.startswith(('4', '5')):  # Only error codes
                        counter[status_code] += 1
                        
        return counter
    except Exception as e:
        logger.error(f"Failed to process {file_path}: {str(e)}")
        raise

def main():
    parser = argparse.ArgumentParser(description='HTTP error analyzer')
    parser.add_argument('file_path', help='Log file path')
    parser.add_argument('--top', type=int, default=3,
                       help='Number of top errors to show')
    args = parser.parse_args()

    try:
        counter = parse_log_file(args.file_path)
        top_errors = counter.most_common(args.top)
        
        print(f"\nTop {args.top} HTTP error codes:")
        for code, count in top_errors:
            print(f"{code}: {count} occurrences")
            
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")

if __name__ == '__main__':
    main()

### Data Analysis with Pandas and Numpy
'''
#!/usr/bin/env python3
"""
Data analysis with pandas and numpy
"""

import pandas as pd
import numpy as np
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

def analyze_data(file_path):
    """Perform data analysis on CSV file"""
    try:
        # Read data
        df = pd.read_csv(file_path)
        logger.info(f"Loaded data: {df.shape[0]} rows, {df.shape[1]} columns")
        
        results = {}
        
        # Basic stats
        results['summary'] = df.describe().to_dict()
        
        # Correlation analysis
        numeric_df = df.select_dtypes(include=[np.number])
        if not numeric_df.empty:
            results['correlation'] = numeric_df.corr().to_dict()
        
        # Top categories
        for col in df.select_dtypes(include=['object']):
            results[f'top_{col}'] = df[col].value_counts().head(5).to_dict()
        
        return results
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise

def main():
    parser = argparse.ArgumentParser(description='Data analyzer')
    parser.add_argument('file_path', help='CSV file path')
    parser.add_argument('--output', help='Output JSON file')
    args = parser.parse_args()

    try:
        results = analyze_data(args.file_path)
        
        # Print results
        print("\nAnalysis Results:")
        for key, value in results.items():
            print(f"\n{key.upper()}:")
            print(value)
            
        # Save to file if requested
        if args.output:
            import json
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            logger.info(f"Saved results to {args.output}")
            
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")

if __name__ == '__main__':
    main()
'''

### Log Cleanup Utility
'''
#!/usr/bin/env python3
"""
Automated log cleanup utility
"""

import os
import glob
import argparse
import logging
import gzip
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

def compress_old_logs(log_dir, days_old):
    """Compress logs older than specified days"""
    cutoff = time.time() - (days_old * 86400)
    processed = 0
    
    for log_file in glob.glob(os.path.join(log_dir, '*.log')):
        if os.stat(log_file).st_mtime < cutoff:
            try:
                # Compress file
                compressed_file = f"{log_file}.gz"
                with open(log_file, 'rb') as f_in:
                    with gzip.open(compressed_file, 'wb') as f_out:
                        f_out.writelines(f_in)
                
                # Remove original
                os.remove(log_file)
                processed += 1
                logger.info(f"Compressed {log_file}")
                
            except Exception as e:
                logger.error(f"Failed to process {log_file}: {str(e)}")
    
    return processed

def cleanup_compressed_logs(log_dir, days_keep):
    """Delete compressed logs older than retention period"""
    cutoff = time.time() - (days_keep * 86400)
    deleted = 0
    
    for gz_file in glob.glob(os.path.join(log_dir, '*.log.gz')):
        if os.stat(gz_file).st_mtime < cutoff:
            try:
                os.remove(gz_file)
                deleted += 1
                logger.info(f"Deleted {gz_file}")
            except Exception as e:
                logger.error(f"Failed to delete {gz_file}: {str(e)}")
    
    return deleted

def main():
    parser = argparse.ArgumentParser(description='Log cleanup utility')
    parser.add_argument('log_dir', help='Directory containing logs')
    parser.add_argument('--compress-days', type=int, default=7,
                       help='Compress logs older than X days')
    parser.add_argument('--delete-days', type=int, default=30,
                       help='Delete compressed logs older than X days')
    args = parser.parse_args()

    try:
        logger.info("Starting log cleanup process")
        
        # Compress old logs
        compressed = compress_old_logs(args.log_dir, args.compress_days)
        logger.info(f"Compressed {compressed} log files")
        
        # Delete old compressed logs
        deleted = cleanup_compressed_logs(args.log_dir, args.delete_days)
        logger.info(f"Deleted {deleted} compressed log files")
        
    except Exception as e:
        logger.error(f"Cleanup failed: {str(e)}")

if __name__ == '__main__':
    main()
'''

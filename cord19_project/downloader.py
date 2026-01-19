"""
downloader.py - Stream CORD-19 from AWS S3 (Unsigned/Public Access)
Memory-safe streaming with progress indicator
"""

import boto3
from botocore import UNSIGNED
from botocore.config import Config
from pathlib import Path
from tqdm import tqdm
import config

# =============================================================================
# S3 CLIENT SETUP (No API Keys Required)
# =============================================================================
def get_s3_client():
    """Create S3 client with unsigned (public) access."""
    return boto3.client(
        's3',
        region_name=config.S3_REGION,
        config=Config(signature_version=UNSIGNED)
    )


def get_file_size(s3_client, bucket: str, key: str) -> int:
    """Get file size in bytes from S3 object metadata."""
    response = s3_client.head_object(Bucket=bucket, Key=key)
    return response['ContentLength']


# =============================================================================
# STREAM DOWNLOAD WITH PROGRESS
# =============================================================================
def download_with_progress(
    s3_client,
    bucket: str,
    key: str,
    output_path: Path,
    chunk_size: int = 8 * 1024 * 1024  # 8MB chunks
) -> Path:
    """Stream download from S3 with progress bar."""
    
    total_size = get_file_size(s3_client, bucket, key)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"[DOWNLOAD] s3://{bucket}/{key}")
    print(f"[SIZE] {total_size / (1024**2):.1f} MB")
    
    response = s3_client.get_object(Bucket=bucket, Key=key)
    body = response['Body']
    
    with open(output_path, 'wb') as f:
        with tqdm(total=total_size, unit='B', unit_scale=True, desc="Progress") as pbar:
            while True:
                chunk = body.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
                pbar.update(len(chunk))
    
    print(f"[SAVED] {output_path}")
    return output_path


# =============================================================================
# MAIN DOWNLOAD FUNCTION
# =============================================================================
def download_cord19_metadata(force_download: bool = False) -> Path:
    """Download CORD-19 metadata.csv from AWS S3."""
    
    output_path = config.RAW_FILE
    
    if output_path.exists() and not force_download:
        size_mb = output_path.stat().st_size / (1024**2)
        print(f"[SKIP] File already exists: {output_path} ({size_mb:.1f} MB)")
        print("   Use force_download=True to re-download")
        return output_path
    
    s3_client = get_s3_client()
    return download_with_progress(
        s3_client=s3_client,
        bucket=config.S3_BUCKET,
        key=config.S3_KEY,
        output_path=output_path
    )


if __name__ == "__main__":
    print("=" * 60)
    print("CORD-19 Downloader - Standalone Test")
    print("=" * 60)
    download_cord19_metadata()

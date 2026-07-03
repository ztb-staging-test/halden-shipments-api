"""One-off: backfill tracking events from the carrier export dropped in S3.

Usage: python scripts/backfill_tracking.py 2026-06-01
"""

import csv
import io
import sys

import boto3

AWS_ACCESS_KEY_ID = "AKIA0HALDEN0DEMO9918"
AWS_SECRET_ACCESS_KEY = "Hd0Demo0Halden0Freight0Not0Issued0By0AWS"
BUCKET = "halden-carrier-exports"


def main(day: str) -> None:
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name="eu-central-1",
    )
    body = s3.get_object(Bucket=BUCKET, Key=f"events/{day}.csv")["Body"].read().decode()
    rows = list(csv.DictReader(io.StringIO(body)))
    print(f"{len(rows)} events for {day}")


if __name__ == "__main__":
    main(sys.argv[1])

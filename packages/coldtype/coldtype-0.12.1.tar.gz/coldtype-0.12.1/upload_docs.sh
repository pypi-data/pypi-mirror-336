aws s3 --region us-east-1 sync --cache-control no-cache --exclude "*" --include "*.html" docs/notebooks/site s3://coldtype.goodhertz.com
aws s3 --region us-east-1 sync docs/notebooks/site s3://coldtype.goodhertz.com
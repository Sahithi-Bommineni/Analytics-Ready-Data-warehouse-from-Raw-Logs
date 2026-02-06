#setup s3 bucket
resource "aws_s3_bucket" "yelp_bronze" {
  bucket = "yelp-raw-data-sahithi"
}

#IAM policy for snowflake
resource "aws_iam_policy" "snowflake_access" {
    name = "SnowflakeS3AccessPolicy" #policy name in AWS
    description = "Allows Snowflake to read/write to Yelp S3 bucket"
    policy = jsonencode({
        Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject", #read files from bucket
          "s3:GetObjectVersion", #read specific versions
          "s3:ListBucket", #list bucket contents
          "s3:PutObject" #write/upload files
        ]
        Effect   = "Allow"      #these permissions are granted to the following
        Resource = [
          "${aws_s3_bucket.yelp_bronze.arn}", #the bucket itself
          "${aws_s3_bucket.yelp_bronze.arn}/*" #objects inside the bucket
        ]
      }
    ]
    })
}

#IAM role for the snowflake
/*esource "aws_iam_role" "snowflake_role" {
  name = "Snowflake_S3_Integration_Role" #name of the role

  assume_role_policy = jsonencode({ #who can use the role
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          AWS = var.snowflake_storage_user_arn
        }
        Condition = {
          StringEquals = {
            "sts:ExternalId" = var.snowflake_external_id
          } # in Snowflake, we will update this with Snowflake's AWS Identity.  
        }
      }
    ]
  })
}*/
data "aws_iam_role" "iam_s3_role" {
  name = "IAM_S3_ROLE"
}

resource "aws_iam_role_policy_attachment" "attach_to_existing" {
  role = data.aws_iam_role.iam_s3_role.name
  policy_arn = aws_iam_policy.snowflake_access.arn
}

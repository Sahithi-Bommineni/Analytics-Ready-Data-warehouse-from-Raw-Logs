#file that holds variables
variable "snowflake_storage_user_arn" {
  type        = string
  description = "The ARN provided by DESC STORAGE INTEGRATION in Snowflake"
}

variable "snowflake_external_id" {
  type        = string
  description = "The External ID provided by DESC STORAGE INTEGRATION in Snowflake"
}

variable "aws_access_key" {
  type        = string
  description = "AWS Access Key for the IAM user with permissions to access S3"
}
variable "aws_secret_key" {
  type        = string
  description = "AWS Secret Key for the IAM user with permissions to access S3"
}
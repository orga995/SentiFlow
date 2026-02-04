provider "aws" {
  region = "us-east-1"
  
  # תגיות שיופיעו על כל המשאבים (עוזר לניהול)
  default_tags {
    tags = {
      Project     = "SentiFlow"
      Environment = "Production"
      Owner       = "DevOps-Student"
      ManagedBy   = "Terraform"
    }
  }
}
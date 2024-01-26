variable "project" {
  description = "project"
  default     = "atomic-airship-410619"
}

variable "credentials" {
  description = "credentials for the service account"
  default     = "./keys/creds.json"
}

variable "region" {
  description = "region"
  default     = "europe-west1-b"
}

variable "location" {
  description = "location"
  default     = "EU"
}


variable "bq_dataset_name" {
  description = "My BigQuery dataset name!"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "My gcs bucket name!"
  default     = "atomic-airship-410619-terra-bucket"
}


variable "gcs_storage_class" {
  description = "storage class for gcp bucket"
  default     = "STANDARD"
}
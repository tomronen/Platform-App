# Platform App

## Introduction

Platform App is a platform application that uses FastAPI to create and manage EKS clusters on AWS. The purpose of the project is to provide an API for creating, retrieving the status of, and deleting EKS clusters.

## Deployment

To deploy the project, follow these steps:

1. Ensure you have Python 3.8 installed.
2. Install the required dependencies using the following commands:
   ```sh
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. Run the application using the following command:
   ```sh
   python main.py
   ```
4. Optionally, you can use the provided CI workflow to automate the deployment process. The CI workflow is available in `.github/workflows/ci.yml`.

## Usage

To use the project, follow these instructions:

1. To create a new EKS cluster, use the `/create-cluster` endpoint by sending a POST request with the required parameters (`cluster_name`, `node_count`, `node_type`).
2. To retrieve the status of an existing cluster, use the `/clusters/{cluster_name}` endpoint by sending a GET request.
3. To delete an existing cluster, use the `/clusters/{cluster_name}` endpoint by sending a DELETE request.

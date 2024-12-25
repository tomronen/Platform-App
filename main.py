from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
import subprocess
import os

app = FastAPI()

class ClusterRequest(BaseModel):
    name: str
    version: str

class ClusterManager:
    def __init__(self):
        self.clusters = {}

    def create_cluster(self, name: str, version: str):
        if name in self.clusters:
            raise ValueError("Cluster already exists")

        os.environ['CDK_DEFAULT_ACCOUNT'] = boto3.client('sts').get_caller_identity().get('Account')
        os.environ['CDK_DEFAULT_REGION'] = boto3.session.Session().region_name

        subprocess.run(["cdk", "deploy", f"--parameters", f"clusterName={name}", f"--parameters", f"clusterVersion={version}"], check=True)
        self.clusters[name] = {"name": name, "version": version}

    def delete_cluster(self, name: str):
        if name not in self.clusters:
            raise ValueError("Cluster does not exist")

        subprocess.run(["cdk", "destroy", f"--parameters", f"clusterName={name}"], check=True)
        del self.clusters[name]

    def list_clusters(self):
        return list(self.clusters.keys())

cluster_manager = ClusterManager()

@app.post("/clusters/")
def create_cluster(request: ClusterRequest):
    try:
        cluster_manager.create_cluster(request.name, request.version)
        return {"message": "Cluster created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/clusters/{name}")
def delete_cluster(name: str):
    try:
        cluster_manager.delete_cluster(name)
        return {"message": "Cluster deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/clusters/")
def list_clusters():
    return {"clusters": cluster_manager.list_clusters()}

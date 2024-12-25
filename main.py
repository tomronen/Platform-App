from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pulumi
import pulumi_aws as aws
import pulumi_eks as eks
import pulumi_kubernetes as k8s
from pulumi_aws import iam

app = FastAPI()

class ClusterRequest(BaseModel):
    cluster_name: str
    node_count: int
    node_type: str

class ClusterResponse(BaseModel):
    cluster_name: str
    status: str

def create_cluster(cluster_name: str, node_count: int, node_type: str):
    # Create an IAM role for the EKS cluster
    eks_role = iam.Role(f"{cluster_name}-eks-role",
                        assume_role_policy=aws.iam.assume_role_policy_for_principal(
                            aws.iam.Principals.Service("eks.amazonaws.com")
                        ))

    # Attach the necessary policies to the IAM role
    iam.RolePolicyAttachment(f"{cluster_name}-eks-policy-attachment",
                             role=eks_role.name,
                             policy_arn="arn:aws:iam::aws:policy/AmazonEKSClusterPolicy")

    # Create the EKS cluster
    cluster = eks.Cluster(cluster_name,
                          role_arn=eks_role.arn,
                          vpc_config=eks.ClusterVpcConfigArgs(
                              subnet_ids=["subnet-12345678", "subnet-87654321"]
                          ))

    # Create a node group for the EKS cluster
    node_group = eks.NodeGroup(f"{cluster_name}-node-group",
                               cluster=cluster.name,
                               node_group_name=f"{cluster_name}-node-group",
                               node_role_arn=eks_role.arn,
                               scaling_config=eks.NodeGroupScalingConfigArgs(
                                   desired_size=node_count,
                                   max_size=node_count,
                                   min_size=node_count
                               ),
                               instance_types=[node_type])

    return cluster

@app.post("/create-cluster", response_model=ClusterResponse)
async def create_cluster_endpoint(request: ClusterRequest):
    try:
        cluster = create_cluster(request.cluster_name, request.node_count, request.node_type)
        return ClusterResponse(cluster_name=cluster.name, status="CREATED")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/clusters/{cluster_name}", response_model=ClusterResponse)
async def get_cluster_status(cluster_name: str):
    try:
        cluster = eks.Cluster.get(cluster_name, cluster_name)
        return ClusterResponse(cluster_name=cluster.name, status=cluster.status)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Cluster not found")

@app.delete("/clusters/{cluster_name}", response_model=ClusterResponse)
async def delete_cluster(cluster_name: str):
    try:
        cluster = eks.Cluster.get(cluster_name, cluster_name)
        cluster.delete()
        return ClusterResponse(cluster_name=cluster_name, status="DELETED")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import * as cdk from '@aws-cdk/core';
import * as eks from '@aws-cdk/aws-eks';
import * as iam from '@aws-cdk/aws-iam';

interface PlatformAppStackProps extends cdk.StackProps {
  clusterName: string;
  clusterVersion: string;
}

export class PlatformAppStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props: PlatformAppStackProps) {
    super(scope, id, props);

    const cluster = new eks.Cluster(this, 'Cluster', {
      clusterName: props.clusterName,
      version: eks.KubernetesVersion.of(props.clusterVersion),
      defaultCapacity: 2,
    });

    const adminRole = new iam.Role(this, 'AdminRole', {
      assumedBy: new iam.AccountRootPrincipal(),
    });

    cluster.awsAuth.addMastersRole(adminRole);
  }
}

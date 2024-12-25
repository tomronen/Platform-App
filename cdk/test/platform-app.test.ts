import { expect as expectCDK, haveResource } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as PlatformApp from '../lib/platform-app-stack';

test('EKS Cluster Created', () => {
  const app = new cdk.App();
  const stack = new PlatformApp.PlatformAppStack(app, 'TestStack', {
    clusterName: 'test-cluster',
    clusterVersion: '1.21',
  });
  expectCDK(stack).to(haveResource('AWS::EKS::Cluster', {
    Name: 'test-cluster',
    Version: '1.21',
  }));
});

test('IAM Role Created', () => {
  const app = new cdk.App();
  const stack = new PlatformApp.PlatformAppStack(app, 'TestStack', {
    clusterName: 'test-cluster',
    clusterVersion: '1.21',
  });
  expectCDK(stack).to(haveResource('AWS::IAM::Role'));
});

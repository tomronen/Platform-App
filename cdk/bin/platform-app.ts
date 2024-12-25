#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { PlatformAppStack } from '../lib/platform-app-stack';

const app = new cdk.App();
new PlatformAppStack(app, 'PlatformAppStack', {
  clusterName: 'my-cluster',
  clusterVersion: '1.21',
});

#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { PlatformAppStack } from '../lib/platform-app-stack';

const app = new cdk.App();
new PlatformAppStack(app, 'PlatformAppStack');

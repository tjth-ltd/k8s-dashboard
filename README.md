# k8s-dashboard-nginx

Installation script for a Kubernetes Dashboard on a local cluster (The installation script assumes that kubectl has full-admin access to the Kubernetes Cluster).

*NOTE: This setup should not be used in production, it allows unauthenticated full admin access to your Kubernetes Dashboard and is for Demo purposes only*

## Nginx Dashboard with Basic Auth

To complete the Dashboard installation, run the installation script from this repository. This script will communicate with your Kubernetes cluster to generate the required pods and services, before updating the docker-compose file with your user Token for the Kubernetes Dashboard

```
python install-dashboard.py
```

## Starting the Dashboard

To start the Dashboard, simply "Up" the docker containers on your host - The Nginx proxy will then be available at http://[your-host]:8080

```
sudo docker-compose up -d
```
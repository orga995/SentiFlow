🚀 SentiFlow - End-to-End DevOps Project
Overview
SentiFlow is a multi-tier microservice application designed for sentiment analysis. The project demonstrates a full CI/CD lifecycle, deploying a Flask-based Frontend, a Python Backend, and a Database into a managed AWS EKS Cluster .
+4

🛠️ Technology Stack

Cloud: AWS (EKS, ECR, VPC, S3, DynamoDB).
+3


Infrastructure as Code: Terraform.
+2


Orchestration: Kubernetes & Helm.
+3


CI/CD: GitHub Actions & ArgoCD.
+4


Monitoring: Prometheus & Grafana.
+3


Networking: Nginx Ingress Controller.
+2

🏗️ Infrastructure (IaC)
The entire infrastructure is provisioned using Terraform:
+1


Networking: Custom VPC with Public/Private subnets across multiple AZs and NAT Gateways.
+1


Compute: Managed AWS EKS Cluster with dedicated Node Groups.
+1


State Management: Remote state stored in S3 with DynamoDB for state locking.
+1

📦 CI/CD Pipeline
We implemented a robust GitHub Flow for continuous integration and delivery:
+1

1. Continuous Integration (GitHub Actions)
Every push to master or a feature/ branch triggers the CI pipeline :
+2


Build: Docker images are built for both Frontend and Backend.
+1


Artifacts: Images are tagged and pushed to Amazon ECR.
+2

2. Continuous Deployment (ArgoCD)
Deployment is managed via ArgoCD following GitOps principles:
+2

The cluster automatically syncs with the Helm charts stored in the repository.
+1

Ensures the "Desired State" in Git matches the "Actual State" in Kubernetes.

📊 Monitoring & Observability
To ensure system reliability, we deployed the kube-prometheus-stack:
+1


Prometheus: Collects metrics from nodes and applications.


Grafana: Visualizes cluster health and resource usage via custom dashboards.

🚀 How to Access

ArgoCD UI: Accessible via Port-forwarding or Ingress.

kubectl port-forward svc/argocd-server -n argocd 8080:443


SentiFlow App: Exposed via Nginx Ingress.
+1


Monitoring: Dashboards available in the Grafana UI.

💡 Final Project Note
This project was completed as part of the "Warriors to Hi-Tech" DevOps program at ORT Singalovski College .
+1

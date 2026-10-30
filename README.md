# secure-payments-gitops-platform
A complete delivery lifecycle of a simulated payments API
# Secure Payments GitOps Platform

A hands-on DevOps and Kubernetes security lab demonstrating the complete
delivery lifecycle of a simulated payments API: automated testing, container
builds, security scanning, GitOps-based deployment, Kubernetes hardening,
monitoring, and operational troubleshooting.

> Scope: personal lab project. The payment endpoint is simulated and does not
> process real transactions or store payment-card information. This is a
> learning environment, not a production payment platform.

## Objectives

- Build and package an application using Docker.
- Automate application validation and image publishing with GitHub Actions.
- Deploy to a Kubernetes cluster bootstrapped with kubeadm.
- Use Argo CD to reconcile Kubernetes resources from Git.
- Apply Kubernetes workload and network security controls.
- Collect application metrics using Prometheus.
- Visualize performance and health using Grafana.
- Document investigation and recovery procedures as operational runbooks.

## Architecture

1. A developer pushes application code or opens a pull request.
2. GitHub Actions runs automated tests, linting, and security checks.
3. A successful main-branch workflow builds and publishes a versioned
   application image to GitHub Container Registry (GHCR).
4. The deployment configuration is updated with the new image version.
5. Argo CD detects the Git change and reconciles the Kubernetes workload.
6. Kubernetes runs the application with explicit resource and security settings.
7. Prometheus collects metrics, while Grafana presents dashboards and alerts.

Git is the desired-state source of truth. Application CI builds and validates
artifacts; Argo CD is responsible for reconciling deployment state.

## Technology Stack

- Docker: container image packaging.
- GitHub Actions: CI workflow, validation, image build, and publication.
- GitHub Container Registry: versioned container images.
- Ubuntu Server, containerd, kubeadm, kubelet, and kubectl: Kubernetes lab.
- Calico: cluster networking and NetworkPolicy enforcement.
- Kubernetes and Kustomize: declarative application configuration.
- Argo CD: GitOps reconciliation and deployment health.
- Prometheus: metric collection and alert rules.
- Grafana: dashboards and investigation.
- Trivy: image and/or filesystem vulnerability scanning.
- Helm: installation of the monitoring stack.

## Kubernetes Security Controls

The application workload is configured to use, where applicable:

- A non-root runtime user.
- `allowPrivilegeEscalation: false`.
- A read-only root filesystem.
- Dropped Linux capabilities.
- The RuntimeDefault seccomp profile.
- CPU and memory requests and limits.
- Liveness and readiness probes.
- A dedicated ServiceAccount and disabled automatic token mounting when
  the workload does not need Kubernetes API access.
- Namespace Pod Security Admission enforcement with the `restricted` profile.
- NetworkPolicies that limit allowed pod traffic.
- Versioned images rather than an unpinned `latest` tag.

The Dockerfile uses an appropriate minimal base image, avoids embedding
credentials, and runs the application as a non-root user.

The CI workflow scans the source and/or image with Trivy. A passing scan is
not proof that an image is vulnerability-free; findings must be assessed
against severity, exploitability, and the application's exposure.

## CI/CD and GitOps

### Continuous integration

The GitHub Actions workflow is intended to:

1. Check out the repository.
2. Install application dependencies.
3. Run automated tests and linting.
4. Build the Docker image.
5. Perform the configured security scans.
6. Publish a uniquely versioned image on the permitted branch/event.
7. Update the deployment configuration with the new image version.

The workflow uses the minimum required token permissions. Package publishing
uses the GitHub token rather than a hard-coded registry password.

### Continuous delivery

Argo CD watches the repository path containing the lab manifests.

The desired image version is recorded in Git. Argo CD compares this desired
state with the live cluster and reconciles permitted differences according
to the configured sync policy.

A rollback is performed by restoring the previous known-good version in Git
and allowing Argo CD to reconcile it. A manual change to the live cluster is
not a substitute for updating the desired state.

## Observability

The application exposes:

- A liveness endpoint.
- A readiness endpoint.
- A Prometheus-compatible metrics endpoint.

The Grafana dashboard is designed to show:

- Request rate.
- Request error rate.
- Request latency, including a percentile view where histogram data is available.
- Application and Kubernetes workload health.

An example alert detects application unavailability or an elevated error rate.
Every alert should have a documented investigation or recovery procedure.

## Repository Structure

- `app/`: application source and tests.
- `.github/workflows/`: CI configuration.
- `k8s/base/`: reusable Kubernetes resources.
- `k8s/overlays/lab/`: lab-specific configuration.
- `argocd/`: Argo CD Application resource.
- `monitoring/`: metric scraping and alert configuration.
- `dashboards/`: exported Grafana dashboard.
- `docs/runbooks/`: troubleshooting and operational procedures.

## Lab Setup

The cluster runs locally in VMware on an Ubuntu Server VM. Kubernetes is
installed with kubeadm and containerd; Calico supplies pod networking.

After the cluster and CNI are healthy:

1. Install Helm.
2. Install Argo CD in the `argocd` namespace.
3. Configure the Argo CD Application to watch `k8s/overlays/lab`.
4. Install `kube-prometheus-stack` in a dedicated monitoring namespace.
5. Configure metric discovery and apply the application manifests.
6. Verify rollout health, probes, security settings, and metric collection.

The lab services are accessed locally using `kubectl port-forward`.
No administrative interfaces are exposed directly to the public internet.

## Verification and Demonstration

A successful demonstration should show:

- A passing automated test and CI workflow.
- A versioned image published to GHCR.
- A Kubernetes Deployment and Service running in the cluster.
- The expected security context on the running Pod.
- NetworkPolicy resources applied and tested.
- Argo CD reporting a healthy, synchronized application.
- A Git change resulting in the expected application version.
- Prometheus scraping the application metrics.
- A Grafana dashboard and at least one useful alert rule.
- A troubleshooting runbook for a failed rollout or increased error rate.

## Operational Runbooks

### Failed Pod or rollout

Inspect the pod state, Events, current and previous container logs, image
pull status, resource availability, probes, and security-context failures.
Record the actual root cause rather than immediately deleting or restarting
the workload.

### Elevated error rate

Confirm the alert and its time window, check whether the issue began after a
deployment, inspect application logs and request metrics, verify dependency
health, and decide whether to roll back the image or mitigate the failing
dependency. Validate recovery after the change.

## Design Decisions and Limitations

- kubeadm is used to understand Kubernetes bootstrap and node components,
  rather than delegating cluster creation to a managed Kubernetes service.
- A single-node local cluster keeps the project affordable and reproducible.
- The single-node lab does not provide high availability or multiple failure
  domains.
- GitOps keeps desired state in version control and separates artifact
  creation from deployment reconciliation.
- Public lab images and repositories are used where appropriate; secrets and
  personal credentials are never committed.
- This simulated API does not represent real payment processing, compliance
  certification, or a production-grade financial platform.

## Future Improvements

- Separate application source and environment configuration into two repos.
- Pin deployed images by digest and introduce image signing and verification.
- Add software bill of materials generation and policy checks.
- Add Falco runtime detection where supported by the lab environment.
- Add resource quotas and additional admission controls.
- Introduce automated deployment promotion between environments.
- Validate the design against a multi-node cluster and failure scenarios.
- Integrate production-grade secret management and a managed state store
  where appropriate.

## Project Status

Personal lab project. This README should be updated to reflect only the
components that have actually been built, tested, and demonstrated.

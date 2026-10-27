# K8S-ENTERPRISE-PROJECT.md
### The Assignment — "Ravenswood" Internal Kubernetes Platform

> **Who this is for:** a DevOps engineer building depth toward **CKA → CKAD → CKS** (Kubernetes v1.35). You operate and secure infrastructure; you do **not** write application code here. The app is a black box you deploy, wire up, and defend.
>
> **How to use these two files — read this or you'll waste the project:**
> 1. Work **only** from this file first. Attempt every task cold, in your own lab. Struggle. Get it wrong.
> 2. Only after you have a working (or broken-but-attempted) result, open `K8S-ENTERPRISE-SOLUTION.md` and compare.
> 3. Retrieval beats re-reading. If you read the solution first, you'll recognise it on the page and fail to reproduce it under a 2-hour exam clock. Don't.
>
> **Exam reality check (why this lab looks nothing like EKS):** CKA/CKAD/CKS run on a **self-managed kubeadm cluster** where you SSH into control-plane nodes. ~40% of CKA/CKS (etcd, kubeadm upgrades, static pods, API-server flags) is *impossible* on a managed cloud because the provider hides the control plane. Stages 1–3 are therefore on your own kubeadm cluster. **Stage 4 is AWS EKS and is explicitly NOT exam material** — it's there so you see what "managed" actually takes away and adds.

---

## SECTION A — Objective & Scenario

**Scenario.** Ravenswood Retail is standing up an internal Kubernetes platform to host **Boutique**, a multi-tier commerce application (web frontend → API/checkout → background worker → PostgreSQL + Redis + an internal message queue). You are the platform engineer. Over four stages you take it from bare Linux VMs to a hardened cluster, then mirror it onto managed cloud.

**The application (you do not build it).** Use an off-the-shelf polyglot demo so 100% of your effort is Kubernetes, not code:
- Primary: **Google "Online Boutique"** (`microservices-demo`) — 10+ services, gRPC, a load generator. Realistic tiering.
- Alternative: **"Sock Shop"** if you want a queue/DB split that maps more obviously to tiers.

You will deploy it, expose it, scale it, isolate it, harden it, and migrate it. You will never open its source.

**The four-stage arc (each stage consumes the previous one's output):**

| Stage | Persona | Cert | You end with |
|---|---|---|---|
| 1 | Cluster administrator | **CKA** | A kubeadm cluster you can build, back up, upgrade, and repair |
| 2 | Platform/deploy engineer | **CKAD** (ops lens) | Boutique running well: Helm/Kustomize, probes, autoscaling, config |
| 3 | Security engineer | **CKS** | The same cluster + app hardened and audited |
| 4 | Cloud platform engineer | *(none — production)* | Boutique on EKS; a written diff of what managed cloud changed |

**Sequencing rule you cannot break:** CKS requires you to have **passed CKA first**. So the cert order is fixed: CKA, then CKAD (fast for you — mostly revision), then CKS.

---

## SECTION B — Bare-Minimum Infrastructure Setup

Goal: the smallest **non-default** cluster that still lets you practise everything. "Non-default" means you build it yourself with kubeadm, not `eksctl create cluster`.

**Topology:** 3 nodes — 1 control-plane, 2 workers.

**Recommended host:** 3× AWS EC2 `t3.medium` (2 vCPU / 4 GB) on Ubuntu 22.04, same VPC/subnet, security group open between them on the K8s ports. This reuses the AWS account you'll need in Stage 4. **Stop the instances when idle** — this is a few dollars, not free tier. Local `multipass`/Vagrant works too if you'd rather keep it off-cloud.

**Bootstrap checklist (do this from memory — commands are in the solution):**
1. On all 3 nodes: disable swap, load `overlay` + `br_netfilter`, set the sysctl bridge/forwarding params.
2. Install a CRI runtime (**containerd**), set `SystemdCgroup = true`.
3. Install `kubeadm`, `kubelet`, `kubectl` pinned to the **v1.35** minor (so you can practise the upgrade *from* 1.34 later — see Stage 1, Task 1.5).
4. `kubeadm init` on the control-plane with an explicit `--pod-network-cidr`.
5. Install a CNI that **supports NetworkPolicy** — use **Calico** (Cilium is fine too). Flannel will bite you in Stage 3 because it ignores NetworkPolicy.
6. `kubeadm join` the two workers.
7. Set up your shell: `kubectl` alias, `k` completion, and the exam `export do="--dry-run=client -o yaml"` / `export now="--force --grace-period=0"` muscle memory.

**Definition of done for Section B:** `kubectl get nodes` shows 3 `Ready`, and a test pod on worker-1 can `curl` a test pod on worker-2 (proves CNI + cross-node networking).

---

## SECTION C — The Three Interrelated Problem Statements (+ Stage 4 capstone)

Each task is tagged with the exam domain it trains. Weights are the official v1.35 curriculum weights, so you can see where to spend time.

### STAGE 1 — Administration (CKA)
*CKA weights: Troubleshooting 30% · Cluster Architecture/Install/Config 25% · Services & Networking 20% · Workloads & Scheduling 15% · Storage 10%.*

- **Task 1.1 — RBAC for the app team.** Create a namespace `boutique`, a ServiceAccount `deployer`, and a Role/RoleBinding that lets `deployer` manage Deployments/Services/ConfigMaps in `boutique` **only** — no cluster-wide access, no secrets read. Prove it with `kubectl auth can-i`. *(Cluster Architecture/Config)*
- **Task 1.2 — Dynamic storage.** Define a StorageClass and make PostgreSQL's data survive a pod delete via a PVC bound to a dynamically provisioned PV. Show the PV is `Bound` and data persists across a pod restart. *(Storage)*
- **Task 1.3 — Expose Boutique.** Publish the frontend two ways: a classic **Ingress**, and again with the **Gateway API** (`Gateway` + `HTTPRoute`). Explain in one line when you'd pick Gateway API. *(Services & Networking — Gateway API is new in the 2025 CKA)*
- **Task 1.4 — etcd backup & restore.** Take a snapshot with `etcdctl`, delete a namespace to simulate disaster, restore from the snapshot, prove the namespace is back. *(Cluster Architecture — a near-guaranteed exam task; impossible on EKS)*
- **Task 1.5 — Cluster upgrade.** Upgrade the cluster one minor version (1.34 → 1.35) with `kubeadm upgrade`, draining and uncordoning each node in the correct order (control-plane first). *(Cluster Architecture — impossible on EKS)*
- **Task 1.6 — Scheduling control.** Taint worker-2 so only the `worker` tier tolerates it; use nodeAffinity to keep PostgreSQL off it. *(Workloads & Scheduling)*
- **Task 1.7 — Break/fix drill (do this blind).** Have a colleague or a script (a) stop the kubelet on a worker, (b) corrupt the `kube-apiserver` static pod manifest, (c) misconfigure a Service selector. Diagnose and fix all three by reading logs/`journalctl`/`crictl`, not by guessing. *(Troubleshooting — 30%, the single biggest exam bucket)*

### STAGE 2 — Deployment & Operations (CKAD, platform-engineer lens)
*CKAD weights: App Env/Config/Security 25% · Design & Build 20% · Deployment 20% · Services & Networking 20% · Observability 15%. You're operating the app, not writing it.*

- **Task 2.1 — Package it.** Deploy Boutique with its **Helm** chart into `boutique`; then create a **Kustomize** overlay that changes replica counts and image tags for a `staging` vs `prod` namespace without editing the base. *(Deployment)*
- **Task 2.2 — Config & secrets.** Externalise the frontend's runtime config into a ConfigMap and the DB credentials into a Secret; mount both. Change a ConfigMap value and trigger a rollout. *(App Env/Config/Security)*
- **Task 2.3 — Health.** Add correct **liveness, readiness, and startup** probes to the API service. Deliberately make readiness fail and show traffic stops routing to that pod. *(Observability)*
- **Task 2.4 — Autoscale.** Add an **HPA (autoscaling/v2)** on the API driven by CPU; drive load with the demo's load generator and watch it scale. *(Deployment / Workloads)*
- **Task 2.5 — Batch.** Add a **CronJob** that runs a nightly "reconciliation" against the DB, and a one-shot **Job** for a migration. Handle failure/backoff. *(Design & Build)*
- **Task 2.6 — Sidecar.** Add a **logging sidecar** (a second container tailing a shared `emptyDir`) to one service — the canonical multi-container pattern. *(Design & Build)*
- **Task 2.7 — Tier isolation (first pass).** Write a **NetworkPolicy** so only the API can reach PostgreSQL; the frontend cannot. *(Services & Networking — sets up Stage 3)*
- **Task 2.8 — Safe rollout.** Do a rolling update, verify zero-downtime with the load generator running, then `kubectl rollout undo`. *(Deployment)*

### STAGE 3 — Security & Hardening (CKS)
*CKS weights: Minimize Microservice Vulns 20% · Supply Chain 20% · Monitoring/Logging/Runtime 20% · Cluster Setup 15% · Cluster Hardening 15% · System Hardening 10%. Requires CKA passed.*

- **Task 3.1 — Benchmark the cluster.** Run **kube-bench** (CIS) against control-plane and nodes; fix at least five FAIL findings. *(Cluster Setup)*
- **Task 3.2 — Harden the API server.** Turn on **audit logging** with a policy, disable anonymous auth / insecure settings, and set appropriate `--authorization-mode`. *(Cluster Hardening — you can only do this because you own the control plane)*
- **Task 3.3 — Encrypt secrets at rest.** Configure an **EncryptionConfiguration** (`aescbc`/`secretbox`) on the API server and re-encrypt existing secrets. *(Cluster Hardening — note how EKS replaces this with KMS in Stage 4)*
- **Task 3.4 — Default-deny networking.** Replace 2.7's single policy with a **namespace-wide default-deny** ingress+egress, then allow only the required flows. *(Cluster Setup)*
- **Task 3.5 — Least privilege.** Audit RBAC; remove any wildcard verbs; disable `automountServiceAccountToken` where the app doesn't need the API. *(Cluster Hardening)*
- **Task 3.6 — Pod hardening.** Enforce **Pod Security Standards `restricted`** on `boutique`; add `securityContext` (non-root, read-only rootfs, drop ALL caps) and a **seccomp** `RuntimeDefault` profile; apply an **AppArmor** profile to one workload. *(Minimize Microservice Vulns / System Hardening)*
- **Task 3.7 — Supply chain gate.** Scan the images with **Trivy**; write an admission policy (**Kyverno** or a `ValidatingAdmissionPolicy`) that blocks images that are `:latest`, unsigned, or from a registry not on your allowlist. *(Supply Chain)*
- **Task 3.8 — Runtime detection.** Install **Falco**; trigger a rule (e.g. a shell spawned inside a container) and read the alert. *(Monitoring/Logging/Runtime)*
- **Task 3.9 — Sandbox (stretch).** Run one workload under **gVisor (runsc)** via a RuntimeClass. *(Minimize Microservice Vulns)*

### STAGE 4 — EKS Production Mirror (NOT exam material — production reality)
*Zero exam value. Full job value. This is where your original AWS spec lives.*

- **Task 4.1 — Provision.** Stand up an EKS cluster with **Terraform** (or `eksctl`) — custom **managed node group**, non-default VPC/subnets, CoreDNS/kube-proxy/VPC-CNI add-ons.
- **Task 4.2 — Identity.** Give the checkout service AWS access (say, an S3 bucket for receipts) via **IRSA** — OIDC provider + IAM role + annotated ServiceAccount. **No node-wide credentials.**
- **Task 4.3 — Secrets.** Enable **KMS envelope encryption** for etcd secrets — the managed replacement for Task 3.3, which you now *cannot* configure yourself.
- **Task 4.4 — Scaling.** Install **Karpenter** (or Cluster Autoscaler); trigger a scale-up by scheduling unschedulable pods and watch nodes appear.
- **Task 4.5 — Ingress.** Expose Boutique with the **AWS Load Balancer Controller** (ALB) instead of your kubeadm Ingress.
- **Task 4.6 — The deliverable that matters.** Write a one-page **diff**: for each Stage 1–3 task, note what EKS *took away* (control-plane access, etcd, API-server flags) and what it *added* (IRSA, KMS, Karpenter, VPC CNI, ELB). This document is the actual point of Stage 4.

---

## SECTION D — Technical Hints & Guided Topics (study *before* you start each stage)

**Global exam logistics**
- Exams are on **Kubernetes v1.35**, hands-on, in a browser terminal, ~2 hours, open-book against `kubernetes.io/docs` only.
- Buy the exam → you get **2 killer.sh** simulator sessions. They are harder than the real exam. Treat a killer.sh run as your readiness gate, not practice.
- Live in `kubectl ... $do` (dry-run to YAML) and `kubectl explain` — you will not have time to hand-write manifests.

**Stage 1 (CKA) — study first:** kubeadm cluster lifecycle; static pods in `/etc/kubernetes/manifests`; `etcdctl snapshot save/restore`; the drain→upgrade→uncordon order; RBAC verbs/resources; StorageClass/PV/PVC binding modes; Gateway API (`gateway.networking.k8s.io/v1`). Docs: Cluster Administration, "Backing up an etcd cluster", "Upgrading kubeadm clusters".

**Stage 2 (CKAD) — study first:** the difference between the three probe types (most people misuse startup vs liveness); `autoscaling/v2` HPA; Helm values vs Kustomize overlays (know when each wins); multi-container patterns (sidecar/init/ambassador). Docs: Configure Liveness/Readiness/Startup Probes; Horizontal Pod Autoscaling; Kustomize.

**Stage 3 (CKS) — study first:** CIS Benchmark + kube-bench; API-server security flags; `EncryptionConfiguration`; NetworkPolicy semantics (default-deny is additive-allow); Pod Security Standards vs the old PSP; seccomp/AppArmor wiring; Trivy; admission control (Kyverno / `ValidatingAdmissionPolicy`); Falco rules; audit policy. Docs: "Encrypting Secret Data at Rest", "Pod Security Standards", "Restrict a Container's Syscalls with seccomp".

**Stage 4 (EKS) — study first (job, not exam):** EKS control-plane architecture; the **IRSA/OIDC** token-exchange flow (`AssumeRoleWithWebIdentity`); Karpenter provisioners/NodePools; VPC CNI IP allocation; the AWS Load Balancer Controller. Docs: AWS EKS User Guide (IRSA, Karpenter), Terraform `terraform-aws-modules/eks`.

**Where to be honest with yourself:** the boring Stage-1 troubleshooting drills (Task 1.7) are 30% of CKA and the thing that actually fails candidates. Do them more than feels necessary. The app-layer tasks (Stage 2) you likely half-know already from Helm/ArgoCD — move fast there. CKS is your growth frontier and the most AI-resistant skill in the set — spend real time in Stage 3.

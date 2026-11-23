## Azzeddine Lachgar

DevOps engineer building multi-tenant Kubernetes platforms that are zero-trust by default and know what every tenant costs in watts.

Kubestronaut: CKA · CKAD · CKS · KCNA · KCSA

### Upstream contributions

| Project | PR | Status |
|---|---|---|
| [Kepler](https://github.com/sustainable-computing-io/kepler) (CNCF) | [Parse positional QEMU `-name` values, so VMs get their real name](https://github.com/sustainable-computing-io/kepler/pull/2764) | merged |
| [Capsule](https://github.com/projectcapsule/capsule) (CNCF) | [Skip quotas of namespaces deleted during the tenant sync](https://github.com/projectcapsule/capsule/pull/2314) | merged |
| [Kamaji](https://github.com/clastix/kamaji) | [Standard `Ready` condition on TenantControlPlane](https://github.com/clastix/kamaji/pull/1419) | merged |
| Capsule | [Namespace quota race under concurrent creates](https://github.com/projectcapsule/capsule/pull/2317) | in review |
| Kamaji | [Default `networkProfile` so its port default applies](https://github.com/clastix/kamaji/pull/1433) | in review |
| Kamaji | [Run tenant control planes under the restricted Pod Security Standard](https://github.com/clastix/kamaji/pull/1432) | in review |

### Projects

- **[joule-budget](https://github.com/lachgar-Azzeddine/joule-budget)**: an energy budget per tenant. It measures each tenant's joules with Kepler, and when a tenant spends its daily budget it puts the tenant to sleep: Kamaji control plane scaled to zero, workloads stopped, Capsule tenant cordoned, worker VMs shut down through Proxmox. Everything comes back at the next window.
- **[kamaji-trustd](https://github.com/lachgar-Azzeddine/kamaji-trustd)**: a trustd sidecar for Kamaji, so Talos Linux workers can join a hosted control plane and get their apid certificates.

### Homelab

Both projects come from Project Joule, a homelab on one mini PC:
- Proxmox with a Talos Linux hub cluster.
- Tenants get Capsule namespaces and their own Kamaji clusters.
- Workloads get SPIFFE identities, and secrets live in OpenBao.
- Everything is deployed with Argo CD.
- Every watt is measured with Kepler.
- Images are signed with cosign and carry SLSA provenance.

Writing at [azzhomelab.tech](https://azzhomelab.tech).

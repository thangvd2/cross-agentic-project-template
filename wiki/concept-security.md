---
tags: [concept, security]
products: [vault-core]
sources:
  - raw/vault-core-overview/vault_core_overview_vault_security.md
  - raw/vault-core-overview/vault_core_overview_architecture.md
last_updated: 2026-04-21
---

# Security

Vault Core bakes security into the product development lifecycle from inception, using threat modeling, code scanning, penetration testing, and shared responsibility.

## Shared Responsibility Model

Security is shared between Thought Machine and the client. The exact division depends on the deployment model:
- **Bank-Hosted**: The client bears more responsibility for infrastructure, network, and database security.
- **SaaS**: Thought Machine manages the underlying cloud infrastructure, while the client focuses on identity access management and client-side configuration.

> **Diagram Summary**: In a bank-hosted deployment, responsibility is cleanly divided:
> - **Client responsibilities**: Identity & Access Management, Platform configuration, Data Protection, Audit Logs, Network security, and threat Detection.
> - **Thought Machine responsibilities**: Secure Software Development, Third-Party Audits, Third-Party Penetration Testing, and internal Corporate Security.

## Compliance and Certifications

Vault Core environments and operations align with major compliance standards, including:
- **ISO 27001** (Information Security Management)
- **ISO 22301** (Business Continuity)
- **SOC 2 Type 2** (Confidentiality, Integrity, Availability)

## Data Protection

- **Encryption in Transit**: All connections (Core APIs, UI, Kafka streaming, Postgres) are encrypted using TLS (typically 1.2 or 1.3).
- **Encryption at Rest**: Data is encrypted using AES 256. Bank-hosted clients may use Customer Managed Keys (CMK) to encrypt CSP keys for additional privacy.
- **Secrets Management**: Vault Core uses Hashicorp Vault (or AWS Secrets Manager) to securely store and govern access to secrets via short-lived tokens.

## Authentication and Access Control

Vault Core implements authentication and least-privilege access control across three main areas:
1. **Interactive Access**: The Operations Dashboard integrates with client SAML 2.0 Identity Providers (e.g., Okta, Azure AD) to manage user roles.
2. **Programmatic Access**: Core APIs are secured using JSON Web Tokens (JWT) signed by a client's private key. Vault Core validates claims using Rego policies evaluated via the Open Policy Agent (OPA) framework.
3. **Streaming APIs**: Authenticated via mutual TLS (mTLS), client-configured Access Control Lists (ACLs), or SASL protocols.

## Security in Product Development

Thought Machine employs Secure Software Development Lifecycle (SSDLC) practices:
- **Threat Modelling**: Based on STRIDE methodology.
- **Code Scanning**: SAST, DAST, known CVE scanning, and third-party library testing.
- **Penetration Testing**: Independent testing of APIs and SaaS configuration.

## See Also
- [[entity-vault-core]]: Overview of the Vault Core platform.
- [[concept-architecture]]: How the distributed Kubernetes architecture supports the security model.

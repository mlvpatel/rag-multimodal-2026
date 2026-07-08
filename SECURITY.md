# Security Policy

## Supported versions

This project is maintained on the `main` branch, which always carries the latest security patched dependencies. The most recent release receives security updates. Older snapshots are not separately maintained.

## Reporting a vulnerability

Please do not open a public issue for security problems.

Report a vulnerability privately through GitHub: open the repository Security tab and choose "Report a vulnerability". This creates a private advisory visible only to the maintainer.

You can expect an initial response within a few days. If the report is confirmed, a fix will be prepared and released, and you will be credited in the advisory unless you prefer otherwise. If it is declined, you will receive a short explanation.

## Scope

This policy covers the application code in this repository. Dependency vulnerabilities are tracked with pip-audit in CI and patched by updating the pinned versions. You are welcome to flag any that slip through.

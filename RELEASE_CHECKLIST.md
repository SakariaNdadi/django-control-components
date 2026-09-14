# 0.1.0 release checklist

The project remains at `0.0.1` while components and experimental capabilities
develop. Promotion to `0.1.0` still requires every gate below to pass.

## Required gates

- [ ] `uv run pytest -q` passes without unexpected warnings.
- [ ] `uv run nox -s lint typecheck coverage packaging` passes.
- [ ] The Playwright suite passes in Chromium and Firefox in CI.
- [ ] Core and Studio wheels install and render from an isolated consumer environment.
- [ ] Action-bearing tables use per-request factories; no rendered owner is stored globally.
- [ ] `DEBUG=False`, collected-static, CSP, WSGI, and ASGI deployment smoke tests pass.
- [ ] The demo completes a multi-worker, two-user authorization soak test.
- [ ] README feature status, changelog, migration guide, and package versions agree.
- [ ] Public imports and the supported Python/Django matrix are documented.
- [ ] TestPyPI artifacts are installed in two projects outside this repository.
- [ ] No unresolved critical or high security finding remains.

## Release procedure

1. Freeze features and clear the `0.1.0` defect milestone.
2. Run every required gate from a clean checkout.
3. Publish `0.1.0rc1` to TestPyPI and install both distributions externally.
4. Soak the release candidate for at least 24 hours under multiple workers.
5. Fix only release-blocking defects; publish another candidate when artifacts change.
6. Date the changelog, create the signed tag, and publish the GitHub release.
7. Verify PyPI attestations and repeat the clean consumer installation.

## Explicitly deferred

- Production AI execution or a bundled AI-provider dependency.
- Client-side formset row insertion and nested relation managers.
- Making HTMX 4 the default before its stable release and contract-suite approval.

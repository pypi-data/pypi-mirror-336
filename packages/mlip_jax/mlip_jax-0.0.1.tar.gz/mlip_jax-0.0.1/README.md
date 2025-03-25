# ⚛️ MLIP-JAX: SOTA Machine-Learning Interatomic Potentials in JAX 🚀

This is a placeholder file for the README of the open-source repo.

Steps for transforming internal repo to open-source one:

### COPY OVER

- `.github`
- `docs`
- `mlip_jax`
- `tests`
- `.gitignore`
- `.pre-commit-config.yaml`
- `LICENSE`
- `CHANGELOG`

### DELETE AFTER COPYING OVER

- `tests/experiments`
- `docs/repo_experiments`

### MORE COMPLEX COPIES

- `open_source/pyproject.toml` to `pyproject.toml`
- `open_source/README.md` to `README.md`
- `open_source/docs/index.rst` to `docs/source/index.rst` (OVERWRITING)
- `open_source/ci` to `open_source/ci`

When pushing the resulting branch to the open-source repo, we also need to replace
the CI. We can do that by copying `open_source/ci` to `.github/workflows` after first
deleting all previous content of `.github/workflows`.

# ⚛️ MLIP-JAX: SOTA Machine-Learning Interatomic Potentials in JAX 🚀

## 👀 Overview

MLIP-JAX is a Python library for training and deploying
**Machine Learning Interatomic Potentials (MLIP)** written in JAX. It provides
the following functionality:
- Multiple model architectures (for now: MACE, NequIP and ViSNet)
- Dataset loading and preprocessing
- Training and fine-tuning MLIP models
- Batched inference with trained MLIP models
- MD simulations with MLIP models using multiple simulation backends (for now: JAX-MD and ASE)
- Energy minimizations with MLIP models using the same simulation backends as for MD.

The purpose of the library is to provide users with a toolbox
to deal with MLIP models in true end-to-end fashion.
Hereby we follow the key design principles of (1) **easy-of-use** also for non-expert
users that mainly care about applying pre-trained models to relevant biological or
material science applications, (2) **extensibility and flexibility** for users more
experienced with MLIP and JAX, and (3) a focus on **high inference speeds** that enable
running long MD simulations on large systems which we believe is necessary in order to
bring MLIP to large-scale industrial application.

See the [Installation](#-installation) section for details on how to install
MLIP-JAX and the example Google Colab notebooks linked below for a quick way
to get started. For detailed instructions, visit our extensive
[code documentation](https://mlip-jax-dot-int-research-tpu.uc.r.appspot.com).

## 📦 Installation

MLIP-JAX can be installed via pip like this:

```bash
pip install mlip-jax
```

This command will install a regular CPU-based version of JAX. However, we recommend
to run MLIP workloads on GPU or TPU, hence, it will be required to install the
necessary versions of `jaxlib` which can also be installed via pip. See
the [installation guide of JAX](https://docs.jax.dev/en/latest/installation.html) for
more information.

## :zap: Examples

In addition to the tutorials provided as part of our
[code documentation](https://mlip-jax-dot-int-research-tpu.uc.r.appspot.com),
we also provide example notebooks in Google Colab format that can be used as
simple templates to build your own MLIP pipelines:
- Training a model: LINK
- Running an MD simulation: LINK
- Batched inference: LINK

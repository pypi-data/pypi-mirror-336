import jax.numpy as jnp
import jax
import equinox as eqx
from jaxtyping import Array, Float, Integer
from plum import dispatch
from typing import Optional
from numbers import Real

ZERO = 1e-20


class NormalInverseGamma(eqx.Module):
    m: Float[Array, "*batch n_dim"]
    l: Float[Array, "*batch n_dim"]
    a: Float[Array, "*batch n_dim"]
    b: Float[Array, "*batch n_dim"]


class Dirichlet(eqx.Module):
    alpha: Float[Array, "*batch n_dim k"]

    def __getitem__(self, key):
        return Dirichlet(alpha=self.alpha[key])


class Normal(eqx.Module):
    mu: Float[Array, "*batch n_dim"]
    std: Float[Array, "*batch n_dim"]

    def __getitem__(self, key):
        return Normal(mu=self.mu[key], std=self.std[key])


class Categorical(eqx.Module):
    # assumed normalized, padded
    logprobs: Float[Array, "*batch n_dim k"]

    def __getitem__(self, key):
        return Categorical(logprobs=self.logprobs[key])


BaseF = Categorical | Normal
BaseG = NormalInverseGamma | Dirichlet


class Mixed(eqx.Module):
    dists: tuple[BaseF, ...]

    def __getitem__(self, key):
        return Mixed(dists=tuple([dist[key] for dist in self.dists]))


F = BaseF | Mixed


class MixedConjugate(eqx.Module):
    dists: tuple[BaseG, ...]


class GEM(eqx.Module):
    alpha: Float[Array, "*batch"]
    d: Float[Array, "*batch"]


class Cluster(eqx.Module):
    c: Float[Array, "*batch n"]
    pi: Float[Array, "*batch k"]
    f: Float[Array, "*batch k"]

    def __getitem__(self, key):
        return Cluster(self.c[key], self.pi[key], self.f[key])


class Trace(eqx.Module):
    gem: GEM
    g: NormalInverseGamma | Dirichlet | MixedConjugate
    cluster: Cluster


BaseDatapoint = Float[Array, "*batch n_c"] | Integer[Array, "*batch n_d"]
Datapoint = BaseDatapoint | tuple[BaseDatapoint, ...]


class MixtureModel(eqx.Module):
    # mask: Datapoint
    pi: Float[Array, "*batch k"]
    f: F


@dispatch
def sample(key: Array, dist: Dirichlet) -> Categorical:
    probs = jax.random.dirichlet(key, dist.alpha)
    probs = jnp.where(probs == 0, ZERO, probs)

    return Categorical(jnp.log(probs))


@dispatch
def sample(key: Array, dist: NormalInverseGamma) -> Normal:
    """See Kevin Murphy's Conjugate Bayesian analysis of the Gaussian distribution:
    https://www.cs.ubc.ca/~murphyk/Papers/bayesGauss.pdf"""
    keys = jax.random.split(key)

    log_lambda = jax.random.loggamma(key, dist.a) - jnp.log(dist.b)
    log_sigma = -jnp.log(dist.l) - log_lambda
    std = jnp.exp(log_sigma / 2)
    mu = dist.m + jax.random.normal(keys[1], shape=dist.m.shape) * std

    return Normal(mu=mu, std=jnp.exp(-log_lambda / 2))


@dispatch
def sample(key: Array, dist: MixedConjugate) -> Mixed:
    keys = jax.random.split(key, len(dist.dists))
    dists = tuple([sample(keys[i], dist.dists[i]) for i in range(len(dist.dists))])

    return Mixed(dists=dists)


@dispatch
def sample(key: Array, dist: Normal) -> Float[Array, "n_c"]:
    return dist.mu + dist.std * jax.random.normal(key, shape=dist.mu.shape)


@dispatch
def sample(key: Array, dist: Categorical) -> Integer[Array, "n_D"]:
    return jax.random.categorical(key, dist.logprobs)


@dispatch
def sample(
    key: Array, dist: Mixed
) -> tuple[Float[Array, "n_c"], Integer[Array, "n_d"]]:
    keys = jax.random.split(key, len(dist.dists))
    dists = tuple([sample(keys[i], dist.dists[i]) for i in range(len(dist.dists))])
    return dists


@dispatch
def sample(key: Array, dist: MixtureModel):
    keys = jax.random.split(key)
    cluster = jax.random.categorical(keys[0], dist.pi)
    return sample(key, dist.f[cluster])


@dispatch
def posterior(
    dist: MixedConjugate,
    x: tuple[
        Float[Array, "batch n_normal_dim"], Integer[Array, "batch n_categorical_dim"]
    ],
) -> MixedConjugate:
    dists = tuple([posterior(dist.dists[i], x[i]) for i in range(len(dist.dists))])

    return MixedConjugate(dists=dists)


@dispatch
def posterior(
    dist: MixedConjugate,
    x: tuple[BaseDatapoint, ...],
    c: Integer[Array, "batch"],
    max_clusters: Optional[int] = None,
) -> MixedConjugate:
    dists = tuple(
        [
            posterior(dist.dists[i], x[i], c, max_clusters)
            for i in range(len(dist.dists))
        ]
    )

    return MixedConjugate(dists=dists)


@dispatch
def posterior(
    dist: MixedConjugate,
    x: Integer[Array, "batch n_dim"],
    c: Integer[Array, "batch"],
    max_clusters: Optional[int] = None,
) -> MixedConjugate:
    dists = tuple(
        [
            posterior(dist.dists[i], x[i], c, max_clusters)
            for i in range(len(dist.dists))
        ]
    )

    return MixedConjugate(dists=dists)


###


@dispatch
def posterior(
    dist: NormalInverseGamma,
    x: Float[Array, "batch n_dim"],
    c: Integer[Array, "batch"],
    max_clusters: Optional[int] = None,
) -> NormalInverseGamma:
    N = jax.ops.segment_sum(
        jnp.invert(jnp.isnan(x)).astype(jnp.int32), c, num_segments=max_clusters
    )
    masked_x = jnp.nan_to_num(x, 0.0)
    sum_x = jax.ops.segment_sum(masked_x, c, num_segments=max_clusters)
    sum_x_sq = jax.ops.segment_sum(masked_x**2, c, num_segments=max_clusters)

    return jax.vmap(posterior, in_axes=(None, 0, 0, 0))(dist, N, sum_x, sum_x_sq)


@dispatch
def posterior(
    dist: NormalInverseGamma, x: Float[Array, "batch n_dim"]
) -> NormalInverseGamma:
    N = jnp.sum(jnp.invert(jnp.isnan(x)).astype(jnp.int32), axis=0)
    sum_x = jnp.nansum(x, axis=0)
    sum_x_sq = jnp.nansum(x**2, axis=0)

    return posterior(dist, N, sum_x, sum_x_sq)


@dispatch
def posterior(
    dist: NormalInverseGamma,
    N: Integer[Array, "n_dim"],
    sum_x: Float[Array, "n_dim"],
    sum_x_sq: Float[Array, "n_dim"],
) -> NormalInverseGamma:
    l = dist.l + N
    m = (dist.l * dist.m + sum_x) / l
    a = dist.a + N / 2
    b = dist.b + 0.5 * (sum_x_sq + dist.l * dist.m**2 - l * m**2)

    return NormalInverseGamma(m=m, l=l, a=a, b=b)


@dispatch
def posterior(
    dist: Dirichlet,
    x: Integer[Array, "batch n_dim"],
    c: Integer[Array, "batch"],
    max_clusters: Optional[int] = None,
) -> Dirichlet:
    one_hot_x = jax.nn.one_hot(x, num_classes=dist.alpha.shape[-1], dtype=jnp.int32)
    counts = jax.ops.segment_sum(one_hot_x, c, num_segments=max_clusters)
    return jax.vmap(posterior, in_axes=(None, 0))(dist, counts)


@dispatch
def posterior(dist: Dirichlet, counts: Integer[Array, "n_dim k"]) -> Dirichlet:
    return Dirichlet(alpha=dist.alpha + counts)


@dispatch
def logpdf(dist: Normal, x: Float[Array, "n_dim"]) -> Float[Array, ""]:
    logprob = jnp.nansum(
        -0.5 * jnp.log(2 * jnp.pi)
        - jnp.log(dist.std)
        - 0.5 * ((x - dist.mu) / dist.std) ** 2
    )

    return logprob


@dispatch
def logpdf(dist: Categorical, x: Integer[Array, "n_dim"]) -> Float[Array, ""]:
    return jnp.nansum(
        dist.logprobs.at[jnp.arange(x.shape[-1]), x].get(
            mode="fill", fill_value=jnp.nan
        )
    )


@dispatch
def logpdf(dist: Mixed, x: Datapoint) -> Float[Array, ""]:
    return sum([logpdf(dist.dists[i], x[i]) for i in range(len(dist.dists))])


@dispatch
def logpdf(dist: GEM, pi: Float[Array, "n"], K: Integer[Array, ""]) -> Float[Array, ""]:
    betas = jax.vmap(lambda i: 1 - pi[i] / pi[i - 1])(jnp.arange(len(pi)))
    betas = betas.at[0].set(pi[0])
    logprobs = jax.vmap(jax.scipy.stats.beta.logpdf, in_axes=(0, None, 0))(
        betas, 1 - dist.d, dist.alpha + (1 + jnp.arange(len(pi))) * dist.d
    )
    idx = jnp.arange(logprobs.shape[0])
    logprobs = jnp.where(idx < K, logprobs, 0)
    return jnp.sum(logprobs)


@dispatch
def logpdf(dist: F, x: Datapoint, c: Integer[Array, ""]) -> Float[Array, ""]:
    dist = dist[c]
    return logpdf(dist, x)


@dispatch
def logpdf(dist: MixtureModel, x: Datapoint) -> Float[Array, ""]:
    logprob = jax.vmap(logpdf, in_axes=(0, None))(dist.f, x)
    logprob = logprob + jnp.log(dist.pi)
    return jax.scipy.special.logsumexp(logprob)


@dispatch
def logpdf(dist: MixedConjugate, x: Mixed) -> Float[Array, ""]:
    return sum([logpdf(dist.dists[i], x.dists[i]) for i in range(len(dist.dists))])


@dispatch
def logpdf(dist: NormalInverseGamma, x: Normal) -> Float[Array, ""]:
    """Scores the mu and sigma parameters drawn from an inverse gamma prior.

    Pr[sigma] = Gamma(1/sigma^2; loc=a, scale=1/b)
    Pr[mu] = Normal(mu |  loc=m, scale=sigma/sqrt(l))

    """
    std_logpdf = jax.scipy.stats.gamma.logpdf(x.std**-2, dist.a, scale=1 / dist.b)
    mu_logpdf = jax.scipy.stats.norm.logpdf(
        x.mu, loc=dist.m, scale=x.std / jnp.sqrt(dist.l)
    )
    return jnp.sum(mu_logpdf + std_logpdf)


@dispatch
def logpdf(dist: Dirichlet, x: Categorical) -> Float[Array, ""]:
    logprobs = jax.vmap(jax.scipy.stats.dirichlet.logpdf)(
        jnp.exp(x.logprobs), dist.alpha
    )
    return jnp.sum(logprobs)


def make_trace(
    key: jax.Array,
    alpha: Real,
    d: Real,
    schema: dict,
    data: Datapoint,
    max_clusters: int,
):
    g = make_g(schema)

    n = len(data[0]) if isinstance(data, tuple) else len(data)
    c = jnp.zeros(n, dtype=int)

    if not isinstance(data, tuple):
        data = (data,)
    g_prime = posterior(g, data, c, 2 * max_clusters)

    f = sample(key, g_prime)
    pi = jnp.zeros(max_clusters)
    pi = pi.at[0].set(0.9)
    cluster = Cluster(c=c, f=f, pi=pi)
    gem = GEM(alpha=alpha, d=d)

    return Trace(gem=gem, g=g, cluster=cluster)


def make_g(schema: dict):
    dists = []
    if schema["types"]["normal"]:
        dists.append(make_normal_g(schema))
    if schema["types"]["categorical"]:
        dtypes = schema["var_metadata"]["categorical_precisions"]
        unique_dtypes = list(set(dtypes))
        for dtype in unique_dtypes:
            dists.append(make_categorical_g(schema, dtype))

    return MixedConjugate(dists=dists)


def make_normal_g(schema: dict):
    n_continuous = len(schema["types"]["normal"])

    return NormalInverseGamma(
        m=jnp.zeros(n_continuous),
        l=jnp.ones(n_continuous),
        a=jnp.ones(n_continuous),
        b=jnp.ones(n_continuous),
    )


def make_categorical_g(schema: dict, dtype: int):
    dtypes = schema["var_metadata"]["categorical_precisions"]
    n_discrete = len([d for d in dtypes if dtype == d])
    n_categories = jnp.array(
        [
            len(schema["var_metadata"][col]["levels"])
            for idx, col in enumerate(schema["types"]["categorical"])
            if dtypes[idx] == dtype
        ]
    )
    max_n_categories = jnp.max(n_categories).astype(int)

    cat_alpha = jnp.ones((n_discrete, max_n_categories))
    mask = (
        jnp.tile(jnp.arange(max_n_categories), (n_discrete, 1)) < n_categories[:, None]
    )
    cat_alpha = jnp.where(mask, cat_alpha, ZERO)

    return Dirichlet(alpha=cat_alpha)

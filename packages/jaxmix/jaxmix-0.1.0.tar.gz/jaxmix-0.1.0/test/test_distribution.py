from jaxmix.distributions import (
    Normal,
    Categorical,
    Dirichlet,
    NormalInverseGamma,
    Mixed,
    logpdf,
    posterior,
    sample,
)
import jax.numpy as jnp
import jax


def test_posterior_dirichlet():
    n_dim = 2
    k = 3
    N = 4
    alphas = jnp.array([[1.0, 2.0, 3.0], [3.0, 4.0, -jnp.inf]])
    dirichlet = Dirichlet(alphas)

    # x = jnp.array([[0, 1], [1, 0], [2, 0], [0, 0]])
    counts = jnp.array([[2, 1, 1], [3, 1, 0]])
    # 0, 0, 1, 2 for the first dim
    # 0, 0, 0, 1 for the second dim
    dirichlet_posterior = posterior(dirichlet, counts)
    assert jnp.all(dirichlet_posterior.alpha[0] == jnp.array([1 + 2, 2 + 1, 3 + 1]))
    assert jnp.all(dirichlet_posterior.alpha[1] == jnp.array([3 + 3, 4 + 1, -jnp.inf]))


def test_posterior_nig_with_nans():
    # adapted from cgpm https://github.com/probcomp/cgpm/blob/master/tests/test_teh_murphy.py
    n = jnp.array(10)
    n_dim = 4
    key = jax.random.PRNGKey(1234)
    x = jax.random.normal(key, shape=(n, n_dim))

    # drop some values into NaNs.
    nans = [0, 1, 2, 3]
    i = 0
    for col in range(len(nans)):
        i += 1
        for o in range(nans[col]):
            x = x.at[i, o].set(jnp.nan)

    all_m = jnp.array((1.0, 7.0, 0.43, 1.2))
    all_l = jnp.array((2.0, 18.0, 3.0, 11.0))
    all_a = jnp.array((2.0, 0.3, 7.0, 4.0))
    all_b = jnp.array((1.0, 3.0, 7.5, 22.5))

    h = NormalInverseGamma(all_m, all_l, all_a, all_b)
    h_prime = posterior(h, x)

    def check_posterior(x, mu, l, a, b):
        xbar = jnp.nanmean(x, axis=0)
        N = jnp.sum(jnp.invert(jnp.isnan(x)).astype(jnp.int32))
        ln = l + N
        an = a + N / 2.0
        mun = (l * mu + N * xbar) / (l + N)
        bn = (
            b
            + 0.5 * jnp.nansum((x - xbar) ** 2)
            + l * N * (xbar - mu) ** 2 / (2 * (l + N))
        )
        return mun, ln, an, bn

    mun, ln, an, bn = jax.vmap(check_posterior, in_axes=(1, 0, 0, 0, 0))(
        x, all_m, all_l, all_a, all_b
    )

    assert jnp.allclose(mun, h_prime.m)
    assert jnp.allclose(ln, h_prime.l)
    assert jnp.allclose(an, h_prime.a)
    assert jnp.allclose(bn, h_prime.b)


def test_posterior_nig_cluster_with_nans():
    # adapted from cgpm https://github.com/probcomp/cgpm/blob/master/tests/test_teh_murphy.py
    n = jnp.array(10)
    n_dim = 4
    key = jax.random.PRNGKey(1234)
    x = jax.random.normal(key, shape=(n, n_dim))

    # drop some values into NaNs.
    nans = [0, 1, 2, 3]
    i = 0
    for col in range(len(nans)):
        i += 1
        for o in range(nans[col]):
            x = x.at[i, o].set(jnp.nan)

    all_m = jnp.array((1.0, 7.0, 0.43, 1.2))
    all_l = jnp.array((2.0, 18.0, 3.0, 11.0))
    all_a = jnp.array((2.0, 0.3, 7.0, 4.0))
    all_b = jnp.array((1.0, 3.0, 7.5, 22.5))

    c = jnp.repeat(jnp.array([0, 1, 2, 3]), n)

    h = NormalInverseGamma(all_m, all_l, all_a, all_b)
    h_prime = jax.vmap(posterior, in_axes=(0, None, None))(h, x.T.reshape(-1, 1), c)

    def check_posterior(x, mu, l, a, b):
        xbar = jnp.nanmean(x)
        N = jnp.sum(jnp.invert(jnp.isnan(x)).astype(jnp.int32))
        ln = l + N
        an = a + N / 2.0
        mun = (l * mu + N * xbar) / (l + N)
        bn = (
            b
            + 0.5 * jnp.nansum((x - xbar) ** 2)
            + l * N * (xbar - mu) ** 2 / (2 * (l + N))
        )
        return mun, ln, an, bn

    mun, ln, an, bn = jax.vmap(check_posterior, in_axes=(1, 0, 0, 0, 0))(
        x, all_m, all_l, all_a, all_b
    )

    idxs = ((0, 1, 2, 3), (0, 1, 2, 3))
    assert jnp.allclose(mun, h_prime.m[idxs].ravel())
    assert jnp.allclose(ln, h_prime.l[idxs].ravel())
    assert jnp.allclose(an, h_prime.a[idxs].ravel())
    assert jnp.allclose(bn, h_prime.b[idxs].ravel())


def test_posterior_nig():
    # adapted from cgpm https://github.com/probcomp/cgpm/blob/master/tests/test_teh_murphy.py
    n = jnp.array(100)
    n_dim = 4
    key = jax.random.PRNGKey(1234)
    x = jax.random.normal(key, shape=(n, n_dim))
    sum_x = jnp.sum(x, axis=0)
    sum_x_sq = jnp.sum(x**2, axis=0)

    all_m = jnp.array((1.0, 7.0, 0.43, 1.2))
    all_l = jnp.array((2.0, 18.0, 3.0, 11.0))
    all_a = jnp.array((2.0, 0.3, 7.0, 4.0))
    all_b = jnp.array((1.0, 3.0, 7.5, 22.5))

    h = NormalInverseGamma(all_m, all_l, all_a, all_b)
    h_prime = posterior(h, jnp.repeat(n, n_dim), sum_x, sum_x_sq)

    def check_posterior(x, mu, l, a, b):
        xbar = jnp.mean(x)
        ln = l + n
        an = a + n / 2.0
        mun = (l * mu + n * xbar) / (l + n)
        bn = (
            b
            + 0.5 * jnp.sum((x - xbar) ** 2)
            + l * n * (xbar - mu) ** 2 / (2 * (l + n))
        )
        return mun, ln, an, bn

    mun, ln, an, bn = jax.vmap(check_posterior, in_axes=(1, 0, 0, 0, 0))(
        x, all_m, all_l, all_a, all_b
    )

    assert jnp.allclose(mun, h_prime.m)
    assert jnp.allclose(ln, h_prime.l)
    assert jnp.allclose(an, h_prime.a)
    assert jnp.allclose(bn, h_prime.b)


def test_posterior_nig_cluster():
    # adapted from cgpm https://github.com/probcomp/cgpm/blob/master/tests/test_teh_murphy.py
    n = jnp.array(100)
    n_dim = 4
    key = jax.random.PRNGKey(1234)
    x = jax.random.normal(key, shape=(n, n_dim))

    all_m = jnp.array((1.0, 7.0, 0.43, 1.2))
    all_l = jnp.array((2.0, 18.0, 3.0, 11.0))
    all_a = jnp.array((2.0, 0.3, 7.0, 4.0))
    all_b = jnp.array((1.0, 3.0, 7.5, 22.5))
    c = jnp.repeat(jnp.array([0, 1, 2, 3]), n)

    h = NormalInverseGamma(all_m, all_l, all_a, all_b)
    h_prime = jax.vmap(posterior, in_axes=(0, None, None))(h, x.T.reshape(-1, 1), c)

    def check_posterior(x, mu, l, a, b):
        xbar = jnp.mean(x)
        ln = l + n
        an = a + n / 2.0
        mun = (l * mu + n * xbar) / (l + n)
        bn = (
            b
            + 0.5 * jnp.sum((x - xbar) ** 2)
            + l * n * (xbar - mu) ** 2 / (2 * (l + n))
        )
        return mun, ln, an, bn

    mun, ln, an, bn = jax.vmap(check_posterior, in_axes=(1, 0, 0, 0, 0))(
        x, all_m, all_l, all_a, all_b
    )

    idxs = ((0, 1, 2, 3), (0, 1, 2, 3))
    assert jnp.allclose(mun, h_prime.m[idxs].ravel())
    assert jnp.allclose(ln, h_prime.l[idxs].ravel())
    assert jnp.allclose(an, h_prime.a[idxs].ravel())
    assert jnp.allclose(bn, h_prime.b[idxs].ravel())


def test_posterior_nig_bimodal():
    n = 10000
    n_dim = 2
    max_clusters = 10
    key = jax.random.PRNGKey(1234)
    keys = jax.random.split(key, 6)
    n_data0 = jax.random.normal(keys[0], (n, n_dim)) * 1e-5
    n_data1 = 1 + 1e-5 * jax.random.normal(keys[1], (n, n_dim))
    data = jnp.concatenate((n_data0, n_data1))

    c = jnp.tile(jnp.array([0, max_clusters]), n)
    nig = NormalInverseGamma(
        m=jnp.zeros(2), l=jnp.ones(2), a=jnp.ones(2), b=jnp.ones(2)
    )
    h_prime = posterior(nig, data, c, 2 * max_clusters)
    theta = sample(keys[2], h_prime)

    assert jnp.allclose(theta.std[0], 0.5, atol=1e-2)
    assert jnp.allclose(theta.std[10], 0.5, atol=1e-2)
    assert jnp.allclose(theta.mu[0], 0.5, atol=5e-2)
    assert jnp.allclose(theta.mu[10], 0.5, atol=5e-2)


def test_normal():
    mu = jnp.array([0.0, 1.0])
    std = jnp.array([1.0, 2.0])

    params = Normal(mu=mu, std=std)

    logp = logpdf(params, jnp.array([0.0, 0.0]))

    logp0 = -0.5 * jnp.log(2 * jnp.pi) - jnp.log(1.0) - 0.5 * ((0.0 - 0.0) / 1.0) ** 2
    logp1 = -0.5 * jnp.log(2 * jnp.pi) - jnp.log(2.0) - 0.5 * ((0.0 - 1.0) / 2.0) ** 2
    assert logp == logp0 + logp1


def test_categorical():
    probs = jnp.array([[0.4, 0.6, 0.0], [0.2, 0.3, 0.5]])
    logprobs = jnp.log(probs)

    params = Categorical(logprobs=logprobs)

    logp = logpdf(params, jnp.array([0, 1]))

    logp0 = jnp.log(0.4)
    logp1 = jnp.log(0.3)

    assert logp == logp0 + logp1


def test_mixed():
    mu = jnp.array([0.0, 1.0])
    std = jnp.array([1.0, 2.0])

    normal_params = Normal(mu=mu, std=std)

    probs = jnp.array([[0.4, 0.6, 0.0], [0.2, 0.3, 0.5]])
    logprobs = jnp.log(probs)

    categorical_params = Categorical(logprobs=logprobs)

    mixed_params = Mixed(
        dists=(
            normal_params,
            categorical_params,
        )
    )

    logp = logpdf(mixed_params, (jnp.array([0.0, 0.0]), jnp.array([0, 1])))

    logp_n0 = -0.5 * jnp.log(2 * jnp.pi) - jnp.log(1.0) - 0.5 * ((0.0 - 0.0) / 1.0) ** 2
    logp_n1 = -0.5 * jnp.log(2 * jnp.pi) - jnp.log(2.0) - 0.5 * ((0.0 - 1.0) / 2.0) ** 2

    logp_c0 = jnp.log(0.4)
    logp_c1 = jnp.log(0.3)

    assert logp == logp_n0 + logp_n1 + logp_c0 + logp_c1

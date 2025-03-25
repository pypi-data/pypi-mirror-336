import time
import jax.numpy as jnp
from jax import lax
import jax
from typing import Callable, Tuple
import numpy as np
import os
import hashlib
from pathlib import Path
import shutil
import pickle


def get_cache_dir():
    """Determine the appropriate cache directory based on the OS."""
    if os.name == "nt":  # Windows
        return str(Path(os.getenv("LOCALAPPDATA")) / "Cache" / "cosmologix")
    elif os.name == "posix":  # Unix-like systems
        if "XDG_CACHE_HOME" in os.environ:
            return str(Path(os.environ["XDG_CACHE_HOME"]) / "cosmologix")
        return str(Path.home() / ".cache" / "cosmologix")
    else:
        raise OSError("Unsupported operating system")


jax.config.update("jax_compilation_cache_dir", get_cache_dir())
jax.config.update("jax_persistent_cache_min_entry_size_bytes", -1)
jax.config.update("jax_persistent_cache_min_compile_time_secs", 0.1)
# This is not available in all jax version
try:
    jax.config.update(
        "jax_persistent_cache_enable_xla_caches",
        "xla_gpu_per_fusion_autotune_cache_dir",
    )
except AttributeError:
    pass


def clear_cache(cache_dir=None):
    """
    Clear the cache directory used by cached_download.

    :param cache_dir: Optional directory path for cache. If None, it uses an OS-specific default.
    :return: None
    """
    if cache_dir is None:
        cache_dir = (
            get_cache_dir()
        )  # Assuming get_cache_dir() is defined as in the previous example

    if os.path.exists(cache_dir):
        try:
            shutil.rmtree(cache_dir)  # Remove the entire directory
            print(f"Cache directory {cache_dir} has been cleared.")
        except Exception as e:
            print(f"An error occurred while clearing the cache: {e}")
    else:
        print(f"Cache directory {cache_dir} does not exist.")


def cached_download(url, cache_dir=None):
    """
    Download a file from the web with caching.

    :param url: The URL to download from.
    :param cache_dir: Optional directory path for cache. If None, it uses an OS-specific default.
    :return: Path to the cached file.
    """
    if cache_dir is None:
        cache_dir = get_cache_dir()

    # Create cache directory if it doesn't exist
    os.makedirs(cache_dir, exist_ok=True)

    # Use URL hash for filename to avoid conflicts
    filename = hashlib.md5(url.encode("utf-8")).hexdigest()
    cache_path = os.path.join(cache_dir, filename)

    if os.path.exists(cache_path):
        print(f"Using cached file: {cache_path}")
        return cache_path

    # Download the file
    # this module is a bit slow to import (don't unless needed)
    import requests

    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(cache_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    print(f"File downloaded and cached at: {cache_path}")
    return cache_path


def cached(constant_function):
    """Decorator to cache the result of a function that always returns the same object.

    This decorator is designed for functions with no arguments that
    consistently return an identical object, such as Chi2FullCov
    objects in likelihoods.py which can need expansive factorisation
    of large matrices at their creation. It stores the result in a
    file-based cache using pickle serialization, loading from the
    cache if available or computing and saving it otherwise. The cache
    file is named based on the function’s name and stored in a
    directory returned by `get_cache_dir()`.

    Parameters
    ----------
    constant_function : callable
        A function with no arguments that returns a constant object to be cached.
        Typically used for expensive-to-compute objects like Likelihood instances.

    Returns
    -------
    callable
        A wrapped function that returns the cached object if available, or computes,
        caches, and returns it if not.

    Notes
    -----
    - The cache is stored in a file named 'func_cache_<function_name>' within the
      directory specified by `get_cache_dir()`.
    - The decorator assumes `constant_function` is deterministic and side-effect-free.
    - Uses `pickle` for serialization, so the returned object must be picklable.

    Examples
    --------
    >>> @cached
    ... def expensive_likelihood():
    ...     return Chi2FullCov(...)  # Expensive computation
    >>> result = expensive_likelihood()  # Computes and caches
    >>> result2 = expensive_likelihood()  # Loads from cache

    """
    cache_dir = get_cache_dir()

    # Create cache directory if it doesn't exist
    os.makedirs(cache_dir, exist_ok=True)

    cache_path = os.path.join(cache_dir, f"func_cache_{constant_function.__name__}")

    def cached_function():
        if os.path.exists(cache_path):
            print(f"Using cached file: {cache_path}")
            with open(cache_path, "rb") as fid:
                return pickle.load(fid)
        else:
            obj = constant_function()
            with open(cache_path, "wb") as fid:
                pickle.dump(obj, fid)
            return obj

    return cached_function


def safe_vmap(in_axes: Tuple[None | int, ...] = (None, 0)) -> Callable:
    """
    Vectorize a function with JAX's vmap, treating all inputs as arrays.

    Converts scalar inputs to 1D arrays before applying vmap, ensuring 1D array outputs.

    Parameters:
    - in_axes (Tuple[None | int, ...]): Specifies which dimensions of inputs to vectorize.

    Returns:
    - Callable: JIT-compiled, vectorized version of the input function.
    """

    def wrapper(f: Callable) -> Callable:
        @jax.jit
        def vectorized(*args):
            vargs = [
                jnp.atleast_1d(arg) if ax is not None else arg
                for arg, ax in zip(args, in_axes)
            ]
            result = jax.vmap(f, in_axes=in_axes)(*vargs)
            return result

        return vectorized

    return wrapper


def trapezoidal_rule_integration(
    f: Callable, bound_inf: float, bound_sup: float, n_step: int = 1000, *args, **kwargs
) -> float:
    """
    Compute the integral of f over [bound_inf, bound_sup] using the trapezoidal rule.

    Parameters:
    -----------
    f: Callable
        Function to integrate.
    bound_inf, bound_sup: float
        Integration bounds.
    n_step: int
        Number of subdivisions.
    *args, **kwargs:
        Additional arguments passed to f.

    Returns:
    --------
    float: The computed integral.
    """
    x = jnp.linspace(bound_inf, bound_sup, n_step)
    y = f(x, *args, **kwargs)
    h = (bound_sup - bound_inf) / (n_step - 1)
    return (h / 2) * (y[1:] + y[:-1]).sum()


class Constants:
    G = 6.67384e-11  # m^3/kg/s^2
    c = 299792458.0  # m/s
    pc = 3.08567758e16  # m
    mp = 1.67262158e-27  # kg
    h = 6.62617e-34  # J.s
    k = 1.38066e-23  # J/K
    e = 1.60217663e-19  # C
    year = 31557600.0  # s
    sigma = (
        2 * jnp.pi**5 * k**4 / (15 * h**3 * c**2)
    )  # Stefan-Boltzmann constant J/s / K^4 /m^2
    qmax = 30
    nq = 100
    const = 7.0 / 120 * jnp.pi**4
    const2 = 5.0 / 7.0 / jnp.pi**2
    N = 2000
    am_min = 0.01
    am_max = 600.0
    zeta3 = 1.2020569031595942853997
    zeta5 = 1.0369277551433699263313
    neutrino_mass_fac = (
        94.082  # Conversion factor for thermal neutrinos with Neff=3, TCMB=2.7255
    )


def load_csv_from_url(url, delimiter=","):
    """
    Load a CSV file from a URL directly into a NumPy array

    Parameters:
    - url (str): URL of the CSV file to download.
    - delimiter (str): The string used to separate values in the CSV file (default is ',').

    Returns:
    - numpy.ndarray: The loaded CSV data as a NumPy array.
    """
    # Decode the response content and split into lines
    # lines = response.content.decode("utf-8").splitlines()
    path = cached_download(url)
    with open(path, "r") as fid:
        lines = fid.readlines()

    # Process the CSV data
    def convert(value):
        """Attemps to convert values to numerical types"""
        value = value.strip()
        if not value:
            value = "nan"
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                pass
        return value

    header = lines[0].split(delimiter)
    data = [[convert(value) for value in line.split(delimiter)] for line in lines[1:]]

    return np.rec.fromrecords(data, names=header)


def conflevel_to_delta_chi2(level, dof=2, max_iter=1000, tol=1e-6):
    """Return the ΔΧ² value corresponding to a given
    confidence level in percent

    parameter:
    - level: confidence level in percent
    - dof: Number of degrees of freedom of the chi2 law
    - max_iter: maximum number of iteration in the Newton search.
    - tol: The tolerance for the numerical accuracy of the solution.
    Note: for some reason ppf is not available in jax.scipy but cdf
    is, a quick fix was to solve for the root using Newton method.
    """
    x = jnp.array(dof)
    prob = level / 100

    def f(x):
        return jax.scipy.stats.chi2.cdf(x, dof) - prob

    def df(x):
        return jax.scipy.stats.chi2.pdf(x, dof)

    for _ in range(max_iter):
        x_new = x - f(x) / df(x)
        if jnp.abs(x_new - x) < tol:
            return x_new
        x = x_new
    raise ValueError("Newton's method did not converge")


# This global random key at the module level is provided for
# conveniency so that random vector can be obtained with onliners when
# need. This will note ensure actual randomness nor reproducibility.
# To be used cautiously
global_key = None


def randn(sigma, n=None, key=None):
    """
    Generate a Gaussian random vector scaled by sigma.

    Parameters:
    -----------
    sigma : float or array_like
        Standard deviation to scale the random vector. If sigma is an array,
        each element scales the corresponding element of the output vector.
    n : int or tuple, optional
        If provided, specifies the shape of the output. If not provided (None),
        the shape of `sigma` is used.
    key : jax.random.PRNGKey, optional
        PRNG key for random number generation. If not provided, uses the
        global key, which can lead to non-reproducible results.

    Returns:
    --------
    ndarray
        An array of Gaussian random numbers scaled by `sigma`.

    Notes:
    ------
    - Using the global key (`key=None`) can lead to correlated results across
      function calls since the key is updated globally. For reproducibility,
      pass an explicit key.
    - The function splits the key if no key is provided, which might lead
      to issues in parallel computing scenarios due to key reuse.

    Examples:
    ---------
    >>> import jax.numpy as jnp
    >>> randn(1.0, (2, 3))  # 2x3 matrix of random numbers scaled by 1.0
    >>> randn(jnp.array([1, 2, 3]))  # Vector scaled by different sigmas
    """
    global global_key
    if key is None:
        if global_key is None:
            # This global random key at the module level is provided for
            # conveniency so that random vector can be obtained with onliners when
            # need. This will note ensure actual randomness nor reproducibility.
            # To be used cautiously
            global_key = jax.random.PRNGKey(42)
        global_key, subkey = jax.random.split(global_key)
    else:
        subkey = key
    if n is None:
        n = sigma.shape
    gaussian_vector = jax.random.normal(subkey, n)
    return gaussian_vector * sigma


def speed_measurement(func, *args, n=10):
    """Conveniency function to measure execution and jit speed of
    functions in one go

    """
    jax.clear_caches()  # make sure that compilation is triggered
    tstart = time.time()
    result = jax.block_until_ready(func(*args))
    tcomp = time.time()
    for _ in range(n):
        result = jax.block_until_ready(func(*args))
    tstop1 = time.time()
    jax.clear_caches()  # make sure that compilation is triggered
    tstart2 = time.time()
    jfunc = jax.jit(func)
    tjit = time.time()
    result = jax.block_until_ready(jfunc(*args))
    tcomp2 = time.time()
    for _ in range(n):
        result = jax.block_until_ready(jfunc(*args))
    tstop2 = time.time()
    # return (len(z), tcomp-tstart, (tstop-tcomp)/n)
    return (
        tcomp - tstart,
        (tstop1 - tcomp) / n,
        tjit - tstart2,
        tcomp2 - tjit,
        (tstop2 - tcomp2) / n,
    )


def save(grid, filename):
    """Save data dictionary to a pickle file."""
    import pickle

    with open(filename, "wb") as fid:
        pickle.dump(grid, fid)


def load(filename):
    """Load data dictionary from a pickle file."""
    import pickle

    with open(filename, "rb") as fid:
        return pickle.load(fid)

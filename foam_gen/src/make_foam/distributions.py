from scipy.interpolate import interp1d
from scipy import stats
from numpy import linspace, pi, random, sqrt, log, exp, cumsum, diff
from scipy.special import gamma as gamma_func
import matplotlib.pyplot as plt


def plot_pdf_and_histogram(pdf_function, bub_radii, x_vals):
    """
    Plot the PDF as a line and the histogram of the bubble radii.

    Parameters:
        pdf_function (callable): Function to compute the PDF.
        bub_radii (list or numpy array): Generated bubble radii.
        x_vals (numpy array): Range of x values to evaluate the PDF.
    """
    # Evaluate the PDF over the range of x_values
    pdf_values = pdf_function(x_vals)

    # Create a figure and a set of subplots
    fig, ax = plt.subplots()

    # Plot the PDF line
    ax.plot(x_vals, pdf_values, label='PDF', color='blue')

    # Plot the histogram of the bubble radii
    ax.hist(bub_radii, bins=30, density=True, alpha=0.6, color='green', label='Histogram of Radii')

    # Set labels and title
    ax.set_xlabel('Radius')
    ax.set_ylabel('Probability Density')
    ax.set_title('PDF and Histogram of Bubble Radii')

    # Add legend
    ax.legend()

    # Show the plot
    plt.show()


# Calculate the cumulative distribution function (CDF)
def calculate_cdf(pdf, x_values):
    # Compute PDF values at a dense grid of points
    pdf_values = pdf(x_values)
    # Use numerical integration to compute CDF values
    cdf_values = cumsum(pdf_values) * diff(x_values, prepend=0)
    cdf_values /= cdf_values[-1]  # Normalize to [0, 1]
    return cdf_values


def inverse_transform_sampling(pdf, x_values, n_samples):
    cdf_values = calculate_cdf(pdf, x_values)
    inverse_cdf = interp1d(cdf_values, x_values, kind='linear', fill_value='extrapolate')
    u = random.rand(n_samples)
    return inverse_cdf(u)


def get_bubble_radii(dist, cv, mu, n):
    def lognormal(r):
        sigma = sqrt(log(cv ** 2 + 1))
        mu_log = log(mu / sqrt(1 + cv ** 2))  # Adjusted to incorporate mu
        lognormal_dist = stats.lognorm(s=sigma, scale=exp(mu_log))
        return lognormal_dist.pdf(r)

    def gamma(r):
        # Gamma parameters
        alpha = 1 / cv ** 2
        beta = alpha / mu  # To keep mean = 1
        gamma_dist = stats.gamma(a=alpha, scale=1 / beta)
        return gamma_dist.pdf(r)

    def weibull(r):
        from scipy.optimize import fsolve

        # Define equations to solve for kappa and lambda
        def equations(p):
            kappa, lambda_ = p
            mean_eq = lambda_ * gamma_func(1 + 1 / kappa) - mu
            var_eq = lambda_ ** 2 * (gamma_func(1 + 2 / kappa) - gamma_func(1 + 1 / kappa) ** 2) - (cv * mu) ** 2
            return mean_eq, var_eq

        # Initial guesses for kappa and lambda
        kappa_initial = 0.75
        lambda_initial = mu

        # Solve for kappa and lambda
        kappa, lambda_ = fsolve(equations, (kappa_initial, lambda_initial))

        # Create Weibull distribution
        weibull_dist = stats.weibull_min(c=kappa, scale=lambda_)
        return weibull_dist.pdf(r)

    def devries(r):
        return 2.082 * r / (1 + 0.387 * r ** 2) ** 4

    def gal_or(r):
        return (32 / pi ** 2) * r ** 2 * exp(-(4 / pi) * r ** 2)

    def lemlich(r):
        return (16 / pi) * r ** 2 * exp(-sqrt(16 / pi) * r ** 2)

    # Create a dictionary for the functions
    function = {'lognormal': lognormal, 'gamma': gamma, 'weibull': weibull, 'devries': devries, 'gal_or': gal_or,
                'lemlich': lemlich}[dist]
    # We want to know how deep into the tail we want to sample. For really large cvs and mus we need to adjust
    x_values = linspace(max(0, mu - 5 * (mu * cv)), mu + 5 * (mu * cv), n)
    bubble_radii = inverse_transform_sampling(function, x_values, n)

    # By sorting the bubbles they are able to be inserted more quickly into the box
    bubble_radii = sorted(bubble_radii, reverse=True)
    # Return the bubble radii
    return bubble_radii

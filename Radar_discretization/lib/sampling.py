import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm, beta, cauchy


class TruncatedSampler:
    def __init__(self, distribution, params, bounds):
        """
        A class for sampling from a truncated distribution.
        Parameters:
        - distribution (str): Name of the distribution (e.g. 'gaussian', 'beta', 'cauchy')
        - params (dict): Dictionary containing the parameters of the distribution. The keys depend on the distribution.
        - bounds (tuple): Tuple containing the lower and upper bounds of the distribution.
        """
        self.distribution = distribution
        self.params = params
        self.bounds = bounds
        self.a, self.b = bounds
        
        if distribution == "gaussian":
            self.F_a = norm.cdf(self.a, loc=params["mean"], scale=params["std_dev"])
            self.F_b = norm.cdf(self.b, loc=params["mean"], scale=params["std_dev"])
            self.ppf = lambda u: norm.ppf(u, loc=params["mean"], scale=params["std_dev"])
            self.pdf = lambda x: norm.pdf(x, loc=params["mean"], scale=params["std_dev"])
            self.cdf = lambda x: norm.cdf(x, loc=params["mean"], scale=params["std_dev"])
        
        elif distribution == "beta":
            # Transforming Beta Distribution to fit within bounds [a, b]
            self.F_a = beta.cdf(0, params["alpha"], params["beta"])  # CDF at 0 for [0, 1]
            self.F_b = beta.cdf(1, params["alpha"], params["beta"])  # CDF at 1 for [0, 1]
            
            # Scaled PPF
            self.ppf = lambda u: self.a + beta.ppf(u, params["alpha"], params["beta"]) * (self.b - self.a)
            
            # Scaled PDF
            self.pdf = lambda x: beta.pdf((x - self.a) / (self.b - self.a), params["alpha"], params["beta"]) / (self.b - self.a)
            
            # Scaled CDF
            self.cdf = lambda x: beta.cdf((x - self.a) / (self.b - self.a), params["alpha"], params["beta"])
        
        elif distribution == "cauchy":
            self.F_a = cauchy.cdf(self.a, loc=params["loc"], scale=params["scale"])
            self.F_b = cauchy.cdf(self.b, loc=params["loc"], scale=params["scale"])
            self.ppf = lambda u: cauchy.ppf(u, loc=params["loc"], scale=params["scale"])
            self.pdf = lambda x: cauchy.pdf(x, loc=params["loc"], scale=params["scale"])
            self.cdf = lambda x: cauchy.cdf(x, loc=params["loc"], scale=params["scale"])
        
        elif distribution == "uniform":
            self.F_a = 0.0
            self.F_b = 1.0
            self.ppf = lambda u: u * (self.bounds[1] - self.bounds[0]) + self.bounds[0]
            self.pdf = lambda x: np.where((x >= self.bounds[0]) & (x <= self.bounds[1]), 1 / (self.bounds[1] - self.bounds[0]), 0)
            self.cdf = lambda x: (x - self.bounds[0]) / (self.bounds[1] - self.bounds[0])
        
        else:
            raise ValueError(f"Unknown distribution: {distribution}")
    
    def sample(self, size):
        "Generate samples from the truncated distribution. Returns a 1D numpy array of size 'size'."
        u = np.random.uniform(0, 1, size)
        truncated_u = self.F_a + u * (self.F_b - self.F_a)
        return self.ppf(truncated_u)


class MultiDimensionalSampler:
    """
    A class for sampling from multiple dimensions with different distributions and bounds.
    The sampling_configs argument is a dictionary containing the following structure:
    - Key: Dimension name (e.g. 'azimuth', 'elevation', 'range', ...)
    - Value: Dictionary containing the following keys:
        - 'distribution': Name of the distribution (e.g. 'gaussian', 'beta', 'cauchy') (see TruncatedSampler for
                          supported distributions)
        - 'params': Dictionary containing the parameters of the distribution (e.g. 'mean', 'std_dev' for Gaussian)
        - 'bounds': Tuple containing the lower and upper bounds of the distribution (e.g. (-1, 1))
    """
    def __init__(self, sampling_configs):
        self.samplers = {}
        for dim, config in sampling_configs.items():
            self.samplers[dim] = TruncatedSampler(
                distribution=config["distribution"],
                params=config["params"],
                bounds=config["bounds"]
            )
        self.samples = None
    
    def get_samples(self):
        if self.samples is None:
            raise ValueError("No samples have been generated. Call the 'sample' method first.")
        return self.samples
    
    def sample(self, num_samples):
        """Samples from each dimension and returns a 2D array where each column corresponds to a dimension. """
        data = []
        for dim, sampler in self.samplers.items():
            data.append(sampler.sample(num_samples))
        # Creates 2D array using 1D arrays in 'data' as columns
        self.samples = np.column_stack(data)
    
    def visualize_sampling(self, **num_samples):
        """
        Create a matplotlib figure with subplots showing the PDF, CDF, and sampled points
        for each dimension.
        
        Args:
            num_samples (int): Number of samples to generate for visualization.
        """
        if self.samples is None:    # If samples have not been generated, generate them
            self.sample(num_samples)
        
        fig, axes = plt.subplots(1, len(self.samplers), figsize=(18, 6), constrained_layout=True)
        
        dim_index = np.linspace(0, len(self.samplers) - 1, len(self.samplers)).astype(int) # Is used only to index

        for ax, (dim, sampler), index in zip(axes, self.samplers.items(), dim_index):
            samples = self.samples[:, index]
            x = np.linspace(sampler.a, sampler.b, 500)
            
            # Plot PDF
            ax.plot(x, sampler.pdf(x), label="PDF", color="blue", alpha=0.7)
            
            # Create a second y-axis for the CDF
            ax2 = ax.twinx()
            ax2.plot(x, sampler.cdf(x), label="CDF", color="green", alpha=0.7)
            ax2.set_ylabel("CDF", color="green")
            ax2.tick_params(axis='y', labelcolor='green')
            ax2.set_ylim(0, 1)
            
            # Plot histogram of samples on the primary y-axis
            ax.hist(samples, bins=30, density=True, color="red", alpha=0.2, label="Samples")
            
            # Add labels and legend
            ax.set_title(f"{dim.capitalize()} Sampling ({sampler.distribution})", fontsize=14)
            ax.set_xlabel("Value")
            ax.set_ylabel("Density")
            ax.legend(loc="upper left")
            ax2.legend(loc="upper right")
        
        # Vertical grid lines
        for ax in axes:
            ax.grid(True, which='both', axis='x', linestyle='--', linewidth=0.5)
        
        plt.suptitle("Sampling Visualization", fontsize=16)
        plt.show()

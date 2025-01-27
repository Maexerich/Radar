import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm, beta, cauchy


class TruncatedSampler:
    def __init__(self, distribution, params, bounds):
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
            self.F_a = beta.cdf(self.a, params["alpha"], params["beta"])
            self.F_b = beta.cdf(self.b, params["alpha"], params["beta"])
            self.ppf = lambda u: beta.ppf(u, params["alpha"], params["beta"])
            self.pdf = lambda x: beta.pdf(x, params["alpha"], params["beta"])
            self.cdf = lambda x: beta.cdf(x, params["alpha"], params["beta"])
        
        elif distribution == "cauchy":
            self.F_a = cauchy.cdf(self.a, loc=params["loc"], scale=params["scale"])
            self.F_b = cauchy.cdf(self.b, loc=params["loc"], scale=params["scale"])
            self.ppf = lambda u: cauchy.ppf(u, loc=params["loc"], scale=params["scale"])
            self.pdf = lambda x: cauchy.pdf(x, loc=params["loc"], scale=params["scale"])
            self.cdf = lambda x: cauchy.cdf(x, loc=params["loc"], scale=params["scale"])
        
        else:
            raise ValueError(f"Unknown distribution: {distribution}")
    
    def sample(self, size):
        u = np.random.uniform(0, 1, size)
        truncated_u = self.F_a + u * (self.F_b - self.F_a)
        return self.ppf(truncated_u)


class MultiDimensionalSampler:
    def __init__(self, sampling_configs):
        self.samplers = {}
        for dim, config in sampling_configs.items():
            self.samplers[dim] = TruncatedSampler(
                distribution=config["distribution"],
                params=config["params"],
                bounds=config["bounds"]
            )
    
    def sample(self, num_samples):
        data = []
        for dim, sampler in self.samplers.items():
            data.append(sampler.sample(num_samples))
        return np.column_stack(data)
    
    def visualize_sampling(self, num_samples):
        """
        Create a matplotlib figure with subplots showing the PDF, CDF, and sampled points
        for each dimension.
        
        Args:
            num_samples (int): Number of samples to generate for visualization.
        """
        fig, axes = plt.subplots(1, len(self.samplers), figsize=(18, 6), constrained_layout=True)
        
        for ax, (dim, sampler) in zip(axes, self.samplers.items()):
            samples = sampler.sample(num_samples)
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
            ax.set_title(f"{dim.capitalize()} Sampling", fontsize=14)
            ax.set_xlabel("Value")
            ax.set_ylabel("Density")
            ax.legend(loc="upper left")
            ax2.legend(loc="upper right")
        
        plt.suptitle("Sampling Visualization", fontsize=16)
        plt.show()

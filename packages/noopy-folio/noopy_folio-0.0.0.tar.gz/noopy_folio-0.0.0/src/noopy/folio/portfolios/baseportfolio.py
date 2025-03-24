import abc
import numpy as np
from scipy.stats import norm


class BasePortfolio(abc.ABC):
    """Abstract class that can be inherited by any concrete portfolio model in theory:

    Args:
        ABC (ABC): force abstract class nature
    """
    def __init__(self):
        """Constructor that initialise some protected member variables
        """
        # portfolio attributes
        self._covariances = None
        self._returns = None
        self._weights = None

        # calculated
        self._variance = None

    # @abc.abstractclassmethod # disable such restriction for now
    def get_covariances(self, **kwargs):
        """Base method to get covariance matrix for the portfolio:

        Returns:
            **kwargs: actual parameters might differ in concrete portfolio classes
        """
        return self._covariances

    def get_weights(self, **kwargs):
        """Base method to get weights for the portfolio:

        Returns:
            **kwargs: actual parameters might differ in concrete portfolio classes
        """
        return self._weights

    def get_returns(self, **kwargs):
        """Base method to get returns for the portfolio:

        Returns:
            **kwargs: actual parameters might differ in concrete portfolio classes
        """
        return self._returns

    def get_variance(self):
        """Get variance for the portfolio
        """
        if self._variance is None:
            if self._covariances is None:
                raise ValueError(
                    'Portfolio attribute [covariance] is not set yet.')
            weights = self.get_weights()
            self._variance = (weights.T @ self._covariances @ weights)[0][0]
        return self._variance

    def get_stddev(self):
        """Get standard deviation for the portfolio
        """
        return np.sqrt(self.get_variance())

    def get_valueatrisk(self, confidence):
        """Get VaR for the portfolio
        """
        weights = self.get_weights()
        c = norm.ppf(confidence)
        return (self._returns.T @ weights - c * self.get_stddev())[0][0]

    def get_expectedshortfall(self, confidence):
        """Get ES for the portfolio
        """
        weights = self.get_weights()
        c = norm.pdf(norm.ppf(confidence)) / (1.0 - confidence)
        return (self._returns.T @ weights - c * self.get_stddev())[0][0]

    def get_riskcontribution(self, by='volatility',
                             confidence=None, returnpercentage=True):
        """Get risk contributions from each asset in the portfolio
        """
        weights = self.get_weights()
        sig_weights = self._covariances @ weights
        marginal_risk = sig_weights / np.sqrt(weights.T @ sig_weights)[0][0]

        if by == 'var':
            c = norm.ppf(confidence)
            marginal_risk = self._returns - c * marginal_risk
        elif by == 'es':
            c = norm.pdf(norm.ppf(confidence)) / (1.0 - confidence)
            marginal_risk = self._returns - c * marginal_risk
        elif by != 'volatility':
            raise ValueError(f'risk measure [{by}] is not recognized.')
        rc = weights * marginal_risk

        return rc / np.sum(rc) if returnpercentage else rc

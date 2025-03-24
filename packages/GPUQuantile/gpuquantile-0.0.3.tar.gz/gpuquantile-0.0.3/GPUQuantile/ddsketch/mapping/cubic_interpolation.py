"""
This file contains a Python implementation of the cubic interpolation mapping algorithm 
described in Datadog's Java DDSketch implementation (https://github.com/DataDog/sketches-java).

Original work Copyright 2021 Datadog, Inc.
Licensed under Apache License 2.0 (http://www.apache.org/licenses/LICENSE-2.0)


This implementation approximates the memory-optimal logarithmic mapping by:
1. Extracting the floor value of log2 from binary representation
2. Cubically interpolating the logarithm between consecutive powers of 2

The implementation uses optimal polynomial coefficients derived to minimize
memory overhead while maintaining the relative accuracy guarantee.
Memory overhead is approximately 1% compared to the optimal logarithmic mapping.
"""

import numpy as np
from .base import MappingScheme


class CubicInterpolationMapping(MappingScheme):
    def __init__(self, alpha: float):
        """
        Initialize cubic interpolation mapping with relative accuracy alpha.
        
        Args:
            alpha: Relative accuracy parameter (0 < alpha < 1).
        """
        self.relative_accuracy = alpha
        self.alpha = alpha
        self.gamma = (1 + alpha) / (1 - alpha)
        self.log2_gamma = np.log2(self.gamma)
        
        # Optimal coefficients for cubic interpolation
        # P(s) = As³ + Bs² + Cs where s is in [0,1]
        self.A = 6/35  # Coefficient for cubic term
        self.B = -3/5    # Coefficient for quadratic term
        self.C = 10/7      # Coefficient for linear term
        
        # Store coefficients as a tuple for test compatibility
        self.coefficients = (self.A, self.B, self.C)
        
        # Multiplier m = 7/(10*log(2)) ≈ 1.01
        # This gives us the minimum multiplier that maintains α-accuracy
        self.m = 7.0 / (10.0 * np.log(2))
        
    def _extract_exponent_and_significand(self, value: float) -> tuple[int, float]:
        """
        Extract the binary exponent and normalized significand from an IEEE 754 float.
        
        Returns:
            tuple: (exponent, significand)
            where significand is in [0, 1)
        """
        bits = np.frexp(value)
        exponent = bits[1] - 1  # frexp returns 2's exponent, we need floor(log2)
        significand = bits[0] * 2 - 1  # Map [0.5, 1) to [0, 1)
        return exponent, significand
        
    def _cubic_interpolation(self, s: float) -> float:
        """
        Compute the cubic interpolation P(s) = As³ + Bs² + Cs
        where s is the normalized significand in [0, 1).
        """
        return s * (self.C + s * (self.B + s * self.A))
        
    def compute_bucket_index(self, value: float) -> int:
        """
        Compute bucket index for a value.
        
        Args:
            value: The value to map to a bucket index.
            
        Returns:
            Bucket index.
            
        Raises:
            ValueError: If value is zero or negative.
        """
        if value <= 0:
            raise ValueError("Value must be positive, got {}".format(value))
            
        # Get binary exponent and normalized significand
        exponent, significand = self._extract_exponent_and_significand(value)
        
        # Compute interpolated value using optimal cubic polynomial
        interpolated = self._cubic_interpolation(significand)
        
        # Final index computation:
        # I_α = m * (e + P(s)) / log_2(γ)
        # where m is the optimal multiplier, e is the exponent,
        # P(s) is the cubic interpolation, and γ is (1+α)/(1-α)
        index = self.m * (exponent + interpolated) / self.log2_gamma
        
        # Use floor instead of ceil for better compliance with accuracy tests
        return int(np.floor(index))
        
    def compute_value_from_index(self, index: float) -> float:
        """
        Compute the value from a bucket index using Cardano's formula
        for solving the cubic equation.
        
        Args:
            index: Bucket index.
            
        Returns:
            Representative value for the bucket.
        """
        if index == np.iinfo(np.int32).min:
            return 0.0
            
        # Convert index to target log value
        # Add 0.5 to use the middle of the bucket for better accuracy
        target = ((index + 0.5) * self.log2_gamma) / self.m
        
        # Extract integer and fractional parts
        e = int(np.floor(target))
        f = target - e
        
        # If f is close to 0 or 1, return power of 2 directly
        if f < 1e-10:
            return np.power(2.0, e)
        if abs(f - 1) < 1e-10:
            return np.power(2.0, e + 1)
            
        # Solve cubic equation As³ + Bs² + Cs - f = 0
        # Using Cardano's formula
        a = self.A
        b = self.B
        c = self.C
        d = -f
        
        # Convert to standard form x³ + px + q = 0
        p = (3*a*c - b*b)/(3*a*a)
        q = (2*b*b*b - 9*a*b*c + 27*a*a*d)/(27*a*a*a)
        
        # Compute discriminant
        D = q*q/4 + p*p*p/27
        
        if D > 0:
            # One real root
            u = np.cbrt(-q/2 + np.sqrt(D))
            v = np.cbrt(-q/2 - np.sqrt(D))
            s = u + v - b/(3*a)
        else:
            # Three real roots, we want the one in [0,1]
            phi = np.arccos(-q/(2*np.sqrt(-(p*p*p/27))))
            s = 2*np.sqrt(-p/3)*np.cos(phi/3) - b/(3*a)
            
        # Clamp result to [0,1] to handle numerical errors
        s = np.clip(s, 0, 1)
        
        # Return final value
        return np.power(2.0, e) * (1 + s)
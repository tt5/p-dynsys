#!/usr/bin/env python3
"""
Core simulation module containing mathematical functions
Similar to the core Hopf normal form logic from n1.lua
"""

import numpy as np
from typing import Dict, Tuple, Any


class HopfNormalForm:
    """
    Core Hopf normal form implementation
    Based on the mathematical formulation from n1.lua
    """
    
    def __init__(self, mu: float = 0.1, omega: float = 1.0, 
                 alpha: float = -1.0, beta: float = 1.0, dt: float = 0.01):
        self.mu = mu          # bifurcation parameter
        self.omega = omega    # frequency of oscillations
        self.alpha = alpha    # negative for stable limit cycle
        self.beta = beta      # frequency shift with amplitude
        self.dt = dt          # time step
    
    def step(self, x: float, y: float) -> Tuple[float, float]:
        """
        Perform one step of Hopf normal form integration
        Returns updated (x, y) values
        """
        # Hopf normal form equations
        dx_dt = self.mu * x - self.omega * y + self.alpha * x * (x**2 + y**2)
        dy_dt = self.mu * y + self.omega * x + self.beta * y * (x**2 + y**2)
        
        # Euler integration
        x_new = x + dx_dt * self.dt
        y_new = y + dy_dt * self.dt
        
        return x_new, y_new
    
    def get_derivatives(self, x: float, y: float) -> Tuple[float, float]:
        """Get current derivatives without updating state"""
        dx_dt = self.mu * x - self.omega * y + self.alpha * x * (x**2 + y**2)
        dy_dt = self.mu * y + self.omega * x + self.beta * y * (x**2 + y**2)
        return dx_dt, dy_dt
    
    def get_polar_coords(self, x: float, y: float) -> Tuple[float, float]:
        """Convert to polar coordinates"""
        r = np.sqrt(x**2 + y**2)
        theta = np.arctan2(y, x)
        return r, theta
    
    def update_params(self, **kwargs):
        """Update simulation parameters"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def get_params(self) -> Dict[str, float]:
        """Get current parameters"""
        return {
            'mu': self.mu,
            'omega': self.omega,
            'alpha': self.alpha,
            'beta': self.beta,
            'dt': self.dt
        }


class PredatorPreyModel:
    """
    Core Lotka-Volterra predator-prey implementation
    Based on the mathematical formulation from n1-predprey.lua
    """
    
    def __init__(self, alpha: float = 1.1, beta: float = 0.4, 
                 delta: float = 0.1, gamma: float = 0.4, dt: float = 0.1):
        self.alpha = alpha    # prey growth rate
        self.beta = beta     # predation rate
        self.delta = delta    # predator efficiency
        self.gamma = gamma    # predator death rate
        self.dt = dt         # time step
    
    def step(self, x: float, y: float) -> Tuple[float, float]:
        """
        Perform one step of Lotka-Volterra integration
        Returns updated (prey, predator) values
        """
        # Lotka-Volterra equations
        dx_dt = self.alpha * x - self.beta * x * y
        dy_dt = self.delta * x * y - self.gamma * y
        
        # Euler integration
        x_new = x + dx_dt * self.dt
        y_new = y + dy_dt * self.dt
        
        return x_new, y_new
    
    def get_derivatives(self, x: float, y: float) -> Tuple[float, float]:
        """Get current derivatives without updating state"""
        dx_dt = self.alpha * x - self.beta * x * y
        dy_dt = self.delta * x * y - self.gamma * y
        return dx_dt, dy_dt
    
    def update_params(self, **kwargs):
        """Update simulation parameters"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def get_params(self) -> Dict[str, float]:
        """Get current parameters"""
        return {
            'alpha': self.alpha,
            'beta': self.beta,
            'delta': self.delta,
            'gamma': self.gamma,
            'dt': self.dt
        }

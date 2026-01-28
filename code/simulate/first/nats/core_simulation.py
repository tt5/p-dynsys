#!/usr/bin/env python3
"""
Core simulation module containing mathematical functions
Similar to the core Hopf normal form logic from n1.lua
"""

import numpy as np
from typing import Dict, Tuple, Any, Callable


class HopfNormalForm:
    """
    Core Hopf normal form implementation
    Based on the mathematical formulation from n1.lua
    """
    
    def __init__(self, mu: float = 0.1, omega: float = 1.0, 
                 alpha: float = -1.0, beta: float = 1.0, dt: float = 0.01,
                 integration_method: str = 'rk4'):
        self.mu = mu          # bifurcation parameter
        self.omega = omega    # frequency of oscillations
        self.alpha = alpha    # negative for stable limit cycle
        self.beta = beta      # frequency shift with amplitude
        self.dt = dt          # time step
        self.integration_method = integration_method
        
        # Setup integration method
        if integration_method == 'rk4':
            self._integrate = self._rk4_step
        elif integration_method == 'rk2':
            self._integrate = self._rk2_step
        else:
            self._integrate = self._euler_step
    
    def step(self, x: float, y: float) -> Tuple[float, float]:
        """
        Perform one step of Hopf normal form integration
        Returns updated (x, y) values
        """
        # Check for numerical stability
        if abs(x) > 1e6 or abs(y) > 1e6:
            raise ValueError(f"Numerical overflow: x={x}, y={y}")
        
        return self._integrate(x, y)
    
    def get_derivatives(self, x: float, y: float) -> Tuple[float, float]:
        """Get current derivatives without updating state"""
        dx_dt = self.mu * x - self.omega * y + self.alpha * x * (x**2 + y**2)
        dy_dt = self.mu * y + self.omega * x + self.beta * y * (x**2 + y**2)
        return dx_dt, dy_dt
    
    def _euler_step(self, x: float, y: float) -> Tuple[float, float]:
        """Euler integration method"""
        dx_dt, dy_dt = self.get_derivatives(x, y)
        return x + dx_dt * self.dt, y + dy_dt * self.dt
    
    def _rk2_step(self, x: float, y: float) -> Tuple[float, float]:
        """2nd order Runge-Kutta (midpoint method)"""
        dx_dt1, dy_dt1 = self.get_derivatives(x, y)
        x_mid = x + 0.5 * self.dt * dx_dt1
        y_mid = y + 0.5 * self.dt * dy_dt1
        
        dx_dt2, dy_dt2 = self.get_derivatives(x_mid, y_mid)
        return x + self.dt * dx_dt2, y + self.dt * dy_dt2
    
    def _rk4_step(self, x: float, y: float) -> Tuple[float, float]:
        """4th order Runge-Kutta integration method"""
        # k1
        dx_dt1, dy_dt1 = self.get_derivatives(x, y)
        k1_x, k1_y = self.dt * dx_dt1, self.dt * dy_dt1
        
        # k2
        x2, y2 = x + 0.5 * k1_x, y + 0.5 * k1_y
        dx_dt2, dy_dt2 = self.get_derivatives(x2, y2)
        k2_x, k2_y = self.dt * dx_dt2, self.dt * dy_dt2
        
        # k3
        x3, y3 = x + 0.5 * k2_x, y + 0.5 * k2_y
        dx_dt3, dy_dt3 = self.get_derivatives(x3, y3)
        k3_x, k3_y = self.dt * dx_dt3, self.dt * dy_dt3
        
        # k4
        x4, y4 = x + k3_x, y + k3_y
        dx_dt4, dy_dt4 = self.get_derivatives(x4, y4)
        k4_x, k4_y = self.dt * dx_dt4, self.dt * dy_dt4
        
        # Combine
        x_new = x + (k1_x + 2*k2_x + 2*k3_x + k4_x) / 6
        y_new = y + (k1_y + 2*k2_y + 2*k3_y + k4_y) / 6
        
        return x_new, y_new
    
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
    
    def get_params(self) -> Dict[str, Any]:
        """Get current parameters"""
        return {
            'mu': self.mu,
            'omega': self.omega,
            'alpha': self.alpha,
            'beta': self.beta,
            'dt': self.dt,
            'integration_method': self.integration_method
        }


class PredatorPreyModel:
    """
    Core Lotka-Volterra predator-prey implementation
    Based on the mathematical formulation from n1-predprey.lua
    """
    
    def __init__(self, alpha: float = 1.1, beta: float = 0.4, 
                 delta: float = 0.1, gamma: float = 0.4, dt: float = 0.1,
                 integration_method: str = 'rk4'):
        self.alpha = alpha    # prey growth rate
        self.beta = beta     # predation rate
        self.delta = delta    # predator efficiency
        self.gamma = gamma    # predator death rate
        self.dt = dt         # time step
        self.integration_method = integration_method
        
        # Setup integration method
        if integration_method == 'rk4':
            self._integrate = self._rk4_step
        elif integration_method == 'rk2':
            self._integrate = self._rk2_step
        else:
            self._integrate = self._euler_step
    
    def step(self, x: float, y: float) -> Tuple[float, float]:
        """
        Perform one step of Lotka-Volterra integration
        Returns updated (prey, predator) values
        """
        return self._integrate(x, y)
    
    def get_derivatives(self, x: float, y: float) -> Tuple[float, float]:
        """Get current derivatives without updating state"""
        dx_dt = self.alpha * x - self.beta * x * y
        dy_dt = self.delta * x * y - self.gamma * y
        return dx_dt, dy_dt
    
    def _euler_step(self, x: float, y: float) -> Tuple[float, float]:
        """Euler integration method"""
        dx_dt, dy_dt = self.get_derivatives(x, y)
        return x + dx_dt * self.dt, y + dy_dt * self.dt
    
    def _rk2_step(self, x: float, y: float) -> Tuple[float, float]:
        """2nd order Runge-Kutta (midpoint method)"""
        dx_dt1, dy_dt1 = self.get_derivatives(x, y)
        x_mid = x + 0.5 * self.dt * dx_dt1
        y_mid = y + 0.5 * self.dt * dy_dt1
        
        dx_dt2, dy_dt2 = self.get_derivatives(x_mid, y_mid)
        return x + self.dt * dx_dt2, y + self.dt * dy_dt2
    
    def _rk4_step(self, x: float, y: float) -> Tuple[float, float]:
        """4th order Runge-Kutta integration method"""
        # k1
        dx_dt1, dy_dt1 = self.get_derivatives(x, y)
        k1_x, k1_y = self.dt * dx_dt1, self.dt * dy_dt1
        
        # k2
        x2, y2 = x + 0.5 * k1_x, y + 0.5 * k1_y
        dx_dt2, dy_dt2 = self.get_derivatives(x2, y2)
        k2_x, k2_y = self.dt * dx_dt2, self.dt * dy_dt2
        
        # k3
        x3, y3 = x + 0.5 * k2_x, y + 0.5 * k2_y
        dx_dt3, dy_dt3 = self.get_derivatives(x3, y3)
        k3_x, k3_y = self.dt * dx_dt3, self.dt * dy_dt3
        
        # k4
        x4, y4 = x + k3_x, y + k3_y
        dx_dt4, dy_dt4 = self.get_derivatives(x4, y4)
        k4_x, k4_y = self.dt * dx_dt4, self.dt * dy_dt4
        
        # Combine
        x_new = x + (k1_x + 2*k2_x + 2*k3_x + k4_x) / 6
        y_new = y + (k1_y + 2*k2_y + 2*k3_y + k4_y) / 6
        
        return x_new, y_new
    
    def update_params(self, **kwargs):
        """Update simulation parameters"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def get_params(self) -> Dict[str, Any]:
        """Get current parameters"""
        return {
            'alpha': self.alpha,
            'beta': self.beta,
            'delta': self.delta,
            'gamma': self.gamma,
            'dt': self.dt,
            'integration_method': self.integration_method
        }

from collections import OrderedDict

import numpy as np
from numba import boolean, float64, int64
from numba.experimental import jitclass

solver_spec = OrderedDict()
solver_spec["domX"] = float64  # dimensionless domain length in x
solver_spec["domY"] = float64  # dimensionless domain length in y
solver_spec["minN_log2"] = int64  # log2 minimum number of Chebyshev points
solver_spec["minN"] = int64  # minimum number of Chebyshev points
solver_spec["maxN_log2"] = int64  # log2 maximum number of Chebyshev points
solver_spec["maxN"] = int64  # maximum number of Chebyshev points
solver_spec["Nx_log2"] = int64  # log2 of number of points in x
solver_spec["Nx"] = int64  # number of points in x
solver_spec["Ny_log2"] = int64  # log2 of number of points in y
solver_spec["Ny"] = int64  # number of points in y
solver_spec["chebIts"] = int64  # number of chebyshev iterates
solver_spec["epsilon"] = float64  # tolerance for converged spectral series
solver_spec["meps"] = float64  # Machine epsilon
solver_spec["rtol"] = float64  # tolerance for Runge-Kutta integration
solver_spec["maxStep"] = float64  # max step for Runge-Kutta integration
solver_spec["rk"] = boolean # use rk solver


@jitclass(solver_spec)
class SolverParameters:
    def __init__(
        self,
        domX=1.5,
        domY=1.5,
        minN_log2=4,
        maxN_log2=8,
        Nx_log2=8,
        Ny_log2=8,
        epsilon=1e-8,
        rtol=1e-8,
        maxStep=0.01,
        rk=False
    ):
        self.meps = np.finfo(np.float64).eps

        if domX < 0:
            raise ValueError("In SolverParameters, must have domX>0")
        self.domX = np.float64(domX)  # Dimensionless domain size in x

        if domY < 0:
            raise ValueError("In SolverParameters, must have domY>0")
        self.domY = np.float64(domY)  # Dimensionless domain size in y

        if minN_log2 < 0:
            raise ValueError("In SolverParameters, must have minN_log2>0")
        self.minN_log2 = np.int64(minN_log2)  # Minimum z-resolution (log2)
        self.minN = 2**self.minN_log2

        if maxN_log2 < 0:
            raise ValueError("In SolverParameters, must have maxN_log2>0")
        self.maxN_log2 = np.int64(maxN_log2)  # Maximum z-resolution (log2)
        self.maxN = 2**self.maxN_log2

        if minN_log2 > maxN_log2:
            raise ValueError("In SolverParameters, must have minN_log2 < maxN_log2")

        if Nx_log2 < 0:
            raise ValueError("In SolverParameters, must have Nx_log2>0")
        self.Nx_log2 = np.int64(Nx_log2)  # x-resolution (log2)
        self.Nx = 2**self.Nx_log2

        if Ny_log2 < 0:
            raise ValueError("In SolverParameters, must have Ny_log2>0")
        self.Ny_log2 = np.int64(Ny_log2)  # y-resolution (log2)
        self.Ny = 2**self.Ny_log2

        self.chebIts = self.maxN_log2 - self.minN_log2 + 1

        if epsilon < 0:
            raise ValueError("In SolverParameters, must have epsilon>0")
        if epsilon < 10 * self.meps:
            raise ValueError(
                "In SolverParameters, " + "must have epsilon >= 10*machine epsilon"
            )
        self.epsilon = np.float64(epsilon)

        if rtol < 0:
            raise ValueError("In SolverParameters, must have rtol>0")
        self.rtol = np.float64(rtol)  # tolerance for Runge-Kutta integration

        if maxStep <= 0:
            raise ValueError("In SolverParameters, must have maxStep>0")
        if maxStep >= 1:
            raise ValueError("In SolverParameters, must have maxStep<1")
        self.maxStep = np.float64(maxStep)  # max step for Runge-Kutta integration

        if rk:
            self.rk = True
        else:
            self.rk = False

    def describe(self):
        print("Solver parameters for AshDisperse")
        print("  Dimensionless domain size in x, domX = ", self.domX)
        print("  Dimensionless domain size in y, domY = ", self.domY)
        print(
            "  Minimum resolution in z, minN = ",
            self.minN,
            " (minN_log2 = ",
            self.minN_log2,
            ")",
        )
        print(
            "  Maximum resolution in z, maxN = ",
            self.maxN,
            " (maxN_log2 = ",
            self.maxN_log2,
            ")",
        )
        print("  Number of Chebyshev iterates = ", self.chebIts)
        print("  Tolerance for Chebyshev series, epsilon = ", self.epsilon)
        print("  Resolution in x, Nx = ", self.Nx, " (Nx_log2 = ", self.Nx_log2, ")")
        print("  Resolution in y, Ny = ", self.Ny, " (Ny_log2 = ", self.Ny_log2, ")")
        print("********************")


# pylint: disable=E1101
SolverParameters_type = SolverParameters.class_type.instance_type

def _solver_dict(p):
    return {
        'domX': float(p.domX),
        'domY': float(p.domY),
        'minN_log2': int(p.minN_log2),
        'maxN_log2': int(p.maxN_log2),
        'Nx_log2': int(p.Nx_log2),
        'Ny_log2': int(p.Ny_log2),
        'epsilon': float(p.epsilon),
        'rtol': float(p.rtol),
        'maxStep': float(p.maxStep),
    }
import numpy as np
import plotext as plt
import pytest

from example import rk4


def test_steepwell():
    tmax = 10
    nstep = 1000
    num_sol = rk4.solve(
        lambda t, y: -np.sinh(y),  # noqa: ARG005
        0,
        tmax,
        -1,
        0,
        nstep,
    )

    energy = num_sol[:, 2] ** 2 / 2 + np.cosh(num_sol[:, 1])

    # compare global error

    plt.theme("matrix")
    plt.frame(0)
    plt.plot(num_sol[:, 0], energy, label="energy (RK4)")
    plt.show()
    plt.clf()

    for i, t in enumerate(num_sol[:, 0]):
        assert energy[i] == pytest.approx(energy[0], rel=1e-5), (
            f"Energy left tolerance at t = {t}."
        )

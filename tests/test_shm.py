import numpy as np
import plotext as plt
import pytest

from example import rk4


@pytest.fixture(params=[1, 2, 4])
def hooke_constant(request):
    return request.param


def test_rk4(hooke_constant):
    tmax = 10
    nstep = 1000
    num_sol = rk4.solve(
        lambda t, y: -hooke_constant * y,  # noqa: ARG005
        0,
        tmax,
        -1,
        0,
        nstep,
    )

    # compare global error
    w = np.sqrt(hooke_constant)
    tru_sol = -np.cos(w * num_sol[:, 0])

    plt.theme("matrix")
    plt.frame(0)
    plt.plot(num_sol[:, 0], num_sol[:, 1], label="rk4")
    plt.plot(num_sol[:, 0], tru_sol[:], label="true")
    plt.show()
    plt.clf()

    np.testing.assert_allclose(num_sol[:, 1], tru_sol, rtol=1e-3, atol=1e-3)

    dt = tmax / nstep
    # --- compare local truncation error ---
    # error from true solution with start at previous step)
    # y(t+dt) =[exact]= y(t) * cos(w * dt) + (y'(t)/w) * sin(w * dt)
    # y'(t+dt) =[exact]= -y(t) * w * sin(w * dt) + y'(t) * cos(w * dt)
    tru_shft_cos = np.cos(w * dt)
    tru_shft_sin = np.sin(w * dt)

    # y
    np.testing.assert_allclose(
        num_sol[1:, 1],
        tru_shft_cos * num_sol[:-1, 1] + (tru_shft_sin / w) * num_sol[:-1, 2],
        rtol=1e-5,
        atol=1e-5,
    )
    # y'
    np.testing.assert_allclose(
        num_sol[1:, 2],
        -(tru_shft_sin * w) * num_sol[:-1, 1] + tru_shft_cos * num_sol[:-1, 2],
        rtol=1e-5,
        atol=1e-5,
    )

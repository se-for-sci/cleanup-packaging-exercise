from collections.abc import Sequence

import numpy as np

from example import rk4


def trial(
    N: int = 10000,
    hooke_constant: float = 4,
    dt_prev: float | None = None,
    errs_prev: Sequence[float] | None = None,
) -> tuple[float, float, float, float]:
    """Runs a trial for the known solution y'' + ky = 0

    Args:
        N (int, optional): Number of steps. Defaults to 10000.
        hooke_constant (float, optional): Spring constant k. Defaults to 4.
        dt_prev (float | None, optional): dt value of the trial to compare against.
            Defaults to None.
        errs_prev (Sequence[float] | None, optional): errors of the trial to compare against.
            This should have 3 values: [global_error, LTE (y), LTE (y')]. Defaults to None.

    Returns:
        tuple[float,float,float,float]: The step size dt of this trial, followed by the
            errors [global_error, LTE (y), LTE (y')].
    """
    tmax = 10
    nstep = N
    num_sol = rk4.solve(
        lambda t, y: -hooke_constant * y,  # noqa: ARG005
        0,
        tmax,
        1,
        0,
        nstep,
    )

    # compare global error
    w = np.sqrt(hooke_constant)  # angular frequency
    tru_sol = np.cos(w * num_sol[:, 0])

    glob_err = np.max(np.abs(num_sol[:, 1] - tru_sol))

    dt = tmax / nstep
    # --- compare local truncation error (LTE) ---
    # error from true solution with start at previous step)
    # y(t+dt) =[exact]= y(t) * cos(w * dt) + (y'(t)/w) * sin(w * dt)
    # y'(t+dt) =[exact]= -y(t) * w * sin(w * dt) + y'(t) * cos(w * dt)

    tru_shft_cos = np.cos(w * dt)
    tru_shft_sin = np.sin(w * dt)
    lte_y = np.max(
        np.abs(
            num_sol[1:, 1]
            - tru_shft_cos * num_sol[:-1, 1]
            - tru_shft_sin / w * num_sol[:-1, 2]
        )
    )
    lte_yp = np.max(
        np.abs(
            num_sol[1:, 2]
            + tru_shft_sin * w * num_sol[:-1, 1]
            - tru_shft_cos * num_sol[:-1, 2]
        )
    )

    # print out ratio against prev
    if dt_prev is not None and errs_prev is not None:
        dt_cmp_str = f"(÷{dt_prev / dt:.2f})"
        ge_cmp_str = f"(÷{errs_prev[0] / glob_err:.2f})"
        lte_y_cmp_str = f"(÷{errs_prev[1] / lte_y:.2f})"
        lte_yp_cmp_str = f"(÷{errs_prev[2] / lte_yp:.2f})"
    else:
        dt_cmp_str = ""
        ge_cmp_str = ""
        lte_y_cmp_str = ""
        lte_yp_cmp_str = ""

    print(
        f"{dt:8.1e} {dt_cmp_str:8s} | {glob_err:8.1e} {ge_cmp_str:8s} | {lte_y:8.1e} {lte_y_cmp_str:8s} | {lte_yp:8.1e} {lte_yp_cmp_str:8s}"
    )
    return dt, glob_err, lte_y, lte_yp


if __name__ == "__main__":
    N0 = 10
    print("  time step size  |  max global error |    max LTE (y)   |    max LTE (y') ")
    dt, *errs = trial(N0)
    for i in range(1, 10):
        dt, *errs = trial(N0 * 2**i, dt_prev=dt, errs_prev=errs)
    print(" " * 50 + "(÷ factor of previous row)")

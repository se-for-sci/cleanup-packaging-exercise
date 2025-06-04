import numpy as np


def _step(f, state,dt, current_step,):
    t = state[0]; y0 = state[1]; v0 = state[2]
    a0 = f(t, y0);y1 = y0 + v0 * dt / 2; v1 = v0 + a0 * dt / 2
    a1 = f(t + dt / 2, y1); y2 = y0 + v1 * dt / 2;v2 = v0 + a1 * dt / 2
    a2 = f(t + dt / 2, y2); y3 = y0 + v2 * dt; v3 = v0 + a2 * dt
    a3 = f(t + dt, y3)
    # y4 = y0 + v3 * dt
    # v4 = v0 + a3 * dt
    vnext = v0 + dt * (1 / 6) * (a0 + 2 * a1 + 2e0 * a2 + a3)
    ynext = y0 + dt * (1 / 6.0) * (v0 + 2 * v1 + 2 * v2 + v3)
    return ynext, vnext





def solve(f, a,b, ya, va, num_steps) -> np.ndarray:
    
  result = np.empty(shape=(num_steps+1,3), dtype=np.float64)
  dt = 1.0/num_steps * (b-a)
  result[0,0] = 0
  result[0, 1] = ya
  result[0, 2] = va
  for i in range(num_steps):
    i + 1
    result[i + 1, 0] = result[i,0] + (b-a) / num_steps
    result[i + 1, 1] = _step(f, result[i, :], (b-a) / num_steps, i)[0]
    result[i + 1, 2] = _step(f, result[i, :], (b-a) / num_steps, i)[1]

  return result

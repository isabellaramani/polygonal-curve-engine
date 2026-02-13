# Copilot / AI agent instructions — pitone

Purpose: quick orientation for AI coding agents working on this small project. This repo is a single-script demo that computes a polygon winding number and animates an interpolation to a canonical "star" polygon using NumPy + matplotlib. The goal is to make small changes, add tests, or refactor while preserving interactive behavior.

Quick start (Windows PowerShell):

```powershell
# install runtime deps
pip install numpy matplotlib

# run the demo
python .\test.py
```

Key files
- `test.py` — single entrypoint. Top-level responsibilities:
  - geometry helpers: `angle(p1,p2,p3)`, `winding_number(polygon)`
  - canonical star generator: `star_polygon(n, radius=3)`
  - interpolation: `interpolate(poly1, poly2, steps=50)` returns a list of frames (NumPy arrays)
  - GUI/animator: `class PolygonAnimator` draws frames with matplotlib and provides Next/Prev buttons

Important patterns & conventions (project-specific)
- Entrypoint is a script: the polygon to test is defined under `if __name__ == "__main__":` — modify that array to change input.
- `interpolate` expects two polygons with the same number of vertices (shape (n,2)). Code currently truncates the larger polygon to the smaller length in `__main__` — preserve or improve this behavior when refactoring.
- `PolygonAnimator.update()` appends the first vertex to the polygon (`np.vstack((poly, poly[0]))`) to close the loop before plotting — keep this when changing plotting code.
- `star_polygon` uses a canonical step of 2 (special-cases n==4 to create a bow-tie). This is intentional: changing the step changes the target topology.

Data shapes / contracts (short)
- polygon: numpy array with shape (n,2) where rows = vertices in order.
- interpolate(...) -> list of numpy arrays, each shape (n,2).
- winding_number(polygon) -> small integer (can be negative depending on orientation). In main the code uses `abs(winding_number(...))`.

Common pitfalls to avoid
- Mismatched vertex counts: don’t assume functions will re-index; interpolation requires equal vertex counts.
- Orientation/sign: `winding_number` returns a signed count (main uses abs()). Tests or downstream logic may rely on sign — check carefully.
- Interactive plotting: `PolygonAnimator` keeps state; automated tests should avoid launching the GUI (mock or import small helpers).

Examples for quick edits (concrete)
- Change input polygon: edit the `polygon = np.array([...])` in `test.py`.
- Change target star size: adjust `n_star` computation in `__main__` (currently `n_star = 2*wn + 1` when wn > 0).
- Add unit test for winding number: create `tests/test_winding.py` with a few small arrays and assert expected values.

Debugging tips
- Run a quick function check without the GUI:
  ```powershell
  python -c "import numpy as np; from test import winding_number; print(winding_number(np.array([[0,0],[1,0],[1,1],[0,1]])))"
  ```
- If matplotlib windows hang on CI, run tests in headless mode by setting `MPLBACKEND=Agg` or mocking plotting calls.

When changing behavior
- Keep the interactive demo separate from pure computations (geometry functions). If you refactor, ensure `winding_number`, `angle`, `star_polygon`, and `interpolate` remain importable and side-effect free.

Next steps for AI agents
- If asked to implement features, prefer adding unit tests for the geometry helpers first (happy path + 1-2 edge cases), then change GUI wiring.
- Ask before changing the canonical `star_polygon` stepping logic — higher-level decisions about star topology should come from the repo owner.

If anything above is unclear or you want extra details (tests, CI advice, or a small refactor), tell me which area and I will expand or iterate.

import torch

def b_spline_basis(x: torch.Tensor, knots: torch.Tensor, degree: int, return_all: bool = False) -> torch.Tensor:
    r"""
    Compute B-spline basis functions of a given degree at specified points.

    Parameters
    ----------
    x : torch.Tensor
        The input points where the basis functions are evaluated.
        Should be a 1D tensor.
    knots : torch.Tensor
        The non-decreasing sequence of knots defining the B-spline.
        Should be a 1D tensor with values in [0, 1].
        For proper boundary behavior, the knot sequence should typically include
        (degree + 1) repeated knots at each end (clamped B-spline).
    degree : int
        The degree of the B-spline basis functions (non-negative integer).
    return_all : bool, optional
        If True, returns all basis functions up to the specified degree.

    Returns
    -------
    torch.Tensor
        A 2D tensor of shape (len(x), n_bases) where each column corresponds to a B-spline 
        basis function evaluated at the points in `x`. The basis functions sum to 1 at each point.

    Notes
    -----
    The number of B-spline basis functions, :math:`n_{\text{bases}}`, is determined
    by the number of interior knots :math:`n` and the degree :math:`p`:

    .. math::

        n_{\text{bases}} = n + p + 1

    where :math:`n` is len(knots).

    The basis functions are computed using the Cox-de Boor recursion formula.

    **Cox-de Boor recursion formula:**

    The B-spline basis functions of degree :math:`p` are defined recursively as:

    **Base case (degree 0):**

    .. math::

        N_{i,0}(x) = 
        \begin{cases}
            1, & \text{if } t_i \leq x \leq t_{i+1}, \\
            0, & \text{otherwise}.
        \end{cases}

    **Recursive case:**

    For degrees :math:`p \geq 1`:

    .. math::

        N_{i,p}(x) = \frac{x - t_i}{t_{i+p} - t_i} N_{i,p-1}(x) + \frac{t_{i+p+1} - x}{t_{i+p+1} - t_{i+1}} N_{i+1,p-1}(x)

    If a denominator is zero, the corresponding term is defined to be zero.

    Examples
    --------
    >>> import torch
    >>> x = torch.linspace(0, 1, 5)  # [0.00, 0.25, 0.50, 0.75, 1.00]
    >>> knots = torch.tensor([0, 0.2, 0.4, 0.6, 0.8, 1])
    >>> degree = 2
    >>> basis = b_spline_basis(x, knots, degree)
    >>> print(basis.shape) # 5 points, 7 basis functions (n + p + 1 = 4 + 2 + 1)
    >>> torch.allclose(basis.sum(dim=1), torch.ones(5))  # Sum to 1
    """
    # Input validation
    if degree < 0:
        raise ValueError("Degree must be non-negative")
    
    if not torch.all(knots[1:] >= knots[:-1]):
        raise ValueError("Knots must be in non-decreasing order")
    
    if torch.any(knots < 0) or torch.any(knots > 1):
        raise ValueError("Knots must be in the interval [0, 1]")
    
    # Ensure knots are on same device as input x
    device = x.device
    knots = knots.to(device)
    
    # Match input dtype
    dtype = x.dtype
    n_points = len(x)
    n_knots = len(knots)
    n_bases = n_knots - degree - 1
    
    # Initialize the basis functions matrix for all degrees
    basis = torch.zeros((degree + 1, n_points, n_bases + degree), dtype=dtype, device=device)
    
    # Initialize degree 0 basis functions
    for j in range(n_knots - 1):
        if j < n_knots - degree - 2:
            mask = (knots[j] <= x) & (x < knots[j + 1])
        else:
            # For the last interval, include the right endpoint
            mask = (knots[j] <= x) & (x <= knots[j + 1])
        basis[0, :, j] = mask.to(dtype)
    
    # Add numerical stability threshold
    eps = 1e-10
    
    # Compute basis functions for higher degrees
    for p in range(1, degree + 1):
        for j in range(n_knots - p - 1):
            # Left term
            denom1 = knots[j + p] - knots[j]
            left = torch.zeros_like(x, dtype=dtype, device=device)
            if denom1 > eps:
                left = (x - knots[j]) / denom1 * basis[p-1, :, j]
            
            # Right term
            denom2 = knots[j + p + 1] - knots[j + 1]
            right = torch.zeros_like(x, dtype=dtype, device=device)
            if denom2 > eps:
                right = (knots[j + p + 1] - x) / denom2 * basis[p-1, :, j + 1]
            
            basis[p, :, j] = left + right
    
    if return_all:
        return basis

    return basis[degree, :, :n_bases]

def b_spline_basis_derivative(x: torch.Tensor, knots: torch.Tensor, degree: int, order: int) -> torch.Tensor:
    """Compute the derivative of B-spline basis functions.
    
    Parameters
    ----------
    x : torch.Tensor
        Points at which to evaluate the derivative. Should be a 1D tensor.
    knots : torch.Tensor
        The knot sequence defining the B-spline. Should be a 1D tensor with values in [0, 1].
    degree : int
        The degree of the B-spline basis functions (non-negative integer).
    order : int
        Order of the derivative to compute. Must be non-negative.
        If greater than degree, returns zeros.
        
    Returns
    -------
    torch.Tensor
        A 2D tensor of shape (len(x), n_bases) containing the derivative values
        of each basis function at the specified points.
    """
    if order == 0:
        return b_spline_basis(x, knots, degree)
    
    if order > degree:
        return torch.zeros((len(x), len(knots) - degree - 1), dtype=x.dtype, device=x.device)
    
    # Only adjust x if there are points at the upper endpoint to avoid 0 derivatives
    eps = 1e-6
    upper_endpoint_mask = (x == knots[-1])
    if upper_endpoint_mask.any():
        x_adj = x.clone()
        x_adj[upper_endpoint_mask] -= eps
    else:
        x_adj = x
    
    n_points = len(x)
    n_bases = len(knots) - degree - 1
    knots = knots.to(x.device)
    
    if order == 1:
        basis = b_spline_basis(x_adj, knots, degree - 1)
        denom1 = knots[degree:degree+n_bases] - knots[:n_bases]
        denom2 = knots[degree+1:degree+n_bases+1] - knots[1:n_bases+1]
        
        valid_denom1 = denom1 > 1e-10
        valid_denom2 = denom2 > 1e-10
        result = torch.zeros((n_points, n_bases), dtype=x.dtype, device=x.device)
        result[:, valid_denom1] += degree * basis[:, :-1][:, valid_denom1] / denom1[valid_denom1]
        result[:, valid_denom2] -= degree * basis[:, 1:][:, valid_denom2] / denom2[valid_denom2]
        
        return result
    
    # For higher order derivatives, recursively compute using the same formula
    # but with degree-1 and order-1
    return degree * (
        _div_or_zero(
            b_spline_basis_derivative(x_adj, knots, degree-1, order-1)[:, :-1],
            knots[degree:degree+n_bases] - knots[:n_bases]
        ) -
        _div_or_zero(
            b_spline_basis_derivative(x_adj, knots, degree-1, order-1)[:, 1:],
            knots[degree+1:degree+n_bases+1] - knots[1:n_bases+1]
        )
    )

def _div_or_zero(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    """Safe division that returns 0 when denominator is too small."""
    mask = b > 1e-10
    result = torch.zeros_like(a)
    result[:, mask] = a[:, mask] / b[mask]
    return result

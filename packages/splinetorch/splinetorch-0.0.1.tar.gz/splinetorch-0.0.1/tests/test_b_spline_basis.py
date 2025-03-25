import torch
import pytest
from splinetorch.b_spline_basis import b_spline_basis, b_spline_basis_derivative

torch.manual_seed(42)

def test_partition_of_unity():
    x = torch.linspace(0, 1, 100)
    knots = torch.tensor([0.0, 0.0, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.0, 1.0])
    degree = 2
    basis = b_spline_basis(x, knots, degree)
    assert torch.allclose(basis.sum(dim=1), torch.ones(len(x)))

def test_endpoint_values():
    x = torch.tensor([0.0, 1.0])
    knots = torch.tensor([0.0, 0.0, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.0, 1.0])
    degree = 2
    basis = b_spline_basis(x, knots, degree)
    
    # At x=0, only the first basis function should be 1
    assert torch.allclose(basis[0, 0], torch.tensor(1.0))
    assert torch.allclose(basis[0, 1:], torch.zeros(basis.shape[1]-1))
    
    # At x=1, only the last basis function should be 1
    assert torch.allclose(basis[1, -1], torch.tensor(1.0))
    assert torch.allclose(basis[1, :-1], torch.zeros(basis.shape[1]-1))

def test_non_negative():
    x = torch.linspace(0, 1, 100)
    knots = torch.tensor([0.0, 0.0, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.0, 1.0])
    degree = 3
    basis = b_spline_basis(x, knots, degree)
    assert (basis >= 0).all()

def test_shape():
    torch.manual_seed(42)
    x = torch.linspace(0, 1, 10)
    test_cases = [
        (torch.tensor([0.0, 0.5, 1.0]), 2),
        (torch.tensor([0.0, 0.3, 0.6, 1.0]), 2),
        (torch.tensor([0.0, 0.2, 0.4, 0.6, 0.8, 1.0]), 3),
    ]
    
    for knots, degree in test_cases:
        knots = torch.cat((torch.zeros(degree + 1), knots[1:-1], torch.ones(degree + 1)))
        basis = b_spline_basis(x, knots, degree)
        expected_n_bases = len(knots) - degree - 1
        assert basis.shape == (len(x), expected_n_bases)

def test_input_validation():
    x = torch.linspace(0, 1, 10)
    knots = torch.tensor([0.0, 0.0, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.0, 1.0])
    
    # Test invalid degree
    with pytest.raises(ValueError):
        b_spline_basis(x, knots, -1)
    
    # Test non-increasing knots
    with pytest.raises(ValueError):
        b_spline_basis(x, torch.tensor([0.0, 0.4, 0.2, 1.0]), 2)
    
    # Test knots outside [0, 1]
    with pytest.raises(ValueError):
        b_spline_basis(x, torch.tensor([0.0, -0.1, 0.5, 1.0]), 2)
    with pytest.raises(ValueError):
        b_spline_basis(x, torch.tensor([0.0, 0.5, 1.1, 1.0]), 2)

def test_degree_zero():
    x = torch.linspace(0, 1, 100)
    knots = torch.tensor([0.0, 0.3, 0.7, 1.0])
    basis = b_spline_basis(x, knots, degree=0)
    
    # Each point should have exactly one basis function equal to 1
    assert torch.allclose(basis.sum(dim=1), torch.ones(len(x)))
    assert (torch.sum(basis == 1, dim=1) == 1).all()

def test_single_point_evaluation():
    x = torch.tensor([0.5])
    knots = torch.tensor([0.0, 0.0, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.0, 1.0])
    degree = 2
    basis = b_spline_basis(x, knots, degree)
    expected_n_bases = len(knots) - degree - 1
    assert basis.shape == (1, expected_n_bases)
    assert torch.allclose(basis.sum(), torch.tensor(1.0))

def test_reproducibility():
    x = torch.linspace(0, 1, 10)
    knots = torch.tensor([0.0, 0.0, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.0, 1.0])
    degree = 2
    
    basis1 = b_spline_basis(x, knots, degree)
    basis2 = b_spline_basis(x, knots, degree)
    assert torch.allclose(basis1, basis2)

def test_dtype_consistency():
    x = torch.linspace(0, 1, 10, dtype=torch.float64)
    knots = torch.tensor([0.0, 0.2, 0.4, 0.6, 0.8, 1.0], dtype=torch.float64)
    degree = 2
    basis = b_spline_basis(x, knots, degree)
    assert basis.dtype == torch.float64

def test_derivative_shape():
    x = torch.linspace(0, 1, 10)
    knots = torch.tensor([0.0, 0.0, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.0, 1.0])
    degree = 3
    
    for order in range(degree + 2):  # Test up to degree + 1
        deriv = b_spline_basis_derivative(x, knots, degree, order)
        expected_n_bases = len(knots) - degree - 1
        assert deriv.shape == (len(x), expected_n_bases)

def test_derivative_zero_order():
    """Test that 0th derivative equals the basis functions"""
    x = torch.linspace(0, 1, 10)
    knots = torch.tensor([0.0, 0.0, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.0, 1.0])
    degree = 2
    
    basis = b_spline_basis(x, knots, degree)
    deriv = b_spline_basis_derivative(x, knots, degree, order=0)
    assert torch.allclose(basis, deriv)

def test_derivative_higher_than_degree():
    """Test that derivatives of order > degree are zero"""
    x = torch.linspace(0, 1, 10)
    knots = torch.tensor([0.0, 0.0, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.0, 1.0])
    degree = 2
    
    deriv = b_spline_basis_derivative(x, knots, degree, order=degree+1)
    assert torch.allclose(deriv, torch.zeros_like(deriv))

def test_derivative_partition_of_unity():
    """Test that first derivatives sum to zero"""
    x = torch.linspace(0, 1, 100)
    knots = torch.tensor([0.0, 0.0, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.0, 1.0])
    degree = 2
    
    deriv = b_spline_basis_derivative(x, knots, degree, order=1)
    assert torch.allclose(deriv.sum(dim=1), torch.zeros(len(x)), atol=1e-6)

def test_derivative_endpoint_values():
    """Test derivative values at endpoints"""
    x = torch.tensor([0.0, 1.0])
    knots = torch.tensor([0.0, 0.0, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.0, 1.0])
    degree = 2
    
    deriv = b_spline_basis_derivative(x, knots, degree, order=1)
    
    # Check all right/left derivatives are zero at endpoints
    assert torch.allclose(deriv[0, 3:], torch.zeros(deriv.shape[1]-3))
    assert torch.allclose(deriv[1, :-3], torch.zeros(deriv.shape[1]-3))

def test_derivative_constant_reproduction():
    """Test that derivatives of constant functions are zero"""
    x = torch.linspace(0, 1, 10)
    knots = torch.tensor([0.0, 0.0, 0.0, 0.5, 1.0, 1.0, 1.0])
    degree = 2
    
    # third derivative of quadratic B-spline should be zero
    deriv = b_spline_basis_derivative(x, knots, degree, order=3)
    assert torch.allclose(deriv, torch.zeros_like(deriv), atol=1e-6)

def test_derivative_linear_reproduction():
    """Test derivatives of linear B-splines"""
    x = torch.linspace(0, 1, 10)
    knots = torch.tensor([0.0, 0.0, 0.5, 1.0, 1.0])
    degree = 1
    
    # First derivative of linear B-spline should be constant
    deriv = b_spline_basis_derivative(x, knots, degree, order=1)
    
    # Check that derivatives between knots are constant
    for i in range(deriv.shape[1]):
        mask1 = deriv[:5, i] != 0
        mask2 = deriv[5:, i] != 0
        if mask1.any():
            unique_vals = torch.unique(deriv[:5][mask1, i])
            assert len(unique_vals) == 1
        if mask2.any():
            unique_vals = torch.unique(deriv[5:][mask2, i])
            assert len(unique_vals) == 1

def test_derivative_numerical():
    """Test derivative values against numerical differentiation"""
    x = torch.linspace(0.1, 0.9, 10)  # Avoid endpoints for stability
    knots = torch.tensor([0.0, 0.0, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.0, 1.0])
    degree = 2
    h = 1e-3
    
    # Compute numerical derivative
    basis_plus = b_spline_basis(x + h, knots, degree)
    basis_minus = b_spline_basis(x - h, knots, degree)
    numerical_deriv = (basis_plus - basis_minus) / (2 * h)
    
    # Compute analytical derivative
    analytical_deriv = b_spline_basis_derivative(x, knots, degree, order=1)
    
    assert torch.allclose(numerical_deriv, analytical_deriv, atol=1e-4)

def test_derivative_dtype_consistency():
    """Test that derivatives maintain dtype"""
    x = torch.linspace(0, 1, 10, dtype=torch.float64)
    knots = torch.tensor([0.0, 0.0, 0.0, 0.5, 1.0, 1.0, 1.0], dtype=torch.float64)
    degree = 2
    
    deriv = b_spline_basis_derivative(x, knots, degree, order=1)
    assert deriv.dtype == torch.float64

def test_derivative_device_consistency():
    """Test that derivatives maintain device placement"""
    x = torch.linspace(0, 1, 10)
    knots = torch.tensor([0.0, 0.0, 0.0, 0.5, 1.0, 1.0, 1.0])
    degree = 2
    
    deriv = b_spline_basis_derivative(x, knots, degree, order=1)
    assert deriv.device == x.device

# def test_higher_order_derivatives():
#     """Test higher-order derivatives of B-spline basis functions."""
#     x = torch.tensor([0.5])
#     degree = 3
#     knots = torch.tensor([0., 0., 0., 0., 0.5, 1., 1., 1., 1.])
    
#     # First derivative
#     deriv1 = b_spline_basis_derivative(x, knots, degree, 1)
    
#     # Second derivative
#     deriv2 = b_spline_basis_derivative(x, knots, degree, 2)
    
#     # Third derivative
#     deriv3 = b_spline_basis_derivative(x, knots, degree, 3)
    
#     # Check that derivatives have correct shapes
#     assert deriv1.shape == (1, len(knots) - degree - 1)
#     assert deriv2.shape == (1, len(knots) - degree - 1)
#     assert deriv3.shape == (1, len(knots) - degree - 1)
    
#     # Third derivative should be constant for cubic splines
#     assert torch.allclose(deriv3, deriv3[0])







import torch
import pytest
import numpy as np
import matplotlib.pyplot as plt
from splinetorch.b_spline import BSpline

torch.manual_seed(42)

@pytest.fixture
def simple_data():
    x = torch.linspace(0, 1, 10)
    y = torch.sin(2 * torch.pi * x)
    return x.view(-1, 1), y.view(-1, 1)

@pytest.fixture
def multivariate_data():
    torch.manual_seed(42)
    x = torch.rand(20, 2)
    y = torch.sum(x**2, dim=1).view(-1, 1)
    return x, y

@pytest.fixture
def binary_data():
    x = torch.linspace(0, 1, 100).view(-1, 1)
    # Create binary labels based on a sine wave threshold
    y = (torch.sin(2 * torch.pi * x) > 0).float()
    return x, y

@pytest.fixture
def categorical_data():
    x = torch.linspace(0, 1, 100).view(-1, 1)
    # Create 3 classes based on x value ranges
    y = torch.zeros(100)
    y[(x.flatten() >= 0.33) & (x.flatten() < 0.66)] = 1
    y[x.flatten() >= 0.66] = 2
    return x, y.long()

def test_initialization():
    torch.manual_seed(42)
    knots = torch.linspace(0, 1, 10)
    spline = BSpline(input_dim=1, output_dim=1, knots=knots)
    assert spline.coefficients.shape[0] == 1
    assert spline.coefficients.shape[2] == 1

    # Test initialization with data
    x = torch.linspace(0, 1, 10).view(-1, 1)
    y = torch.sin(2 * torch.pi * x)
    spline = BSpline(x=x, y=y)
    assert spline.coefficients.shape[0] == 1
    assert spline.coefficients.shape[2] == 1

    # Test initialization with custom knots
    knots = torch.linspace(0, 1, 5)
    spline = BSpline(x=x, y=y, knots=knots)
    assert len(spline.knots.unique()) == len(knots)

    # Test initialization with multiple input dimensions
    x_multi = torch.rand(10, 2)  # 2D input
    y_multi = torch.sum(x_multi**2, dim=1).view(-1, 1)
    spline_multi = BSpline(x=x_multi, y=y_multi)
    assert spline_multi.coefficients.shape[0] == 2
    assert spline_multi.coefficients.shape[2] == 1

    # Add new tests for output_type initialization
    x = torch.linspace(0, 1, 10).view(-1, 1)
    y_binary = (x > 0.5).float()
    spline_binary = BSpline(x=x, y=y_binary, output_type="binary")
    assert spline_binary.output_type == "binary"
    assert spline_binary.coefficients.shape[2] == 1

    # Test categorical classification initialization
    y_categorical = torch.randint(0, 3, (10,))
    spline_categorical = BSpline(x=x, y=y_categorical, output_type="categorical")
    assert spline_categorical.output_type == "categorical"
    num_classes = len(torch.unique(y_categorical))
    assert spline_categorical.coefficients.shape[2] == num_classes

def test_input_validation():
    with pytest.raises(ValueError):
        BSpline()
    
    with pytest.raises(ValueError):
        BSpline(input_dim=1)
    
    with pytest.raises(ValueError):
        x = torch.randn(10, 1, 1)
        y = torch.randn(10, 1)
        BSpline(x=x, y=y)

def test_fit_and_predict(simple_data):
    x, y = simple_data
    spline = BSpline(x=x, y=y, degree=3)
    
    spline.fit(x, y, epochs=10)
    y_pred = spline.predict(x)
    assert y_pred.shape == y.shape
    
    # Test that predictions are reasonable (MSE should be small)
    mse = torch.mean((y - y_pred) ** 2)
    assert mse < 0.1

def test_multivariate_fit(multivariate_data):
    x, y = multivariate_data
    spline = BSpline(x=x, y=y, degree=2)
    
    spline.fit(x, y, epochs=10)
    y_pred = spline.predict(x)
    
    assert y_pred.shape == y.shape
    mse = torch.mean((y - y_pred) ** 2)
    assert mse < 0.1

def test_constraints():
    """Test positive and monotone constraints."""
    x = torch.linspace(0, 1, 20).view(-1, 1)
    # Using sin(4πx) - 0.5: oscillates and has negative values
    y = torch.sin(4 * torch.pi * x) - 0.5
    
    spline_pos = BSpline(x=x, y=y, positive=True)
    spline_pos.fit(x, y, epochs=10)
    y_pred_pos = spline_pos.predict(x)
    assert torch.all(y_pred_pos >= 0)
    
    spline_mono = BSpline(x=x, y=y, monotone=True)
    spline_mono.fit(x, y, epochs=10)
    y_pred_mono = spline_mono.predict(x)
    diffs = y_pred_mono[1:] - y_pred_mono[:-1]
    assert torch.all(diffs >= -1e-6)

def test_plot_fit(simple_data, monkeypatch):
    monkeypatch.setattr(plt, 'show', lambda: None)
    
    x, y = simple_data
    spline = BSpline(x=x, y=y)
    spline.fit(x, y, epochs=10)
    spline.plot_fit(x, y)

def test_early_stopping(simple_data):
    x, y = simple_data
    spline = BSpline(x=x, y=y)
    spline.fit(x, y, epochs=1000, early_stopping_patience=2, early_stopping_tol=1e-10)
    y_pred = spline.predict(x)
    assert y_pred.shape == y.shape

def test_device_handling(simple_data):
    x, y = simple_data
    spline = BSpline(x=x, y=y)
    
    spline.fit(x, y, device='cpu')
    assert spline.coefficients.device.type == 'cpu'
    
    if torch.cuda.is_available():
        spline.fit(x, y, device='cuda')
        y_pred_cuda = spline.predict(x)
        
        # Test that model can still work on CPU after CUDA training
        y_pred_cpu = spline.predict(x)
        assert y_pred_cpu.device.type == 'cpu'
        assert torch.allclose(y_pred_cuda.cpu(), y_pred_cpu, atol=1e-6)

def test_rescale_input(simple_data):
    x, y = simple_data
    spline = BSpline(x=x, y=y)
    
    x_rescaled = spline._rescale_input(x)
    assert torch.all(x_rescaled >= 0)
    assert torch.all(x_rescaled <= 1)

def test_out_of_range_input():
    """Test behavior with input values outside [0, 1] range."""
    torch.manual_seed(42)
    
    x_single = torch.tensor([-0.5]).view(-1, 1)
    y_single = torch.tensor([0.0]).view(-1, 1)
    spline_single = BSpline(x=x_single, y=y_single)
    
    x_multi = torch.tensor([-0.5, 0.2, 1.5, 2.0]).view(-1, 1)
    y_multi = torch.tensor([0.0, 0.2, 0.4, 0.5]).view(-1, 1)
    spline_multi = BSpline(x=x_multi, y=y_multi)
    
    x_test = torch.tensor([-1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0]).view(-1, 1)
    
    y_pred_single = spline_single.predict(x_test)
    y_pred_multi = spline_multi.predict(x_test)
    
    assert y_pred_single.shape == (len(x_test), 1)
    assert y_pred_multi.shape == (len(x_test), 1)
    
    x_2d = torch.tensor([
        [-0.5, -0.5],
        [0.2, 1.5],
        [1.5, 0.2],
        [2.0, 2.0]
    ])
    y_2d = torch.sum(x_2d**2, dim=1).view(-1, 1)
    spline_2d = BSpline(x=x_2d, y=y_2d)
    
    x_test_2d = torch.tensor([
        [-1.0, -1.0],
        [0.5, 0.5],
        [1.5, 1.5]
    ])
    
    y_pred_2d = spline_2d.predict(x_test_2d)
    assert y_pred_2d.shape == (len(x_test_2d), 1)

def test_binary_classification(binary_data):
    x, y = binary_data
    spline = BSpline(x=x, y=y, output_type="binary")
    
    spline.fit(x, y, epochs=50)
    y_pred = spline.predict(x)
    
    # Check output shape and range
    assert y_pred.shape == y.shape
    assert torch.all(y_pred >= 0) and torch.all(y_pred <= 1)
    
    # Convert probabilities to binary predictions
    y_pred_binary = (y_pred > 0.5).float()
    
    # Check accuracy (should be reasonable for this simple case)
    accuracy = (y_pred_binary == y).float().mean()
    assert accuracy > 0.8

def test_categorical_classification(categorical_data):
    x, y = categorical_data
    num_classes = len(torch.unique(y))
    spline = BSpline(x=x, y=y, output_type="categorical")  # Remove output_dim parameter
    
    spline.fit(x, y, epochs=50)
    y_pred = spline.predict(x)
    
    # Check output shape
    assert y_pred.shape == (len(x), num_classes)
    
    # Check that predictions sum to 1
    assert torch.allclose(y_pred.sum(dim=1), torch.ones(len(x)), atol=1e-6)
    
    # Convert probabilities to class predictions
    y_pred_classes = torch.argmax(y_pred, dim=1)
    
    # Check accuracy (should be reasonable for this simple case)
    accuracy = (y_pred_classes == y).float().mean()
    assert accuracy > 0.7

def test_output_type_validation():
    x = torch.linspace(0, 1, 10).view(-1, 1)
    y = torch.zeros(10, 1)
    
    # Test invalid output_type
    with pytest.raises(ValueError):
        BSpline(x=x, y=y, output_type="invalid_type")

def test_binary_prediction_range(binary_data):
    x, y = binary_data
    spline = BSpline(x=x, y=y, output_type="binary")
    
    # Test with out-of-range inputs
    x_test = torch.tensor([-0.5, 0.0, 0.5, 1.0, 1.5]).view(-1, 1)
    y_pred = spline.predict(x_test)
    
    # Predictions should still be valid probabilities
    assert torch.all(y_pred >= 0) and torch.all(y_pred <= 1)

def test_categorical_prediction_distribution(categorical_data):
    x, y = categorical_data
    num_classes = len(torch.unique(y))
    spline = BSpline(x=x, y=y, output_dim=num_classes, output_type="categorical")
    
    # Test with various inputs
    x_test = torch.tensor([-0.5, 0.0, 0.5, 1.0, 1.5]).view(-1, 1)
    y_pred = spline.predict(x_test)
    
    # Check that predictions are valid probability distributions
    assert torch.all(y_pred >= 0) and torch.all(y_pred <= 1)
    assert torch.allclose(y_pred.sum(dim=1), torch.ones(len(x_test)), atol=1e-6)

def test_multivariate_binary_classification():
    # Create 2D input data
    x = torch.rand(100, 2)
    # Create binary labels based on distance from center
    y = (torch.sum((x - 0.5)**2, dim=1) < 0.25).float().view(-1, 1)
    
    spline = BSpline(x=x, y=y, output_type="binary")
    spline.fit(x, y, epochs=50)
    y_pred = spline.predict(x)
    
    assert y_pred.shape == y.shape
    assert torch.all(y_pred >= 0) and torch.all(y_pred <= 1)
    
    # Test accuracy
    y_pred_binary = (y_pred > 0.5).float()
    accuracy = (y_pred_binary == y).float().mean()
    assert accuracy > 0.7

def test_constant_function_derivatives():
    """Test derivatives of a constant function (should all be zero)."""
    x = torch.linspace(0, 1, 20).view(-1, 1)
    y = torch.ones_like(x)
    
    spline = BSpline(x=x, y=y, degree=3, number_of_knots=5)
    spline.fit(x, y, epochs=100)
    
    # First three derivatives should be close to zero
    for order in range(1, 4):
        deriv = spline.evaluate_derivative(x, order)
        assert torch.allclose(deriv, torch.zeros_like(deriv), atol=1e-3)

def test_linear_function_derivatives():
    """Test derivatives of a linear function."""
    x = torch.linspace(0, 1, 300).view(-1, 1)
    y = 2*x + 1  # y = 2x + 1
    
    spline = BSpline(x=x, y=y, degree=3, number_of_knots=10)
    spline.fit(x, y, lr=0.1, early_stopping_patience=4000)

    # pred acc
    d0 = spline.evaluate_derivative(x, 0)
    print((((d0-1)/2) - x).round(decimals=3))

    # First derivative should be close to 2
    d1 = spline.evaluate_derivative(x, 1)
    assert torch.allclose(d1, 2*torch.ones_like(d1), atol=1e-1)
    
    # Higher derivatives should be close to 0
    for order in range(2, 4):
        deriv = spline.evaluate_derivative(x, order)
        assert torch.allclose(deriv, torch.zeros_like(deriv), atol=1)

def test_sine_function_derivatives():
    """Test derivatives of sine function."""
    x = torch.linspace(0, 2*np.pi, 50).view(-1, 1)
    y = torch.sin(x)
    
    spline = BSpline(x=x, y=y, degree=3, number_of_knots=15)
    spline.fit(x, y, epochs=500)
    
    # Test points
    x_test = torch.linspace(0.5, 2*np.pi-0.5, 20).view(-1, 1)
    
    # First derivative should be close to cos(x)
    d1 = spline.evaluate_derivative(x_test, 1)
    expected_d1 = torch.cos(x_test)
    assert torch.allclose(d1, expected_d1, atol=0.1)
    
    # Second derivative should be close to -sin(x)
    d2 = spline.evaluate_derivative(x_test, 2)
    expected_d2 = -torch.sin(x_test)
    assert torch.allclose(d2, expected_d2, atol=0.2)

def test_derivative_constraints():
    """Test that derivative constraints are respected."""
    x = torch.linspace(0, 1, 100).view(-1, 1)
    y = x**2
    
    # Constraint: first derivative >= 1
    derivative_constraints = {1: {'>': torch.tensor(1.0)}}
    
    spline = BSpline(x=x, y=y, degree=3, number_of_knots=7)
    spline.fit(x, y, epochs=400, constraint_weight=10.0, derivative_constraints=derivative_constraints)
    
    # Check that first derivative is >= 1 everywhere
    x_test = torch.linspace(0, 1, 100).view(-1, 1)
    d1 = spline.evaluate_derivative(x_test, 1)
    assert torch.all(d1 >= 0.99)  # Using 0.99 to account for numerical issues

def test_higher_order_derivatives():
    """Test that derivatives higher than degree return zeros."""
    x = torch.linspace(0, 1, 20).view(-1, 1)
    y = x**2
    
    degree = 3
    spline = BSpline(x=x, y=y, degree=degree, number_of_knots=5)
    spline.fit(x, y, epochs=100)
    
    # Test derivatives of order > degree
    for order in range(degree + 1, degree + 4):
        deriv = spline.evaluate_derivative(x, order)
        assert torch.allclose(deriv, torch.zeros_like(deriv))

def test_numerical_vs_analytical_derivatives():
    """Compare numerical and analytical derivatives."""
    x = torch.linspace(0, 1, 300).view(-1, 1)
    y = torch.sin(2 * np.pi * x)
    
    spline = BSpline(x=x, y=y, degree=3, number_of_knots=10)
    spline.fit(x, y)
    
    # Test points
    x_test = torch.linspace(0.1, 0.9, 10).view(-1, 1)
    h = 1e-3
    
    # First derivative
    analytical_d1 = spline.evaluate_derivative(x_test, 1)
    numerical_d1 = (spline.predict(x_test + h) - spline.predict(x_test - h)) / (2 * h)
    assert torch.allclose(analytical_d1, numerical_d1, atol=1e-1)
    
    # Second derivative
    analytical_d2 = spline.evaluate_derivative(x_test, 2)
    numerical_d2 = (spline.predict(x_test + h) - 2*spline.predict(x_test) + spline.predict(x_test - h)) / (h**2)
    assert torch.allclose(analytical_d2, numerical_d2, atol=3e-1)

def test_derivative_magnitudes():
    """Test that derivative magnitudes are reasonable."""
    x = torch.linspace(0, 1, 150).view(-1, 1)
    y = torch.sin(2 * np.pi * x)
    spline = BSpline(x=x, y=y, degree=3, number_of_knots=7)
    spline.fit(x, y, epochs=200)
    
    x_test = torch.linspace(0.1, 0.9, 10).view(-1, 1)
    # First derivative maximum should be around 2π (derivative of sin(2πx))
    d1 = spline.evaluate_derivative(x_test, 1)
    assert torch.all(torch.abs(d1) <= 2 * np.pi + 0.5)
    
    # Second derivative maximum should be around (2π)² 
    d2 = spline.evaluate_derivative(x_test, 2)
    assert torch.all(torch.abs(d2) <= (2 * np.pi)**2 + 1.0)

def test_derivative_chain_rule():
    """Test that the chain rule is correctly applied for scaled inputs."""
    # Create data with different scale
    x = torch.linspace(-5, 5, 150).view(-1, 1)  # Note the different scale
    y = 2*x
    
    spline = BSpline(x=x, y=y, degree=3, number_of_knots=9)
    spline.fit(x, y, epochs=200)
    
    x_test = torch.linspace(-4, 4, 10).view(-1, 1)
    
    # First derivative should still be approximately 2
    d1 = spline.evaluate_derivative(x_test, 1)
    assert torch.allclose(d1, torch.tensor(2.0), atol=0.2)
    
    # Second derivative should still be approximately 0
    d2 = spline.evaluate_derivative(x_test, 2)
    assert torch.allclose(d2, torch.tensor(0.0), atol=0.2)

def test_point_constraints_with_rescaling():
    """Test that point constraints work correctly with input rescaling."""
    # Create data in [-5, 5] range
    x = torch.linspace(-3, 3, 100).view(-1, 1)
    y = 2*x
    
    # Constraint points in original space
    constraint_points = torch.tensor([[-2.0], [0.0], [2.0]])
    constraint_values = torch.tensor([[-3.0], [-1.0], [3.0]])
    
    point_constraints = {
        0: {'=': (constraint_points, constraint_values)}
    }
    
    spline = BSpline(x=x, y=y, degree=3, number_of_knots=10)
    spline.fit(x, y, epochs=500, point_constraints=point_constraints, constraint_weight=10)
    
    # Verify constraints are satisfied in original space
    predictions = spline.predict(constraint_points)
    assert torch.allclose(predictions, constraint_values, atol=1e-1)

def test_derivative_constraints_with_rescaling():
    """Test that derivative constraints work correctly with input rescaling."""
    # Create data in [-2, 2] range
    x = torch.linspace(-2, 2, 100).view(-1, 1)
    y = x**2  # y = x^2
    
    # First derivative should be >= -1 everywhere
    derivative_constraints = {1: {'>': torch.tensor(-1.0)}}
    
    spline = BSpline(x=x, y=y, degree=3, number_of_knots=7)
    spline.fit(x, y, epochs=200, derivative_constraints=derivative_constraints)
    
    # Test points across the full range
    x_test = torch.linspace(-2, 2, 50).view(-1, 1)
    d1 = spline.evaluate_derivative(x_test, 1)
    assert torch.all(d1 >= -1.1)  # Allow small numerical error

def test_derivatives_different_scales():
    """Test derivatives at different input scales."""
    # Test with different input ranges
    ranges = [
        (-1, 1),    # Symmetric small range
        (-4, 7),  # Symmetric large range
        (2, 4),     # Unit interval
    ]
    
    for x_min, x_max in ranges:
        # Create quadratic function: f(x) = x^2
        x = torch.linspace(x_min, x_max, 100).view(-1, 1)
        y = x**2
        
        spline = BSpline(x=x, y=y, degree=3, number_of_knots=10)
        spline.fit(x, y)
        
        # Test points
        x_test = torch.linspace(x_min + 0.1*(x_max-x_min), x_max - 0.1*(x_max-x_min), 10).view(-1, 1)
        
        # First derivative should be 2x
        d1 = spline.evaluate_derivative(x_test, 1)
        expected_d1 = 2 * x_test
        assert torch.allclose(d1, expected_d1, rtol=0.1)
        
        # Second derivative should be 2
        d2 = spline.evaluate_derivative(x_test, 2)
        expected_d2 = 2 * torch.ones_like(x_test)
        assert torch.allclose(d2, expected_d2, rtol=0.3)

def test_mixed_constraints_with_rescaling():
    """Test combination of point and derivative constraints with rescaling."""
    x = torch.linspace(-3, 3, 100).view(-1, 1)
    y = torch.exp(x)  # y = e^x
    
    # Point constraint: f(0) = 1
    point_constraints = {
        0: {'=': (torch.tensor([[0.0]]), torch.tensor([[1.0]]))}
    }
    
    # Derivative constraint: f'(x) >= 0 (function should be increasing)
    derivative_constraints = {1: {'>': torch.tensor(0.0)}}
    
    spline = BSpline(x=x, y=y, degree=3, number_of_knots=10)
    spline.fit(x, y, epochs=300,
              point_constraints=point_constraints,
              derivative_constraints=derivative_constraints,
              constraint_weight=10.0)
    
    # Verify point constraint
    assert torch.allclose(spline.predict(torch.tensor([[0.0]])), 
                         torch.tensor([[1.0]]), 
                         atol=1e-1)
    
    # Verify derivative constraint
    x_test = torch.linspace(-2.8, 2.8, 50).view(-1, 1)
    d1 = spline.evaluate_derivative(x_test, 1)
    assert torch.all(d1 >= -1e-6)  # Allow for small numerical errors

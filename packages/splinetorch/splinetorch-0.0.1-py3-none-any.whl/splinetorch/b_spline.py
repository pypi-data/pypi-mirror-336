import torch
import torch.nn as nn
import torch.optim as optim
from .b_spline_basis import b_spline_basis, b_spline_basis_derivative

class BSpline(nn.Module):
    """B-spline implementation using PyTorch.

    Parameters
    ----------
    x : torch.Tensor, optional
        Input training data. Shape: (batch_size,) or (batch_size, input_dim)
    y : torch.Tensor, optional
        Target values. Shape: (batch_size,) or (batch_size, output_dim)
    input_dim : int, optional
        Dimension of input data. Required if x not provided.
    output_dim : int, optional
        Dimension of output data. Required if y not provided.
    knots : torch.Tensor, optional
        Knot sequence. If None, generated uniformly using number_of_knots.
    number_of_knots : int, default=10
        Number of knots to generate if knots not provided.
    degree : int, default=3
        Degree of the B-spline.
    positive : bool, default=False
        Whether to constrain the spline to be positive.
    monotone : bool, default=False
        Whether to constrain the spline to be monotone.
    increasing : torch.Tensor, optional
        Direction of monotonicity for each dimension. Only used if monotone=True.
        Shape: (input_dim, output_dim)
    output_type : str, default="continuous"
        Type of output. One of: "continuous", "binary", "categorical"

    Attributes
    ----------
    coefficients : nn.Parameter
        Learnable coefficients for the B-spline basis functions.
        Shape: (input_dim, n_bases, output_dim)
    knots : torch.Tensor
        Normalized knot sequence.
    x_range : torch.Tensor
        Min and max values of input data. Shape: (2, input_dim)
    basis : torch.Tensor or None
        Cached basis function values.

    Examples
    --------
    >>> # Simple univariate regression
    >>> x = torch.linspace(0, 1, 100).view(-1, 1)
    >>> y = torch.sin(2 * torch.pi * x) + torch.randn_like(x) * 0.1
    >>> spline = BSpline(x=x, y=y)
    >>> spline.fit(x, y)
    >>> y_pred = spline.predict(x)
    >>> spline.plot_fit(x, y)
    
    >>> # Binary classification with constraints
    >>> # Monotonely increasing logit
    >>> x = torch.linspace(0, 1, 100).view(-1, 1)
    >>> y = (torch.sin(2.2 * torch.pi * x) > 0).float()
    >>> derivative_constraints = {1: {'>': torch.tensor(0.0)}}  # Monotone increasing
    >>> spline = BSpline(x=x, y=y, output_type="binary")
    >>> spline.fit(x, y, derivative_constraints=derivative_constraints)
    >>> probabilities = spline.predict(x)
    >>> spline.plot_fit(x, y)
    
    >>> # Multivariate regression with point constraints
    >>> x = torch.rand(1000, 2)  # 2D input
    >>> y = torch.sum(2*x**2, dim=1).view(-1, 1) - 2
    >>> # True function value at (0,0) is -2, but we'll constrain it to 0
    >>> point_constraints = { 0: {'=': (torch.tensor([[0.0, 0.0]]), torch.tensor([[0.0]]))} }
    >>> spline = BSpline(x=x, y=y)
    >>> spline.fit(x, y, point_constraints=point_constraints)
    >>> y_pred = spline.predict(x)
    >>> # Verify the constraint at (0,0)
    >>> test_point = torch.tensor([[0.0, 0.0]])
    >>> predicted_value = spline.predict(test_point)
    >>> print(f"Value at (0,0): {predicted_value.item():.6f}")
    
    >>> # PDF fitting with constraints
    >>> x = torch.linspace(0, 1, 1000).view(-1, 1)
    >>> y = torch.exp(-((x - 0.5)**2) / 0.1).view(-1, 1)  # Shape: (n, 1)
    >>> spline = BSpline(x=x, y=y)
    >>> spline.fit(x, y, pdf_constraint=True)  # Ensures non-negative and integrates to 1
    >>> density = spline.predict(x)
    >>> spline.plot_fit(x, y)

    >>> # Categorical classification (3 classes)
    >>> x = torch.rand(300, 2)  # 2D input
    >>> # Create 3 classes based on distance from origin
    >>> distances = torch.sum(x**2, dim=1)
    >>> y = torch.zeros(len(x), dtype=torch.long)  # Shape: (n,)
    >>> y[distances < 0.5] = 0
    >>> y[(distances >= 0.5) & (distances < 1.0)] = 1
    >>> y[distances >= 1.0] = 2
    >>> spline = BSpline(x=x, y=y, output_type="categorical")
    >>> spline.fit(x, y)
    >>> class_probs = spline.predict(x)  # Shape: (n, 3) - probabilities for each class
    """
    def __init__(
        self,
        x: torch.Tensor = None,
        y: torch.Tensor = None,
        input_dim: int = None,
        output_dim: int = None,
        knots: torch.Tensor = None,
        number_of_knots: int = 10,
        degree: int = 3,
        positive: bool = False,
        monotone: bool = False,
        increasing: torch.Tensor = None,
        output_type: str = "continuous"
    ):
        super().__init__()
        
        # Validate output_type
        valid_types = ["continuous", "binary", "categorical"]
        if output_type not in valid_types:
            raise ValueError(f"output_type must be one of {valid_types}")
        self.output_type = output_type
        
        if x is not None:
            if x.dim() > 2:
                raise ValueError("Input x must be 1D or 2D")
            elif x.dim() == 1:
                input_dim = 1
            else:
                input_dim = x.shape[1]
        elif input_dim is None:
            raise ValueError("Either input or input_dim must be provided.")
        
        if y is not None:
            if y.dim() > 2:
                raise ValueError("Output y must be 1D or 2D")
            elif output_type == "categorical":
                output_dim = len(torch.unique(y))
            elif y.dim() == 1:
                output_dim = 1
            else:
                output_dim = y.shape[1]
        elif output_dim is None:
            raise ValueError("Either output or output_dim must be provided.")
        if increasing is None and monotone:
            increasing = torch.ones(input_dim, output_dim)
        if monotone:
            self.register_buffer('increasing', increasing)
        if knots is None:
            if x is not None:
                min_x = x.min(dim=0).values
                max_x = x.max(dim=0).values
            else:
                raise ValueError("Either input, knots or both must be provided.")

            knots = torch.linspace(0, 1, number_of_knots)
        else:
            min_x = knots.min(dim=0).values
            max_x = knots.max(dim=0).values
        
        self.monotone = monotone
        self.positive = positive
        # input dim in columns and rows min/max
        x_range = torch.cat((min_x.view(1, -1), max_x.view(1, -1)), dim=0)
        self.register_buffer('x_range', x_range)
        # standardize knots
        knots = (knots - knots.min(dim=0).values) / (knots.max(dim=0).values - knots.min(dim=0).values)
        knots = torch.cat((torch.zeros(degree), knots, torch.ones(degree)))
        self.register_buffer('knots', knots)
        self.degree = degree
        self.basis = None

        n_bases = len(knots) - degree - 1
        self.coefficients = nn.Parameter(torch.zeros(input_dim, n_bases, output_dim) * 0.01)
        
        # Store new constraint attributes
        self.derivative_constraints = None
        self.point_constraints = None
        self.pdf_constraint = False

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Evaluate the B-spline at given points.

        Parameters
        ----------
        x : torch.Tensor
            Points at which to evaluate the spline.
            Shape: (batch_size,) or (batch_size, input_dim)

        Returns
        -------
        torch.Tensor
            Spline values at the input points:
            - For continuous: raw values
            - For binary: probabilities between 0 and 1
            - For categorical: class probabilities (sum to 1)
        """
        if self.monotone:
            mono_coef = self._monotone_params()
            out = torch.einsum('...ib,...bo->...io', self.basis, mono_coef)
            out *= self.increasing.unsqueeze(1)
        elif self.positive:
            out = torch.einsum('...ib,...bo->...io', self.basis, torch.nn.functional.softplus(self.coefficients))
        else:   
            out = torch.einsum('...ib,...bo->...io', self.basis, self.coefficients)
        
        out = out.sum(dim=0)
        
        if self.output_type == "binary":
            return torch.sigmoid(out)
        elif self.output_type == "categorical":
            return nn.functional.softmax(out, dim=-1)
        else:  # continuous
            return out
    
    def predict(self, x: torch.Tensor) -> torch.Tensor:
        """Evaluate the B-spline at given points.

        Parameters
        ----------
        x : torch.Tensor
            Points at which to evaluate the spline.
            Shape: (batch_size,) or (batch_size, input_dim)

        Returns
        -------
        torch.Tensor
            Spline values at the input points.
            For continuous output: raw values
            For binary output: probabilities in [0,1]
            For categorical output: class probabilities summing to 1
            Shape: (batch_size, output_dim)
        """
        rescaled_x = self._rescale_input(x)
        self.basis = b_spline_basis(rescaled_x.T.flatten(), self.knots, self.degree)
        self.basis = self.basis.view(self.coefficients.shape[0], -1, self.basis.shape[1])
        return self(rescaled_x).detach()
    
    def _rescale_input(self, x: torch.Tensor) -> torch.Tensor:
        x_resc = (x - self.x_range[0]) / (self.x_range[1] - self.x_range[0])
        return x_resc
    
    def _monotone_params(self) -> torch.Tensor:
        if self.positive:
            params = torch.nn.functional.softplus(self.coefficients)
        else:
            mask = torch.ones_like(self.coefficients)
            mask[:, 0, :] = 0  # Keep first elements unchanged
            # Apply softplus only to masked elements while preserving gradients
            params = self.coefficients * (1 - mask) + torch.nn.functional.softplus(self.coefficients) * mask
        return torch.cumsum(params, dim=-2)

    def _compute_constraint_penalty(
        self,
        x: torch.Tensor,
        derivative_constraints: dict[int, dict[str, torch.Tensor]],
        point_constraints: dict[int, dict[str, tuple[torch.Tensor, torch.Tensor]]],
        pdf_constraint: bool
    ) -> torch.Tensor:
        """Compute penalties for all constraints."""
        penalty = torch.tensor(0.0, device=x.device)
        
        if derivative_constraints is not None:
            for order, constraints in derivative_constraints.items():
                deriv = self._evaluate_derivative(x, order)
                for sense, threshold in constraints.items():
                    if sense == '>':
                        penalty += torch.relu(threshold - deriv).mean()
                    elif sense == '<':
                        penalty += torch.relu(deriv - threshold).mean()

        if point_constraints is not None:
            for order, constraints in point_constraints.items():
                for sense, (points, values) in constraints.items():
                    # Rescale points to [0,1] space
                    points_rescaled = self._rescale_input(points)
                    # Use internal method with rescaled points
                    pred = self._evaluate_derivative(points_rescaled, order)
                    
                    if sense == '>':
                        penalty += torch.relu(values - pred).mean()
                    elif sense == '<':
                        penalty += torch.relu(pred - values).mean()
                    elif sense == '=':
                        penalty += (pred - values).pow(2).mean()

        if pdf_constraint:
            # Non-negativity
            pred = self(x)
            penalty += torch.relu(-pred).mean()
            
            # Integration to 1
            dx = (x.max() - x.min()) / (len(x) - 1)
            pred_1d = pred.squeeze()
            integral = 0.5 * (pred_1d[0] + pred_1d[-1] + 2 * pred_1d[1:-1].sum()) * dx
            penalty += 10.0 * (integral - torch.ones_like(integral)).pow(2).mean()

        return penalty

    def _evaluate_derivative(self, x: torch.Tensor, order: int) -> torch.Tensor:
        """Internal method to evaluate derivatives with already rescaled input.
        
        Parameters
        ----------
        x : torch.Tensor
            Points at which to evaluate the derivative (already rescaled to [0,1]).
            Shape: (batch_size,) or (batch_size, input_dim)
        order : int
            Order of the derivative to compute.
        
        Returns
        -------
        torch.Tensor
            Derivative values at the input points.
            Shape: (batch_size, output_dim)
        """
        if order > self.degree:
            return torch.zeros_like(x).expand(-1, self.coefficients.shape[-1])
        
        # Compute derivative basis
        deriv_basis = b_spline_basis_derivative(
            x.T.flatten(),
            self.knots,
            self.degree,
            order
        )
        deriv_basis = deriv_basis.view(self.coefficients.shape[0], -1, deriv_basis.shape[1])
        
        # Compute derivative values
        if self.monotone:
            mono_coef = self._monotone_params()
            out = torch.einsum('...ib,...bo->...io', deriv_basis, mono_coef)
            out *= self.increasing.unsqueeze(1)
        elif self.positive:
            out = torch.einsum('...ib,...bo->...io', deriv_basis, torch.nn.functional.softplus(self.coefficients))
        else:
            out = torch.einsum('...ib,...bo->...io', deriv_basis, self.coefficients)
        
        out = out.sum(dim=0)
        
        # Apply activation functions only for function values (order=0)
        if order == 0:
            if self.output_type == "binary":
                return torch.sigmoid(out)
            elif self.output_type == "categorical":
                return torch.nn.functional.softmax(out, dim=-1)
        
        return out

    def evaluate_derivative(self, x: torch.Tensor, order: int) -> torch.Tensor:
        """Evaluate the derivative of specified order at given points.
        
        Parameters
        ----------
        x : torch.Tensor
            Points at which to evaluate the derivative.
            Shape: (batch_size,) or (batch_size, input_dim)
        order : int
            Order of the derivative to compute. Must be non-negative.
            Returns zeros if order > degree.
        
        Returns
        -------
        torch.Tensor
            Derivative values at the input points.
            Shape: (batch_size, output_dim)
        """
        if order > self.degree:
            return torch.zeros_like(x).expand(-1, self.coefficients.shape[-1])
        
        # Rescale input
        rescaled_x = self._rescale_input(x)
        
        # Get derivative in rescaled space
        deriv = self._evaluate_derivative(rescaled_x, order)
        
        # Apply chain rule scaling
        scale_factor = torch.prod(1.0 / (self.x_range[1] - self.x_range[0])).item() ** order
        return deriv * scale_factor

    def fit(
        self,
        x: torch.Tensor,
        y: torch.Tensor,
        lr: float = 0.1,
        epochs: int = 5000,
        device: str = "cpu",
        smoothing_weight: float = 0.1,
        derivative_penalty: int = 2,
        constraint_weight: float = 1.0,
        early_stopping_patience: int = 150,
        early_stopping_tol: float = 1e-6,
        derivative_constraints: dict[int, dict[str, torch.Tensor]] = None,
        point_constraints: dict[int, dict[str, tuple[torch.Tensor, torch.Tensor]]] = None,
        pdf_constraint: bool = False
    ):
        """Fit the B-spline to data with optional constraints.

        Parameters
        ----------
        x : torch.Tensor
            Input data. Shape: (batch_size,) or (batch_size, input_dim)
        y : torch.Tensor
            Target values. Shape: (batch_size,) or (batch_size, output_dim)
        lr : float, default=0.1
            Learning rate for optimizer.
        epochs : int, default=5000
            Maximum number of training epochs.
        device : str, default="cpu"
            Device to use for computations ("cpu" or "cuda").
        smoothing_weight : float, default=0.1
            Weight for smoothing penalty term.
        derivative_penalty : int, default=2
            Order of derivative to penalize for smoothing.
        constraint_weight : float, default=1.0
            Weight for constraint penalty terms.
        early_stopping_patience : int, default=150
            Number of epochs to wait for improvement before stopping.
        early_stopping_tol : float, default=1e-6
            Tolerance for improvement in early stopping.
        derivative_constraints : dict, optional
            Constraints on derivatives. Format: {order: {operator: threshold}}
            where operator is one of '>', '<'
        point_constraints : dict, optional
            Point-wise constraints. Format: {order: {operator: (points, values)}}
            where operator is one of '>', '<', '='
        pdf_constraint : bool, default=False
            Whether to enforce probability density function constraints
            (non-negativity and integration to 1).
        """
        if len(x) < self.degree + 1:
            raise ValueError(f"Need at least {self.degree + 1} data points for degree {self.degree}")
        
        self.to(device)
        x = x.to(device)
        y = y.to(device)
        
        if self.output_type == "categorical":
            if y.dim() > 1:
                y = y.squeeze()

        smoothing_param_unconstrained = nn.Parameter(torch.tensor(0.0, dtype=torch.float32, device=device))
        optimizer = optim.Adam([self.coefficients, smoothing_param_unconstrained], lr=lr)

        best_loss = float('inf')
        best_coef = None
        patience_counter = 0

        rescaled_x = self._rescale_input(x)
        self.basis = b_spline_basis(rescaled_x.T.flatten(), self.knots.to(device), self.degree)
        self.basis = self.basis.view(self.coefficients.shape[0], -1, self.basis.shape[1])

        difference_matrix = torch.diff(torch.eye(self.knots.shape[0] - self.degree - 1), n=derivative_penalty, axis=0)
        penalty_matrix = difference_matrix.T @ difference_matrix
        penalty_matrix = penalty_matrix.clone().detach().to(dtype=torch.float32, device=device)  # Move to correct device
        

        try:
            for epoch in range(epochs):
                optimizer.zero_grad()
                
                # Compute prediction and main loss
                y_pred = self(rescaled_x)
                if self.output_type == "binary":
                    loss = nn.functional.binary_cross_entropy(y_pred, y.float())
                elif self.output_type == "categorical":
                    loss = nn.functional.cross_entropy(y_pred, y.long())
                else:
                    loss = nn.functional.mse_loss(y_pred, y)

                # Add constraint penalties
                constraint_loss = self._compute_constraint_penalty(
                    rescaled_x,
                    derivative_constraints,
                    point_constraints,
                    pdf_constraint
                )

                smoothing_param = torch.nn.functional.softplus(smoothing_param_unconstrained)
                # coefficients^T * penalty_matrix * coefficients
                smoothing_loss = smoothing_param * (self.coefficients[0, :, 0] @ penalty_matrix @ self.coefficients[0, :, 0])
                # smoothing_loss = smoothing_param * torch.einsum('...bi, bc, ...co -> ...io', self.coefficients, penalty_matrix, self.coefficients)
                total_loss = loss + constraint_weight * constraint_loss + smoothing_weight * smoothing_loss
                
                total_loss.backward()
                optimizer.step()
                
                # Early stopping check
                current_loss = total_loss.item()
                if current_loss < best_loss - early_stopping_tol:
                    best_loss = current_loss
                    best_coef = self.coefficients.detach().clone()
                    patience_counter = 0
                else:
                    patience_counter += 1
                    
                if patience_counter >= early_stopping_patience:
                    print(f"Early stopping at epoch {epoch+1}")
                    break
                    
                if (epoch + 1) % 10 == 0:
                    print(f"Epoch {epoch+1}/{epochs}, Loss: {current_loss:.6f}")
        
        finally:
            if best_coef is not None:
                self.coefficients.data = best_coef.cpu()
            # Move model back to CPU and restore best parameters
            self.to('cpu')

    def plot_fit(self, x: torch.Tensor, y: torch.Tensor, n_points: int = 100, extra_points_per_knot: int = 10):
        """Visualize spline fits with adaptive sampling near knots.

        Parameters
        ----------
        x : torch.Tensor
            Input tensor.
        y : torch.Tensor
            Target tensor.
        n_points : int, default=100
            Base number of points for visualization.
        extra_points_per_knot : int, default=10
            Additional points to sample around each knot.

        """
        import matplotlib.pyplot as plt
        
        input_dim = x.shape[1] if x.dim() > 1 else 1
        
        if self.output_type == "categorical":
            # For categorical, plot probability for each class
            num_classes = self.coefficients.shape[2]
            y_onehot = torch.nn.functional.one_hot(y.long(), num_classes=num_classes).float()
            output_dim = num_classes
        else:
            output_dim = y.shape[1] if y.dim() > 1 else 1
            y_onehot = y
        
        for i in range(input_dim):
            # Get knot locations for this dimension
            knots = self.knots.unique()
            knots = knots * (self.x_range[1, i] - self.x_range[0, i]) + self.x_range[0, i]
            
            # Use median for other dimensions
            x_min, x_max = self.x_range[0, i], self.x_range[1, i]
            grid = torch.linspace(x_min, x_max, n_points)
            x_median = x.median(dim=0).values
            x_grid = x_median.repeat(len(grid), 1)
            x_grid[:, i] = grid
            y_pred = self.predict(x_grid).detach()
            
            for j in range(output_dim):
                fig, ax = plt.subplots(figsize=(10, 6))
                
                if self.output_type == "categorical":
                    # For categorical, plot actual class points at 0 and 1
                    class_mask = (y == j)
                    x_class = x[class_mask]
                    if len(x_class) > 0:
                        ax.scatter(x_class[:, i].numpy(), torch.ones(len(x_class)).numpy(),
                                 color='blue', alpha=0.5, s=20, label=f'Class {j} data')
                        ax.scatter(x_class[:, i].numpy(), torch.zeros(len(x_class)).numpy(),
                                 color='blue', alpha=0.1, s=20)
                else:
                    ax.scatter(x[:, i].numpy(), y_onehot[:, j].numpy(),
                             color='blue', alpha=0.5, s=20, label='Data')
                
                ax.plot(x_grid[:, i].numpy(), y_pred[:, j].numpy(),
                       color='red', label=f'Class {j} probability' if self.output_type == "categorical" else 'Spline fit')
                
                for knot in knots:
                    ax.axvline(x=knot.item(), color='gray', linestyle='--', alpha=0.5)
                
                ax.set_xlabel(f'Input {i+1}')
                if self.output_type == "categorical":
                    ax.set_ylabel(f'Class {j} Probability')
                    ax.set_title(f'Input {i+1} vs Class {j} Probability')
                else:
                    ax.set_ylabel(f'Output {j+1}')
                    ax.set_title(f'Input {i+1} vs Output {j+1}')
                
                ax.legend()
                ax.grid(True, alpha=0.3)
                
                plt.tight_layout()
                plt.show()

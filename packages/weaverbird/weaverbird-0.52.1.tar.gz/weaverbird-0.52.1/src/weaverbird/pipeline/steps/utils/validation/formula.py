"""Validation utilities for Formula step."""
from weaverbird.pipeline.steps.formula import FormulaStep, FormulaStepWithVariable
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError

# Formula step doesn't explicitly reference columns in a way we can easily validate
# The formula itself is a string that may reference columns, but parsing it is complex


def validate_formula_step_columns(step: FormulaStep | FormulaStepWithVariable, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the formula step exist in the dataset.
    
    Note: This validator doesn't check columns referenced inside the formula expression itself,
    as that would require parsing and analyzing the formula syntax.
    
    Args:
        step: The formula step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    # Formula step doesn't have explicit column references to validate
    # The actual formula might have column references but would need a parser to validate
    pass

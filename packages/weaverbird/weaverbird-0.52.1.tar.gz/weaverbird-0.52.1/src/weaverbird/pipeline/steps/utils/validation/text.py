"""Validation utilities for Text step."""
from weaverbird.pipeline.steps.text import TextStep, TextStepWithVariable
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError

# Text step doesn't explicitly reference columns in a way we can easily validate
# The text template may reference columns, but parsing it is complex


def validate_text_step_columns(step: TextStep | TextStepWithVariable, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the text step exist in the dataset.
    
    Note: This validator doesn't check columns referenced inside the text template itself,
    as that would require parsing and analyzing the template syntax.
    
    Args:
        step: The text step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    # Text step doesn't have explicit column references to validate
    # The text template might have column references but would need a parser to validate
    pass

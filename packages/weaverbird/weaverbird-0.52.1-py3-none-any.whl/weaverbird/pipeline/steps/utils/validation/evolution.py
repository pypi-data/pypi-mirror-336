"""Validation utilities for Evolution step."""
from weaverbird.pipeline.steps.evolution import EvolutionStep, EvolutionStepWithVariable
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError


def validate_evolution_step_columns(step: EvolutionStep | EvolutionStepWithVariable, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the evolution step exist in the dataset.
    
    Args:
        step: The evolution step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        MissingColumnError: If any column referenced in the step doesn't exist in the dataset
    """
    if step.date_col not in available_columns:
        raise MissingColumnError(column=step.date_col, step_name="evolution", context="date_col parameter")
    
    if step.value_col not in available_columns:
        raise MissingColumnError(column=step.value_col, step_name="evolution", context="value_col parameter")
    
    # Check index columns if they exist
    if step.index_columns:
        for col in step.index_columns:
            if col not in available_columns:
                raise MissingColumnError(column=col, step_name="evolution", context="index_columns parameter")

"""Exceptions for step validation errors."""


class StepValidationError(Exception):
    """Base exception for validation errors in pipeline steps."""
    
    def __init__(self, message: str, step_name: str):
        self.step_name = step_name
        super().__init__(message)


class MissingColumnError(StepValidationError):
    """Exception raised when a column referenced in a step doesn't exist in the dataset."""
    
    def __init__(self, column: str, step_name: str, context: str):
        self.column = column
        self.context = context
        message = f"Column '{column}' referenced in {step_name} {context} doesn't exist in the dataset"
        super().__init__(message, step_name)
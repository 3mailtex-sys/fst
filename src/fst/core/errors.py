"""Custom exceptions used across the pipeline."""


class FSTError(Exception):
    """Base exception for application errors."""


class ConfigurationError(FSTError):
    """Raised when runtime configuration is invalid."""


class PipelineStageError(FSTError):
    """Raised when a pipeline stage fails."""

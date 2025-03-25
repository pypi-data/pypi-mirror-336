"""Validation utilities for pipeline steps."""
from weaverbird.pipeline.pipeline import PipelineStep, PipelineStepWithVariables
from weaverbird.pipeline.steps.absolutevalue import AbsoluteValueStep, AbsoluteValueStepWithVariable
from weaverbird.pipeline.steps.addmissingdates import AddMissingDatesStep, AddMissingDatesStepWithVariables
from weaverbird.pipeline.steps.aggregate import AggregateStep, AggregateStepWithVariables
from weaverbird.pipeline.steps.argmax import ArgmaxStep, ArgmaxStepWithVariable
from weaverbird.pipeline.steps.argmin import ArgminStep, ArgminStepWithVariable
from weaverbird.pipeline.steps.comparetext import CompareTextStep, CompareTextStepWithVariables
from weaverbird.pipeline.steps.concatenate import ConcatenateStep, ConcatenateStepWithVariable
from weaverbird.pipeline.steps.convert import ConvertStep
from weaverbird.pipeline.steps.cumsum import CumSumStep, CumSumStepWithVariable
from weaverbird.pipeline.steps.date_extract import DateExtractStep, DateExtractStepWithVariable
from weaverbird.pipeline.steps.delete import DeleteStep
from weaverbird.pipeline.steps.dissolve import DissolveStep
from weaverbird.pipeline.steps.duplicate import DuplicateStep
from weaverbird.pipeline.steps.duration import DurationStep, DurationStepWithVariable
from weaverbird.pipeline.steps.evolution import EvolutionStep, EvolutionStepWithVariable
from weaverbird.pipeline.steps.fillna import FillnaStep, FillnaStepWithVariable
from weaverbird.pipeline.steps.filter import FilterStep, FilterStepWithVariables
from weaverbird.pipeline.steps.formula import FormulaStep, FormulaStepWithVariable
from weaverbird.pipeline.steps.fromdate import FromdateStep
from weaverbird.pipeline.steps.hierarchy import HierarchyStep
from weaverbird.pipeline.steps.ifthenelse import IfthenelseStep, IfThenElseStepWithVariables
from weaverbird.pipeline.steps.join import JoinStep, JoinStepWithVariable
from weaverbird.pipeline.steps.lowercase import LowercaseStep
from weaverbird.pipeline.steps.moving_average import MovingAverageStep
from weaverbird.pipeline.steps.percentage import PercentageStep
from weaverbird.pipeline.steps.pivot import PivotStep, PivotStepWithVariable
from weaverbird.pipeline.steps.rank import RankStep, RankStepWithVariable
from weaverbird.pipeline.steps.rename import RenameStep, RenameStepWithVariable
from weaverbird.pipeline.steps.replace import ReplaceStep, ReplaceStepWithVariable
from weaverbird.pipeline.steps.replacetext import ReplaceTextStep, ReplaceTextStepWithVariable
from weaverbird.pipeline.steps.rollup import RollupStep, RollupStepWithVariable
from weaverbird.pipeline.steps.select import SelectStep
from weaverbird.pipeline.steps.simplify import SimplifyStep
from weaverbird.pipeline.steps.sort import SortStep
from weaverbird.pipeline.steps.split import SplitStep, SplitStepWithVariable
from weaverbird.pipeline.steps.statistics import StatisticsStep
from weaverbird.pipeline.steps.substring import SubstringStep
from weaverbird.pipeline.steps.text import TextStep, TextStepWithVariable
from weaverbird.pipeline.steps.todate import ToDateStep
from weaverbird.pipeline.steps.top import TopStep, TopStepWithVariables
from weaverbird.pipeline.steps.totals import TotalsStep, TotalsStepWithVariable
from weaverbird.pipeline.steps.trim import TrimStep
from weaverbird.pipeline.steps.uniquegroups import UniqueGroupsStep, UniqueGroupsStepWithVariable
from weaverbird.pipeline.steps.unpivot import UnpivotStep, UnpivotStepWithVariable
from weaverbird.pipeline.steps.uppercase import UppercaseStep
from weaverbird.pipeline.steps.waterfall import WaterfallStep, WaterfallStepWithVariable

from weaverbird.pipeline.steps.utils.validation.absolute_value import validate_absolute_value_step_columns
from weaverbird.pipeline.steps.utils.validation.add_missing_dates import validate_add_missing_dates_step_columns
from weaverbird.pipeline.steps.utils.validation.aggregate import validate_aggregate_step_columns
from weaverbird.pipeline.steps.utils.validation.argmax import validate_argmax_step_columns
from weaverbird.pipeline.steps.utils.validation.argmin import validate_argmin_step_columns
from weaverbird.pipeline.steps.utils.validation.compare_text import validate_compare_text_step_columns
from weaverbird.pipeline.steps.utils.validation.concatenate import validate_concatenate_step_columns
from weaverbird.pipeline.steps.utils.validation.convert import validate_convert_step_columns
from weaverbird.pipeline.steps.utils.validation.cumsum import validate_cumsum_step_columns
from weaverbird.pipeline.steps.utils.validation.date_extract import validate_date_extract_step_columns
from weaverbird.pipeline.steps.utils.validation.delete import validate_delete_step_columns
from weaverbird.pipeline.steps.utils.validation.dissolve import validate_dissolve_step_columns
from weaverbird.pipeline.steps.utils.validation.duplicate import validate_duplicate_step_columns
from weaverbird.pipeline.steps.utils.validation.duration import validate_duration_step_columns
from weaverbird.pipeline.steps.utils.validation.errors import MissingColumnError, StepValidationError
from weaverbird.pipeline.steps.utils.validation.evolution import validate_evolution_step_columns
from weaverbird.pipeline.steps.utils.validation.fillna import validate_fillna_step_columns
from weaverbird.pipeline.steps.utils.validation.filter import validate_filter_step_columns
from weaverbird.pipeline.steps.utils.validation.formula import validate_formula_step_columns
from weaverbird.pipeline.steps.utils.validation.fromdate import validate_fromdate_step_columns
from weaverbird.pipeline.steps.utils.validation.hierarchy import validate_hierarchy_step_columns
from weaverbird.pipeline.steps.utils.validation.ifthenelse import validate_ifthenelse_step_columns
from weaverbird.pipeline.steps.utils.validation.join import validate_join_step_columns
from weaverbird.pipeline.steps.utils.validation.lowercase import validate_lowercase_step_columns
from weaverbird.pipeline.steps.utils.validation.moving_average import validate_moving_average_step_columns
from weaverbird.pipeline.steps.utils.validation.percentage import validate_percentage_step_columns
from weaverbird.pipeline.steps.utils.validation.pivot import validate_pivot_step_columns
from weaverbird.pipeline.steps.utils.validation.rank import validate_rank_step_columns
from weaverbird.pipeline.steps.utils.validation.rename import validate_rename_step_columns
from weaverbird.pipeline.steps.utils.validation.replace import validate_replace_step_columns
from weaverbird.pipeline.steps.utils.validation.replacetext import validate_replacetext_step_columns
from weaverbird.pipeline.steps.utils.validation.rollup import validate_rollup_step_columns
from weaverbird.pipeline.steps.utils.validation.select import validate_select_step_columns
from weaverbird.pipeline.steps.utils.validation.simplify import validate_simplify_step_columns
from weaverbird.pipeline.steps.utils.validation.sort import validate_sort_step_columns
from weaverbird.pipeline.steps.utils.validation.split import validate_split_step_columns
from weaverbird.pipeline.steps.utils.validation.statistics import validate_statistics_step_columns
from weaverbird.pipeline.steps.utils.validation.substring import validate_substring_step_columns
from weaverbird.pipeline.steps.utils.validation.text import validate_text_step_columns
from weaverbird.pipeline.steps.utils.validation.todate import validate_todate_step_columns
from weaverbird.pipeline.steps.utils.validation.top import validate_top_step_columns
from weaverbird.pipeline.steps.utils.validation.totals import validate_totals_step_columns
from weaverbird.pipeline.steps.utils.validation.trim import validate_trim_step_columns
from weaverbird.pipeline.steps.utils.validation.uniquegroups import validate_uniquegroups_step_columns
from weaverbird.pipeline.steps.utils.validation.unpivot import validate_unpivot_step_columns
from weaverbird.pipeline.steps.utils.validation.uppercase import validate_uppercase_step_columns
from weaverbird.pipeline.steps.utils.validation.waterfall import validate_waterfall_step_columns

__all__ = [
    "validate_step_columns",
    "MissingColumnError", 
    "StepValidationError"
]


def validate_step_columns(step: PipelineStep | PipelineStepWithVariables, available_columns: set[str]) -> None:
    """Validate that all columns referenced by the step exist in the dataset.
    
    Dispatches to specific validation functions based on the step type.
    
    Args:
        step: The pipeline step to validate
        available_columns: Set of column names available in the dataset
        
    Raises:
        StepValidationError: If any column referenced in the step doesn't exist in the dataset
        NotImplementedError: If no validator exists for the given step type
    """
    # Dispatch to specific validators based on step type
    if isinstance(step, AggregateStep | AggregateStepWithVariables):
        validate_aggregate_step_columns(step, available_columns)
    elif isinstance(step, AbsoluteValueStep | AbsoluteValueStepWithVariable):
        validate_absolute_value_step_columns(step, available_columns)
    elif isinstance(step, AddMissingDatesStep | AddMissingDatesStepWithVariables):
        validate_add_missing_dates_step_columns(step, available_columns)
    elif isinstance(step, ArgmaxStep | ArgmaxStepWithVariable):
        validate_argmax_step_columns(step, available_columns)
    elif isinstance(step, ArgminStep | ArgminStepWithVariable):
        validate_argmin_step_columns(step, available_columns)
    elif isinstance(step, CompareTextStep | CompareTextStepWithVariables):
        validate_compare_text_step_columns(step, available_columns)
    elif isinstance(step, ConcatenateStep | ConcatenateStepWithVariable):
        validate_concatenate_step_columns(step, available_columns)
    elif isinstance(step, ConvertStep):
        validate_convert_step_columns(step, available_columns)
    elif isinstance(step, CumSumStep | CumSumStepWithVariable):
        validate_cumsum_step_columns(step, available_columns)
    elif isinstance(step, DateExtractStep | DateExtractStepWithVariable):
        validate_date_extract_step_columns(step, available_columns)
    elif isinstance(step, DeleteStep):
        validate_delete_step_columns(step, available_columns)
    elif isinstance(step, DissolveStep):
        validate_dissolve_step_columns(step, available_columns)
    elif isinstance(step, DuplicateStep):
        validate_duplicate_step_columns(step, available_columns)
    elif isinstance(step, DurationStep | DurationStepWithVariable):
        validate_duration_step_columns(step, available_columns)
    elif isinstance(step, EvolutionStep | EvolutionStepWithVariable):
        validate_evolution_step_columns(step, available_columns)
    elif isinstance(step, FillnaStep | FillnaStepWithVariable):
        validate_fillna_step_columns(step, available_columns)
    elif isinstance(step, FilterStep | FilterStepWithVariables):
        validate_filter_step_columns(step, available_columns)
    elif isinstance(step, FormulaStep | FormulaStepWithVariable):
        validate_formula_step_columns(step, available_columns)
    elif isinstance(step, FromdateStep):
        validate_fromdate_step_columns(step, available_columns)
    elif isinstance(step, HierarchyStep):
        validate_hierarchy_step_columns(step, available_columns)
    elif isinstance(step, IfthenelseStep | IfThenElseStepWithVariables):
        validate_ifthenelse_step_columns(step, available_columns)
    elif isinstance(step, JoinStep | JoinStepWithVariable):
        validate_join_step_columns(step, available_columns)
    elif isinstance(step, LowercaseStep):
        validate_lowercase_step_columns(step, available_columns)
    elif isinstance(step, MovingAverageStep):
        validate_moving_average_step_columns(step, available_columns)
    elif isinstance(step, PercentageStep):
        validate_percentage_step_columns(step, available_columns)
    elif isinstance(step, PivotStep | PivotStepWithVariable):
        validate_pivot_step_columns(step, available_columns)
    elif isinstance(step, RankStep | RankStepWithVariable):
        validate_rank_step_columns(step, available_columns)
    elif isinstance(step, RenameStep | RenameStepWithVariable):
        validate_rename_step_columns(step, available_columns)
    elif isinstance(step, ReplaceStep | ReplaceStepWithVariable):
        validate_replace_step_columns(step, available_columns)
    elif isinstance(step, ReplaceTextStep | ReplaceTextStepWithVariable):
        validate_replacetext_step_columns(step, available_columns)
    elif isinstance(step, RollupStep | RollupStepWithVariable):
        validate_rollup_step_columns(step, available_columns)
    elif isinstance(step, SelectStep):
        validate_select_step_columns(step, available_columns)
    elif isinstance(step, SimplifyStep):
        validate_simplify_step_columns(step, available_columns)
    elif isinstance(step, SortStep):
        validate_sort_step_columns(step, available_columns)
    elif isinstance(step, SplitStep | SplitStepWithVariable):
        validate_split_step_columns(step, available_columns)
    elif isinstance(step, StatisticsStep):
        validate_statistics_step_columns(step, available_columns)
    elif isinstance(step, SubstringStep):
        validate_substring_step_columns(step, available_columns)
    elif isinstance(step, TextStep | TextStepWithVariable):
        validate_text_step_columns(step, available_columns)
    elif isinstance(step, ToDateStep):
        validate_todate_step_columns(step, available_columns)
    elif isinstance(step, TopStep | TopStepWithVariables):
        validate_top_step_columns(step, available_columns)
    elif isinstance(step, TotalsStep | TotalsStepWithVariable):
        validate_totals_step_columns(step, available_columns)
    elif isinstance(step, TrimStep):
        validate_trim_step_columns(step, available_columns)
    elif isinstance(step, UniqueGroupsStep | UniqueGroupsStepWithVariable):
        validate_uniquegroups_step_columns(step, available_columns)
    elif isinstance(step, UnpivotStep | UnpivotStepWithVariable):
        validate_unpivot_step_columns(step, available_columns)
    elif isinstance(step, UppercaseStep):
        validate_uppercase_step_columns(step, available_columns)
    elif isinstance(step, WaterfallStep | WaterfallStepWithVariable):
        validate_waterfall_step_columns(step, available_columns)
    else:
        raise NotImplementedError(f"No column validator implemented for step type: {step.name}")
from datetime import datetime
from enum import StrEnum
from typing import List

from pydantic import BaseModel, field_validator

from elluminate.schemas.base import BatchCreateStatus
from elluminate.schemas.criterion import Criterion
from elluminate.schemas.generation_metadata import GenerationMetadata


class RatingValue(StrEnum):
    YES = "YES"
    NO = "NO"
    INAPPLICABLE = "INAPPLICABLE"


class Rating(BaseModel):
    """Rating model."""

    id: int
    criterion: Criterion
    rating: RatingValue
    reasoning: str | None = None
    generation_metadata: GenerationMetadata | None = None
    created_at: datetime

    @field_validator("rating", mode="before")
    @classmethod
    def convert_bool_to_rating(cls, v):
        # TODO: Remove this once boolean ratings are fully deprecated.
        if isinstance(v, bool):
            return RatingValue.YES if v else RatingValue.NO
        return v


class RatingMode(StrEnum):
    """Enum for rating mode. In current implementation, only two modes are supported: fast mode is without reasoning and detailed mode is with reasoning."""

    FAST = "fast"
    DETAILED = "detailed"


class CreateRatingRequest(BaseModel):
    prompt_response_id: int
    rating_mode: RatingMode = RatingMode.FAST
    experiment_id: int | None = None


class BatchCreateRatingRequest(BaseModel):
    prompt_response_ids: list[int]
    rating_mode: RatingMode = RatingMode.FAST
    experiment_id: int | None = None


class BatchCreateRatingResponseStatus(BatchCreateStatus[List[Rating]]):
    pass

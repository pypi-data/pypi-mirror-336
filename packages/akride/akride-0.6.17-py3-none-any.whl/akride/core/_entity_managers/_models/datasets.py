from typing import Optional

from pydantic import BaseModel, field_validator

from akride import Constants
from akride.core.enums import DataType
from akride.core.exceptions import UserError


class SourceContainerData(BaseModel):
    id: str


class CreateDatasetIn(BaseModel):
    dataset_name: str
    dataset_namespace: str = "default"
    data_type: DataType = DataType.IMAGE
    glob_pattern: str = Constants.DEFAULT_IMAGE_BLOB_EXPR
    overwrite: bool = False
    sample_frame_rate: float = -1

    source_container_data: Optional[SourceContainerData] = None

    @field_validator("sample_frame_rate")
    @classmethod
    def validate_frame_rate(cls, v: float, values) -> float:
        data_type = values.data.get("data_type")

        if data_type == DataType.IMAGE and v != -1:
            raise UserError(
                message="Sample frame rate is not applicable for image datasets!",
            )
        return v

    @field_validator("glob_pattern")
    @classmethod
    def set_glob_pattern(cls, v: str, values) -> str:
        data_type = values.data.get("data_type")

        if (
            data_type == DataType.VIDEO
            and v == Constants.DEFAULT_IMAGE_BLOB_EXPR
        ):
            return Constants.DEFAULT_VIDEO_BLOB_EXPR
        return v

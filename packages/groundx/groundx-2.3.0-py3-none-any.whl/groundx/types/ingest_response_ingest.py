# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing_extensions
from ..core.serialization import FieldMetadata
from .processing_status import ProcessingStatus
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import typing
import pydantic


class IngestResponseIngest(UniversalBaseModel):
    process_id: typing_extensions.Annotated[str, FieldMetadata(alias="processId")]
    status: ProcessingStatus

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow

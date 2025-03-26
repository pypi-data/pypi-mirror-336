import pandera.typing
import pandera
import enum
from typing_extensions import TypeAlias

from pandera.api.base.types import StrictType


PDAIndex: TypeAlias = pandera.typing.Index
PDASeries: TypeAlias = pandera.typing.Series
PDADataFrame: TypeAlias = pandera.typing.DataFrame


def Field(*args, **kwargs):
    isin = kwargs.pop("isin", None)
    if isin is not None and issubclass(isin, enum.Enum):
        kwargs["isin"] = [e.value for e in isin]

    return pandera.Field(*args, **kwargs)


PDAField: TypeAlias = Field


class BaseConfig(pandera.api.pandas.model_config.BaseConfig):
    strict: StrictType = True
    coerce: bool = True
    ordered: bool = True
    unique_column_names = True

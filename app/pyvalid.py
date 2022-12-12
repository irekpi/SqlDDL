from typing import List, Optional

from pydantic import BaseModel, validator

default = {
    'SQLtypes': {'int', 'varchar', 'bigint', 'float', 'nvarchar', 'date', 'decimal', 'time', 'char', 'datetime2'},
}


class Bool(str):
    true = 'True'
    false = "False"


class SqlColumns(BaseModel):
    name: str
    type: Optional[str]
    size: Optional[str]
    references: Optional[str]
    unique: Optional[Bool]
    nullable: Optional[Bool]
    default: Optional[str]
    check: Optional[str]

    @validator('type')
    def check_type(cls, v):
        assert v in default['SQLtypes'], f'Incorrect SQL type for {v}'
        return v


class SqlDDL(BaseModel):
    table_name: str
    columns: List[SqlColumns]
    primary_key: Optional[List]

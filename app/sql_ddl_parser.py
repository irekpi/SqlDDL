from dataclasses import dataclass
from typing import Dict, List, Union

from simple_ddl_parser import DDLParser

unsafe_str = "SET ANSI_NULLS ON\nGO\nSET QUOTED_IDENTIFIER ON\nGO"


@dataclass
class SqlDDLParser:
    ddl_str: str
    output_mode: str = None

    def parse_data(self, ddl_str: str) -> Dict:
        try:
            incoming_data = ddl_str.replace(unsafe_str, '')
            data_dict = DDLParser(incoming_data).run(output_mode=self.output_mode)[0]
            return data_dict
        except Exception as e:
            print(f"{e} occurred. Data is not valid for parse")
            raise

    def get_data(self) -> Dict:
        data = self.parse_data(self.ddl_str)
        return self.clean_(data)

    def clean_(self, data: Dict) -> Dict:
        for item in data:
            data[item] = self.cleaner_factory(data.get(item))
        return data

    def cleaner_factory(self, data):
        if data:
            _map = {
                'str': self.clean_str,
                'list': self.clean_list,
                'dict': self.clean_dict,
                'bool': self.bool_int,
                'int': self.bool_int
            }
            return _map[type(data).__name__](data)

    def clean_str(self, data: str) -> str:
        return data.strip('[]')

    def clean_list(self, data: List) -> List:
        return [self.cleaner_factory(i) for i in data]

    def clean_dict(self, data: Dict) -> Dict:
        return {k: self.cleaner_factory(g) if isinstance(g, str) else g for k, g in data.items()}

    def bool_int(self, data: Union[bool, int]) -> Union[bool, int]:
        return data

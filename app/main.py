from app.pyvalid import SqlDDL
from app.sql_ddl_parser import SqlDDLParser
from fastapi import FastAPI, File

app = FastAPI()


@app.post("/sql_parse/")
@app.post("/sql_parse/{encoding}")
def sql_parse(file: bytes = File(), encoding: str = 'ascii'):
    file = crlf_to_lf(file).decode(encoding)
    data = SqlDDLParser(file).get_data()
    validated_data = SqlDDL(**data)

    return {'msg': validated_data}


def crlf_to_lf(byte_str):
    windows_line_ending = b'\r\n'
    unix_line_ending = b'\n'
    content = byte_str.replace(windows_line_ending, unix_line_ending)
    return content

from enum import Enum


class ReformatRequestOutputFormat(str, Enum):
    CSV = "CSV"
    HTML = "HTML"
    JSON = "JSON"
    MARKDOWN = "Markdown"
    STRING = "String"
    XML = "XML"
    YAML = "YAML"

    def __str__(self) -> str:
        return str(self.value)

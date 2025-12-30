import json
from rest_framework.parsers import BaseParser


class FormJSONParser(BaseParser):
    media_type = "application/x-www-form-urlencoded"

    def parse(self, stream, media_type=None, parser_context=None):
        raw = stream.read().decode("utf-8")
        if raw.startswith("{"):
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                return {}
        return {}

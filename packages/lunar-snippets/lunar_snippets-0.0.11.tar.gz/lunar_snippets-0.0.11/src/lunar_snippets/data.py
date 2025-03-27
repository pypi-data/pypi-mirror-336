from jsonpath_ng import parse
from pathlib import Path
import json
from typing import Any


class JsonPathExpression:
    def __init__(self, path: str):
        self.full_path = f"${path}"
        try:
            self._parsed = parse(self.full_path)
        except Exception as e:
            raise ValueError(f"Invalid JSON path: {path}") from e

    def find(self, payload: Any):
        return self._parsed.find(payload)


class SnippetData:
    def __init__(self, metadata_path: str):
        self.metadata_path = Path(metadata_path)

        if not self.metadata_path.is_absolute():
            raise ValueError("metadata_path must be an absolute path")

        with self.metadata_path.open() as f:
            self._data = json.load(f)

        # If optimal, could build a merged view for matching against if it
        # turns out to be the most common use case

    def get(self, query: JsonPathExpression):
        if not isinstance(query, JsonPathExpression):
            raise ValueError("query must be a JsonPathExpression")

        # Iterate through metadata instances in reverse order since the last
        # instance is the most recent
        for instance in reversed(self._data.get('metadata_instances', [])):
            # Get the payload for this instance
            payload = instance.get('payload', {})

            # Apply jsonpath query to payload
            matches = [match.value for match in query.find(payload)]
            if matches:
                # Return first match found
                # there should be only one per metadata instance
                return matches[0]

        # Return None if no matches found
        return None

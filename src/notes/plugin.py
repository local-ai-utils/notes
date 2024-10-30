from . import tools

def register(_, plugin_config):
    return {
        "name": "notes",
        "tools": tools,
        "functions": [
            {
                "name": "create",
                "description": "A simple note-taking endpoint. It accepts an array of categories for the note, and the text for the note. It is add-only, no update or delete options.",
                "strict": True,
                "parameters": {
                    "type": "object",
                    "required": [
                        "categories",
                        "note_text"
                    ],
                    "properties": {
                        "categories": {
                            "type": "array",
                            "description": "Array of categories for the note. Apply categories liberally, more is usually better. Names, places, topics, genres, and note type are all good categories.",
                            "items": {
                                "type": "string",
                                "description": "Category for the note"
                            }
                        },
                        "note_text": {
                            "type": "string",
                            "description": "Text content of the note"
                        }
                    },
                    "additionalProperties": False
                }
            }
        ]
    }

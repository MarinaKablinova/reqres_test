schema_user = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "email": {"type": "string"},
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "avatar": {"type": "string"}
        },
"required":["id", "email", "first_name", "last_name", "avatar"]
    }

schema_resource = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "name": {"type": "string"},
        "year": {"type": "number"},
        "color": {"type": "string"},
        "pantone_value": {"type": "string"}
        },
"required":["id", "name", "year", "color", "pantone_value"]
}

schema_new_user = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "job": {"type": "string"},
        "id": {"type": "string"},
        "createdAt": {"type": "string"},
        },
    "required":["name", "job", "id", "createdAt"]
    }

schema_update_user = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "job": {"type": "string"},
        "updatedAt": {"type": "string"},
        },
    "required":["name", "job", "updatedAt"]
    }

schema_update_user_part = {
    "type": "object",
    "properties": {
        "updatedAt": {"type": "string"},
        },
    "required":["updatedAt"]
    }
from bson import ObjectId


def validate_object_id(object_id: str) -> bool:
    if ObjectId.is_valid(object_id) is False:
        raise ValueError("Invalid book ID")
    return ObjectId(object_id)

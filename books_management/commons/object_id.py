from bson import ObjectId


def validate_object_id(object_id: str) -> bool:
    """
    Validate if the object ID is valid, return the object ID if it is valid, otherwise raise a ValueError.
    :param object_id: str
    :return: ObjectId
    """
    if ObjectId.is_valid(object_id) is False:
        raise ValueError("Invalid book ID")
    return ObjectId(object_id)

from datetime import datetime, timezone

from bson import ObjectId


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def to_object_id(id_value: str) -> ObjectId:
    return ObjectId(id_value)


def normalize_doc(document: dict) -> dict:
    if not document:
        return document
    document["_id"] = str(document["_id"])
    return document

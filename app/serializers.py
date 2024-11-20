from marshmallow import Schema, fields
from app.models import User, URL, Visit

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    urls = fields.Nested('URLSchema', many=True, exclude=('user',))  # Avoid circular references

class URLSchema(Schema):
    id = fields.Int(dump_only=True)
    original_url = fields.Str(required=True)
    short_url = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    visits = fields.Nested('VisitSchema', many=True, exclude=('url',))

class VisitSchema(Schema):
    id = fields.Int(dump_only=True)
    timestamp = fields.DateTime(dump_only=True)
    user_agent = fields.Str()
    ip_address = fields.Str()

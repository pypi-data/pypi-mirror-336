import typing

from marshmallow import fields
from marshmallow_dataclass.union_field import Union as MdUnion
from marshmallow_jsonschema import JSONSchema
from marshmallow_jsonschema.base import FIELD_VALIDATORS

try:
    from marshmallow_union import Union

    ALLOW_UNIONS = True
except ImportError:
    ALLOW_UNIONS = False

try:
    from marshmallow_enum import EnumField, LoadDumpOptions

    ALLOW_ENUMS = True
except ImportError:
    ALLOW_ENUMS = False


class JSONSchemaWithUnion(JSONSchema):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def _from_union_schema(self, obj, field) -> typing.Dict[str, typing.List[typing.Any]]:
        """Get a union type schema. Uses anyOf to allow the value to be any of the provided sub fields"""
        if isinstance(field, Union):

            return {
                "anyOf": [
                    self._get_schema_for_field(obj, sub_field)
                    for sub_field in field._candidate_fields
                ]
            }
        elif isinstance(field, MdUnion):
            return {
                "anyOf": [
                    self._get_schema_for_field(obj, sub_field)
                    for _, sub_field in field.union_fields
                ]
            }

    def _get_schema_for_field(self, obj, field):
        """Get schema and validators for field."""
        if hasattr(field, "_jsonschema_type_mapping"):
            schema = field._jsonschema_type_mapping()
        elif "_jsonschema_type_mapping" in field.metadata:
            schema = field.metadata["_jsonschema_type_mapping"]
        else:
            if isinstance(field, fields.Nested):
                # Special treatment for nested fields.
                schema = self._from_nested_schema(obj, field)
            elif ALLOW_UNIONS and isinstance(field, Union) or isinstance(field, MdUnion):
                schema = self._from_union_schema(obj, field)
            else:
                pytype = self._get_python_type(field)
                schema = self._from_python_type(obj, field, pytype)
        # Apply any and all validators that field may have
        for validator in field.validators:
            if validator.__class__ in FIELD_VALIDATORS:
                schema = FIELD_VALIDATORS[validator.__class__](
                    schema, field, validator, obj
                )
            else:
                base_class = getattr(
                    validator, "_jsonschema_base_validator_class", None
                )
                if base_class is not None and base_class in FIELD_VALIDATORS:
                    schema = FIELD_VALIDATORS[base_class](schema, field, validator, obj)
        return schema

# Copyright (c) 2022-2023 Geosiris.
# SPDX-License-Identifier: Apache-2.0
# -*- coding: utf-8 -*-

""" avro python class for file: data_value """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


from etptypes.energistics.etp.v12.datatypes.array_of_boolean import (
    ArrayOfBoolean,
)

from etptypes.energistics.etp.v12.datatypes.array_of_nullable_boolean import (
    ArrayOfNullableBoolean,
)

from etptypes.energistics.etp.v12.datatypes.array_of_int import ArrayOfInt

from etptypes.energistics.etp.v12.datatypes.array_of_nullable_int import (
    ArrayOfNullableInt,
)

from etptypes.energistics.etp.v12.datatypes.array_of_long import ArrayOfLong

from etptypes.energistics.etp.v12.datatypes.array_of_nullable_long import (
    ArrayOfNullableLong,
)

from etptypes.energistics.etp.v12.datatypes.array_of_float import ArrayOfFloat

from etptypes.energistics.etp.v12.datatypes.array_of_double import (
    ArrayOfDouble,
)

from etptypes.energistics.etp.v12.datatypes.array_of_string import (
    ArrayOfString,
)

from etptypes.energistics.etp.v12.datatypes.array_of_bytes import ArrayOfBytes

from etptypes.energistics.etp.v12.datatypes.any_sparse_array import (
    AnySparseArray,
)


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "DataValue", "fields": [{"name": "item", "type": ["null", "boolean", "int", "long", "float", "double", "string", {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfBoolean", "fields": [{"name": "values", "type": {"type": "array", "items": "boolean"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfBoolean", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfNullableBoolean", "fields": [{"name": "values", "type": {"type": "array", "items": ["null", "boolean"]}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfNullableBoolean", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfInt", "fields": [{"name": "values", "type": {"type": "array", "items": "int"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfInt", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfNullableInt", "fields": [{"name": "values", "type": {"type": "array", "items": ["null", "int"]}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfNullableInt", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfLong", "fields": [{"name": "values", "type": {"type": "array", "items": "long"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfLong", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfNullableLong", "fields": [{"name": "values", "type": {"type": "array", "items": ["null", "long"]}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfNullableLong", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfFloat", "fields": [{"name": "values", "type": {"type": "array", "items": "float"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfFloat", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfDouble", "fields": [{"name": "values", "type": {"type": "array", "items": "double"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfDouble", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfString", "fields": [{"name": "values", "type": {"type": "array", "items": "string"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfString", "depends": []}, {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "ArrayOfBytes", "fields": [{"name": "values", "type": {"type": "array", "items": "bytes"}}], "fullName": "Energistics.Etp.v12.Datatypes.ArrayOfBytes", "depends": []}, "bytes", {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "AnySparseArray", "fields": [{"name": "slices", "type": {"type": "array", "items": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "AnySubarray", "fields": [{"name": "start", "type": "long"}, {"name": "slice", "type": {"type": "record", "namespace": "Energistics.Etp.v12.Datatypes", "name": "AnyArray", "fields": [{"name": "item", "type": ["Energistics.Etp.v12.Datatypes.ArrayOfBoolean", "Energistics.Etp.v12.Datatypes.ArrayOfInt", "Energistics.Etp.v12.Datatypes.ArrayOfLong", "Energistics.Etp.v12.Datatypes.ArrayOfFloat", "Energistics.Etp.v12.Datatypes.ArrayOfDouble", "Energistics.Etp.v12.Datatypes.ArrayOfString", "bytes"]}], "fullName": "Energistics.Etp.v12.Datatypes.AnyArray", "depends": ["Energistics.Etp.v12.Datatypes.ArrayOfBoolean", "Energistics.Etp.v12.Datatypes.ArrayOfInt", "Energistics.Etp.v12.Datatypes.ArrayOfLong", "Energistics.Etp.v12.Datatypes.ArrayOfFloat", "Energistics.Etp.v12.Datatypes.ArrayOfDouble", "Energistics.Etp.v12.Datatypes.ArrayOfString"]}}], "fullName": "Energistics.Etp.v12.Datatypes.AnySubarray", "depends": ["Energistics.Etp.v12.Datatypes.AnyArray"]}}}], "fullName": "Energistics.Etp.v12.Datatypes.AnySparseArray", "depends": ["Energistics.Etp.v12.Datatypes.AnySubarray"]}]}], "fullName": "Energistics.Etp.v12.Datatypes.DataValue", "depends": ["Energistics.Etp.v12.Datatypes.ArrayOfBoolean", "Energistics.Etp.v12.Datatypes.ArrayOfNullableBoolean", "Energistics.Etp.v12.Datatypes.ArrayOfInt", "Energistics.Etp.v12.Datatypes.ArrayOfNullableInt", "Energistics.Etp.v12.Datatypes.ArrayOfLong", "Energistics.Etp.v12.Datatypes.ArrayOfNullableLong", "Energistics.Etp.v12.Datatypes.ArrayOfFloat", "Energistics.Etp.v12.Datatypes.ArrayOfDouble", "Energistics.Etp.v12.Datatypes.ArrayOfString", "Energistics.Etp.v12.Datatypes.ArrayOfBytes", "Energistics.Etp.v12.Datatypes.AnySparseArray"]}'


class DataValue(ETPModel):

    item: typing.Optional[
        typing.Union[
            Strict[bool],
            Strict[int],
            Strict[int],
            Strict[float],
            Strict[float],
            Strict[str],
            ArrayOfBoolean,
            ArrayOfNullableBoolean,
            ArrayOfInt,
            ArrayOfNullableInt,
            ArrayOfLong,
            ArrayOfNullableLong,
            ArrayOfFloat,
            ArrayOfDouble,
            ArrayOfString,
            ArrayOfBytes,
            Strict[bytes],
            AnySparseArray,
        ]
    ] = Field(alias="item")

    def dict(self, *args, **kwargs) -> dict[str, object]:
        if isinstance(self.item, ArrayOfBoolean):
            return {
                "item": (
                    "Energistics.Etp.v12.Datatypes.ArrayOfBoolean",
                    {"values": self.item.values},
                )
            }
        elif isinstance(self.item, ArrayOfNullableBoolean):
            return {
                "item": (
                    "Energistics.Etp.v12.Datatypes.ArrayOfNullableBoolean",
                    {"values": self.item.values},
                )
            }
        elif isinstance(self.item, ArrayOfInt):
            return {
                "item": (
                    "Energistics.Etp.v12.Datatypes.ArrayOfInt",
                    {"values": self.item.values},
                )
            }
        elif isinstance(self.item, ArrayOfNullableInt):
            return {
                "item": (
                    "Energistics.Etp.v12.Datatypes.ArrayOfNullableInt",
                    {"values": self.item.values},
                )
            }
        elif isinstance(self.item, ArrayOfLong):
            return {
                "item": (
                    "Energistics.Etp.v12.Datatypes.ArrayOfLong",
                    {"values": self.item.values},
                )
            }
        elif isinstance(self.item, ArrayOfNullableLong):
            return {
                "item": (
                    "Energistics.Etp.v12.Datatypes.ArrayOfNullableLong",
                    {"values": self.item.values},
                )
            }
        elif isinstance(self.item, ArrayOfFloat):
            return {
                "item": (
                    "Energistics.Etp.v12.Datatypes.ArrayOfFloat",
                    {"values": self.item.values},
                )
            }
        elif isinstance(self.item, ArrayOfDouble):
            return {
                "item": (
                    "Energistics.Etp.v12.Datatypes.ArrayOfDouble",
                    {"values": self.item.values},
                )
            }
        elif isinstance(self.item, ArrayOfString):
            return {
                "item": (
                    "Energistics.Etp.v12.Datatypes.ArrayOfString",
                    {"values": self.item.values},
                )
            }
        elif isinstance(self.item, ArrayOfBytes):
            return {
                "item": (
                    "Energistics.Etp.v12.Datatypes.ArrayOfBytes",
                    {"values": self.item.values},
                )
            }
        else:
            return super().dict(*args, **kwargs)

    @validator("item", pre=True, always=True)
    def validate_item_type(cls, v):
        if isinstance(v, (tuple, list)):
            if v[0].endswith("ArrayOfBoolean"):
                return ArrayOfBoolean.construct(values=v[1]["values"])
            elif v[0].endswith("ArrayOfNullableBoolean"):
                return ArrayOfNullableBoolean.construct(values=v[1]["values"])
            elif v[0].endswith("ArrayOfInt"):
                return ArrayOfInt.construct(values=v[1]["values"])
            elif v[0].endswith("ArrayOfNullableInt"):
                return ArrayOfNullableInt.construct(values=v[1]["values"])
            elif v[0].endswith("ArrayOfLong"):
                return ArrayOfLong.construct(values=v[1]["values"])
            elif v[0].endswith("ArrayOfNullableLong"):
                return ArrayOfNullableLong.construct(values=v[1]["values"])
            elif v[0].endswith("ArrayOfFloat"):
                return ArrayOfFloat.construct(values=v[1]["values"])
            elif v[0].endswith("ArrayOfDouble"):
                return ArrayOfDouble.construct(values=v[1]["values"])
            elif v[0].endswith("ArrayOfString"):
                return ArrayOfString.construct(values=v[1]["values"])
            elif v[0].endswith("ArrayOfBytes"):
                return ArrayOfBytes.construct(values=v[1]["values"])
        return v

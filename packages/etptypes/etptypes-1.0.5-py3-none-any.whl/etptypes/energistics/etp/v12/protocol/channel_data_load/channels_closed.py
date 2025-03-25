# Copyright (c) 2022-2023 Geosiris.
# SPDX-License-Identifier: Apache-2.0
# -*- coding: utf-8 -*-

""" avro python class for file: channels_closed """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.ChannelDataLoad", "name": "ChannelsClosed", "protocol": "22", "messageType": "7", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": true, "fields": [{"name": "reason", "type": "string"}, {"name": "id", "type": {"type": "map", "values": "long"}}], "fullName": "Energistics.Etp.v12.Protocol.ChannelDataLoad.ChannelsClosed", "depends": []}'


class ChannelsClosed(ETPModel):

    reason: str = Field(alias="reason")

    id_: typing.Mapping[str, int] = Field(alias="id")

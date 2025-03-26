# Copyright (c) 2022-2023 Geosiris.
# SPDX-License-Identifier: Apache-2.0
# -*- coding: utf-8 -*-

""" avro python class for file: replace_range_response """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.Protocol.ChannelDataLoad", "name": "ReplaceRangeResponse", "protocol": "22", "messageType": "8", "senderRole": "store", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [{"name": "channelChangeTime", "type": "long"}], "fullName": "Energistics.Etp.v12.Protocol.ChannelDataLoad.ReplaceRangeResponse", "depends": []}'


class ReplaceRangeResponse(ETPModel):

    channel_change_time: int = Field(alias="channelChangeTime")

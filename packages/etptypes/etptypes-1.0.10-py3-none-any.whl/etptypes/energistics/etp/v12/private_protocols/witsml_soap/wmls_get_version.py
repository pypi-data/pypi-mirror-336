# Copyright (c) 2022-2023 Geosiris.
# SPDX-License-Identifier: Apache-2.0
# -*- coding: utf-8 -*-

""" avro python class for file: wmls_get_version """

import typing
from pydantic import validator
from etptypes import ETPModel, Field, Strict


avro_schema: typing.Final[
    str
] = '{"type": "record", "namespace": "Energistics.Etp.v12.PrivateProtocols.WitsmlSoap", "name": "WMLS_GetVersion", "protocol": "2100", "messageType": "11", "senderRole": "customer", "protocolRoles": "store,customer", "multipartFlag": false, "fields": [], "fullName": "Energistics.Etp.v12.PrivateProtocols.WitsmlSoap.WMLS_GetVersion", "depends": []}'


class WMLS_GetVersion(ETPModel):
    pass

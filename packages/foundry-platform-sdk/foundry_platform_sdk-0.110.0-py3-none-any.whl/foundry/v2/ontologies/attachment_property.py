#  Copyright 2024 Palantir Technologies, Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


import typing
import warnings

import pydantic
import typing_extensions

from foundry import _core as core
from foundry import _errors as errors
from foundry.v2.ontologies import models as ontologies_models


class AttachmentPropertyClient:
    """
    The API client for the AttachmentProperty Resource.

    :param auth: Your auth configuration.
    :param hostname: Your Foundry hostname (for example, "myfoundry.palantirfoundry.com"). This can also include your API gateway service URI.
    :param config: Optionally specify the configuration for the HTTP session.
    """

    def __init__(
        self,
        auth: core.Auth,
        hostname: str,
        config: typing.Optional[core.Config] = None,
    ):
        self._auth = auth
        self._hostname = hostname
        self._config = config
        self._api_client = core.ApiClient(auth=auth, hostname=hostname, config=config)

        self.with_streaming_response = _AttachmentPropertyClientStreaming(self)
        self.with_raw_response = _AttachmentPropertyClientRaw(self)

    @core.maybe_ignore_preview
    @pydantic.validate_call
    @errors.handle_unexpected
    def get_attachment(
        self,
        ontology: ontologies_models.OntologyIdentifier,
        object_type: ontologies_models.ObjectTypeApiName,
        primary_key: ontologies_models.PropertyValueEscapedString,
        property: ontologies_models.PropertyApiName,
        *,
        artifact_repository: typing.Optional[ontologies_models.ArtifactRepositoryRid] = None,
        package_name: typing.Optional[ontologies_models.SdkPackageName] = None,
        request_timeout: typing.Optional[core.Timeout] = None,
        _sdk_internal: core.SdkInternal = {},
    ) -> ontologies_models.AttachmentMetadataResponse:
        """
        Get the metadata of attachments parented to the given object.

        Third-party applications using this endpoint via OAuth2 must request the
        following operation scopes: `api:ontologies-read`.

        :param ontology: The API name of the ontology. To find the API name, use the **List ontologies** endpoint or check the **Ontology Manager**.
        :type ontology: OntologyIdentifier
        :param object_type: The API name of the object type. To find the API name, use the **List object types** endpoint or check the **Ontology Manager**.
        :type object_type: ObjectTypeApiName
        :param primary_key: The primary key of the object containing the attachment.
        :type primary_key: PropertyValueEscapedString
        :param property: The API name of the attachment property. To find the API name for your attachment, check the **Ontology Manager** or use the **Get object type** endpoint.
        :type property: PropertyApiName
        :param artifact_repository: The repository associated with a marketplace installation.
        :type artifact_repository: Optional[ArtifactRepositoryRid]
        :param package_name: The package name of the generated SDK.
        :type package_name: Optional[SdkPackageName]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: ontologies_models.AttachmentMetadataResponse
        """

        return self._api_client.call_api(
            core.RequestInfo(
                method="GET",
                resource_path="/v2/ontologies/{ontology}/objects/{objectType}/{primaryKey}/attachments/{property}",
                query_params={
                    "artifactRepository": artifact_repository,
                    "packageName": package_name,
                },
                path_params={
                    "ontology": ontology,
                    "objectType": object_type,
                    "primaryKey": primary_key,
                    "property": property,
                },
                header_params={
                    "Accept": "application/json",
                },
                body=None,
                body_type=None,
                response_type=ontologies_models.AttachmentMetadataResponse,
                request_timeout=request_timeout,
                throwable_errors={},
                response_mode=_sdk_internal.get("response_mode"),
            ),
        )

    @core.maybe_ignore_preview
    @pydantic.validate_call
    @errors.handle_unexpected
    def get_attachment_by_rid(
        self,
        ontology: ontologies_models.OntologyIdentifier,
        object_type: ontologies_models.ObjectTypeApiName,
        primary_key: ontologies_models.PropertyValueEscapedString,
        property: ontologies_models.PropertyApiName,
        attachment_rid: ontologies_models.AttachmentRid,
        *,
        artifact_repository: typing.Optional[ontologies_models.ArtifactRepositoryRid] = None,
        package_name: typing.Optional[ontologies_models.SdkPackageName] = None,
        request_timeout: typing.Optional[core.Timeout] = None,
        _sdk_internal: core.SdkInternal = {},
    ) -> ontologies_models.AttachmentV2:
        """
        Get the metadata of a particular attachment in an attachment list.

        Third-party applications using this endpoint via OAuth2 must request the
        following operation scopes: `api:ontologies-read`.

        :param ontology: The API name of the ontology. To find the API name, use the **List ontologies** endpoint or check the **Ontology Manager**.
        :type ontology: OntologyIdentifier
        :param object_type: The API name of the object type. To find the API name, use the **List object types** endpoint or check the **Ontology Manager**.
        :type object_type: ObjectTypeApiName
        :param primary_key: The primary key of the object containing the attachment.
        :type primary_key: PropertyValueEscapedString
        :param property: The API name of the attachment property. To find the API name for your attachment, check the **Ontology Manager** or use the **Get object type** endpoint.
        :type property: PropertyApiName
        :param attachment_rid: The RID of the attachment.
        :type attachment_rid: AttachmentRid
        :param artifact_repository: The repository associated with a marketplace installation.
        :type artifact_repository: Optional[ArtifactRepositoryRid]
        :param package_name: The package name of the generated SDK.
        :type package_name: Optional[SdkPackageName]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: ontologies_models.AttachmentV2
        """

        return self._api_client.call_api(
            core.RequestInfo(
                method="GET",
                resource_path="/v2/ontologies/{ontology}/objects/{objectType}/{primaryKey}/attachments/{property}/{attachmentRid}",
                query_params={
                    "artifactRepository": artifact_repository,
                    "packageName": package_name,
                },
                path_params={
                    "ontology": ontology,
                    "objectType": object_type,
                    "primaryKey": primary_key,
                    "property": property,
                    "attachmentRid": attachment_rid,
                },
                header_params={
                    "Accept": "application/json",
                },
                body=None,
                body_type=None,
                response_type=ontologies_models.AttachmentV2,
                request_timeout=request_timeout,
                throwable_errors={},
                response_mode=_sdk_internal.get("response_mode"),
            ),
        )

    @typing_extensions.overload
    @typing_extensions.deprecated(
        "Using the `stream` parameter is deprecated. Please use the `with_streaming_response` instead."
    )
    def read_attachment(
        self,
        ontology: ontologies_models.OntologyIdentifier,
        object_type: ontologies_models.ObjectTypeApiName,
        primary_key: ontologies_models.PropertyValueEscapedString,
        property: ontologies_models.PropertyApiName,
        *,
        stream: typing.Literal[True],
        artifact_repository: typing.Optional[ontologies_models.ArtifactRepositoryRid] = None,
        package_name: typing.Optional[ontologies_models.SdkPackageName] = None,
        chunk_size: typing.Optional[int] = None,
        request_timeout: typing.Optional[core.Timeout] = None,
        _sdk_internal: core.SdkInternal = {},
    ) -> core.BinaryStream:
        """
        Get the content of an attachment.

        Third-party applications using this endpoint via OAuth2 must request the
        following operation scopes: `api:ontologies-read`.

        :param ontology: The API name of the ontology. To find the API name, use the **List ontologies** endpoint or check the **Ontology Manager**.
        :type ontology: OntologyIdentifier
        :param object_type: The API name of the object type. To find the API name, use the **List object types** endpoint or check the **Ontology Manager**.
        :type object_type: ObjectTypeApiName
        :param primary_key: The primary key of the object containing the attachment.
        :type primary_key: PropertyValueEscapedString
        :param property: The API name of the attachment property. To find the API name for your attachment, check the **Ontology Manager** or use the **Get object type** endpoint.
        :type property: PropertyApiName
        :param artifact_repository: The repository associated with a marketplace installation.
        :type artifact_repository: Optional[ArtifactRepositoryRid]
        :param package_name: The package name of the generated SDK.
        :type package_name: Optional[SdkPackageName]
        :param stream: Whether to stream back the binary data in an iterator. This avoids reading the entire content of the response into memory at once.
        :type stream: bool
        :param chunk_size: The number of bytes that should be read into memory for each chunk. If set to None, the data will become available as it arrives in whatever size is sent from the host.
        :type chunk_size: Optional[int]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: core.BinaryStream
        """
        ...

    @typing_extensions.overload
    def read_attachment(
        self,
        ontology: ontologies_models.OntologyIdentifier,
        object_type: ontologies_models.ObjectTypeApiName,
        primary_key: ontologies_models.PropertyValueEscapedString,
        property: ontologies_models.PropertyApiName,
        *,
        artifact_repository: typing.Optional[ontologies_models.ArtifactRepositoryRid] = None,
        package_name: typing.Optional[ontologies_models.SdkPackageName] = None,
        stream: typing.Literal[False] = False,
        request_timeout: typing.Optional[core.Timeout] = None,
        _sdk_internal: core.SdkInternal = {},
    ) -> bytes:
        """
        Get the content of an attachment.

        Third-party applications using this endpoint via OAuth2 must request the
        following operation scopes: `api:ontologies-read`.

        :param ontology: The API name of the ontology. To find the API name, use the **List ontologies** endpoint or check the **Ontology Manager**.
        :type ontology: OntologyIdentifier
        :param object_type: The API name of the object type. To find the API name, use the **List object types** endpoint or check the **Ontology Manager**.
        :type object_type: ObjectTypeApiName
        :param primary_key: The primary key of the object containing the attachment.
        :type primary_key: PropertyValueEscapedString
        :param property: The API name of the attachment property. To find the API name for your attachment, check the **Ontology Manager** or use the **Get object type** endpoint.
        :type property: PropertyApiName
        :param artifact_repository: The repository associated with a marketplace installation.
        :type artifact_repository: Optional[ArtifactRepositoryRid]
        :param package_name: The package name of the generated SDK.
        :type package_name: Optional[SdkPackageName]
        :param stream: Whether to stream back the binary data in an iterator. This avoids reading the entire content of the response into memory at once.
        :type stream: bool
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: bytes
        """
        ...

    @typing_extensions.overload
    @typing_extensions.deprecated(
        "Using the `stream` parameter is deprecated. Please use the `with_streaming_response` instead."
    )
    def read_attachment(
        self,
        ontology: ontologies_models.OntologyIdentifier,
        object_type: ontologies_models.ObjectTypeApiName,
        primary_key: ontologies_models.PropertyValueEscapedString,
        property: ontologies_models.PropertyApiName,
        *,
        stream: bool,
        artifact_repository: typing.Optional[ontologies_models.ArtifactRepositoryRid] = None,
        package_name: typing.Optional[ontologies_models.SdkPackageName] = None,
        chunk_size: typing.Optional[int] = None,
        request_timeout: typing.Optional[core.Timeout] = None,
        _sdk_internal: core.SdkInternal = {},
    ) -> typing.Union[bytes, core.BinaryStream]:
        """
        Get the content of an attachment.

        Third-party applications using this endpoint via OAuth2 must request the
        following operation scopes: `api:ontologies-read`.

        :param ontology: The API name of the ontology. To find the API name, use the **List ontologies** endpoint or check the **Ontology Manager**.
        :type ontology: OntologyIdentifier
        :param object_type: The API name of the object type. To find the API name, use the **List object types** endpoint or check the **Ontology Manager**.
        :type object_type: ObjectTypeApiName
        :param primary_key: The primary key of the object containing the attachment.
        :type primary_key: PropertyValueEscapedString
        :param property: The API name of the attachment property. To find the API name for your attachment, check the **Ontology Manager** or use the **Get object type** endpoint.
        :type property: PropertyApiName
        :param artifact_repository: The repository associated with a marketplace installation.
        :type artifact_repository: Optional[ArtifactRepositoryRid]
        :param package_name: The package name of the generated SDK.
        :type package_name: Optional[SdkPackageName]
        :param stream: Whether to stream back the binary data in an iterator. This avoids reading the entire content of the response into memory at once.
        :type stream: bool
        :param chunk_size: The number of bytes that should be read into memory for each chunk. If set to None, the data will become available as it arrives in whatever size is sent from the host.
        :type chunk_size: Optional[int]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: typing.Union[bytes, core.BinaryStream]
        """
        ...

    @core.maybe_ignore_preview
    @pydantic.validate_call
    @errors.handle_unexpected
    def read_attachment(
        self,
        ontology: ontologies_models.OntologyIdentifier,
        object_type: ontologies_models.ObjectTypeApiName,
        primary_key: ontologies_models.PropertyValueEscapedString,
        property: ontologies_models.PropertyApiName,
        *,
        artifact_repository: typing.Optional[ontologies_models.ArtifactRepositoryRid] = None,
        package_name: typing.Optional[ontologies_models.SdkPackageName] = None,
        stream: bool = False,
        chunk_size: typing.Optional[int] = None,
        request_timeout: typing.Optional[core.Timeout] = None,
        _sdk_internal: core.SdkInternal = {},
    ) -> typing.Union[bytes, core.BinaryStream]:
        """
        Get the content of an attachment.

        Third-party applications using this endpoint via OAuth2 must request the
        following operation scopes: `api:ontologies-read`.

        :param ontology: The API name of the ontology. To find the API name, use the **List ontologies** endpoint or check the **Ontology Manager**.
        :type ontology: OntologyIdentifier
        :param object_type: The API name of the object type. To find the API name, use the **List object types** endpoint or check the **Ontology Manager**.
        :type object_type: ObjectTypeApiName
        :param primary_key: The primary key of the object containing the attachment.
        :type primary_key: PropertyValueEscapedString
        :param property: The API name of the attachment property. To find the API name for your attachment, check the **Ontology Manager** or use the **Get object type** endpoint.
        :type property: PropertyApiName
        :param artifact_repository: The repository associated with a marketplace installation.
        :type artifact_repository: Optional[ArtifactRepositoryRid]
        :param package_name: The package name of the generated SDK.
        :type package_name: Optional[SdkPackageName]
        :param stream: Whether to stream back the binary data in an iterator. This avoids reading the entire content of the response into memory at once.
        :type stream: bool
        :param chunk_size: The number of bytes that should be read into memory for each chunk. If set to None, the data will become available as it arrives in whatever size is sent from the host.
        :type chunk_size: Optional[int]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: typing.Union[bytes, core.BinaryStream]
        """

        if stream:
            warnings.warn(
                f"client.ontologies.AttachmentProperty.read_attachment(..., stream=True, chunk_size={chunk_size}) is deprecated. Please use:\n\nwith client.ontologies.AttachmentProperty.with_streaming_response.read_attachment(...) as response:\n    response.iter_bytes(chunk_size={chunk_size})\n",
                DeprecationWarning,
                stacklevel=2,
            )

        return self._api_client.call_api(
            core.RequestInfo(
                method="GET",
                resource_path="/v2/ontologies/{ontology}/objects/{objectType}/{primaryKey}/attachments/{property}/content",
                query_params={
                    "artifactRepository": artifact_repository,
                    "packageName": package_name,
                },
                path_params={
                    "ontology": ontology,
                    "objectType": object_type,
                    "primaryKey": primary_key,
                    "property": property,
                },
                header_params={
                    "Accept": "*/*",
                },
                body=None,
                body_type=None,
                response_type=bytes,
                stream=stream,
                chunk_size=chunk_size,
                request_timeout=request_timeout,
                throwable_errors={},
                response_mode=_sdk_internal.get("response_mode"),
            ),
        )

    @typing_extensions.overload
    @typing_extensions.deprecated(
        "Using the `stream` parameter is deprecated. Please use the `with_streaming_response` instead."
    )
    def read_attachment_by_rid(
        self,
        ontology: ontologies_models.OntologyIdentifier,
        object_type: ontologies_models.ObjectTypeApiName,
        primary_key: ontologies_models.PropertyValueEscapedString,
        property: ontologies_models.PropertyApiName,
        attachment_rid: ontologies_models.AttachmentRid,
        *,
        stream: typing.Literal[True],
        artifact_repository: typing.Optional[ontologies_models.ArtifactRepositoryRid] = None,
        package_name: typing.Optional[ontologies_models.SdkPackageName] = None,
        chunk_size: typing.Optional[int] = None,
        request_timeout: typing.Optional[core.Timeout] = None,
        _sdk_internal: core.SdkInternal = {},
    ) -> core.BinaryStream:
        """
        Get the content of an attachment by its RID.

        The RID must exist in the attachment array of the property.

        Third-party applications using this endpoint via OAuth2 must request the
        following operation scopes: `api:ontologies-read`.

        :param ontology: The API name of the ontology. To find the API name, use the **List ontologies** endpoint or check the **Ontology Manager**.
        :type ontology: OntologyIdentifier
        :param object_type: The API name of the object type. To find the API name, use the **List object types** endpoint or check the **Ontology Manager**.
        :type object_type: ObjectTypeApiName
        :param primary_key: The primary key of the object containing the attachment.
        :type primary_key: PropertyValueEscapedString
        :param property: The API name of the attachment property. To find the API name for your attachment, check the **Ontology Manager** or use the **Get object type** endpoint.
        :type property: PropertyApiName
        :param attachment_rid: The RID of the attachment.
        :type attachment_rid: AttachmentRid
        :param artifact_repository: The repository associated with a marketplace installation.
        :type artifact_repository: Optional[ArtifactRepositoryRid]
        :param package_name: The package name of the generated SDK.
        :type package_name: Optional[SdkPackageName]
        :param stream: Whether to stream back the binary data in an iterator. This avoids reading the entire content of the response into memory at once.
        :type stream: bool
        :param chunk_size: The number of bytes that should be read into memory for each chunk. If set to None, the data will become available as it arrives in whatever size is sent from the host.
        :type chunk_size: Optional[int]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: core.BinaryStream
        """
        ...

    @typing_extensions.overload
    def read_attachment_by_rid(
        self,
        ontology: ontologies_models.OntologyIdentifier,
        object_type: ontologies_models.ObjectTypeApiName,
        primary_key: ontologies_models.PropertyValueEscapedString,
        property: ontologies_models.PropertyApiName,
        attachment_rid: ontologies_models.AttachmentRid,
        *,
        artifact_repository: typing.Optional[ontologies_models.ArtifactRepositoryRid] = None,
        package_name: typing.Optional[ontologies_models.SdkPackageName] = None,
        stream: typing.Literal[False] = False,
        request_timeout: typing.Optional[core.Timeout] = None,
        _sdk_internal: core.SdkInternal = {},
    ) -> bytes:
        """
        Get the content of an attachment by its RID.

        The RID must exist in the attachment array of the property.

        Third-party applications using this endpoint via OAuth2 must request the
        following operation scopes: `api:ontologies-read`.

        :param ontology: The API name of the ontology. To find the API name, use the **List ontologies** endpoint or check the **Ontology Manager**.
        :type ontology: OntologyIdentifier
        :param object_type: The API name of the object type. To find the API name, use the **List object types** endpoint or check the **Ontology Manager**.
        :type object_type: ObjectTypeApiName
        :param primary_key: The primary key of the object containing the attachment.
        :type primary_key: PropertyValueEscapedString
        :param property: The API name of the attachment property. To find the API name for your attachment, check the **Ontology Manager** or use the **Get object type** endpoint.
        :type property: PropertyApiName
        :param attachment_rid: The RID of the attachment.
        :type attachment_rid: AttachmentRid
        :param artifact_repository: The repository associated with a marketplace installation.
        :type artifact_repository: Optional[ArtifactRepositoryRid]
        :param package_name: The package name of the generated SDK.
        :type package_name: Optional[SdkPackageName]
        :param stream: Whether to stream back the binary data in an iterator. This avoids reading the entire content of the response into memory at once.
        :type stream: bool
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: bytes
        """
        ...

    @typing_extensions.overload
    @typing_extensions.deprecated(
        "Using the `stream` parameter is deprecated. Please use the `with_streaming_response` instead."
    )
    def read_attachment_by_rid(
        self,
        ontology: ontologies_models.OntologyIdentifier,
        object_type: ontologies_models.ObjectTypeApiName,
        primary_key: ontologies_models.PropertyValueEscapedString,
        property: ontologies_models.PropertyApiName,
        attachment_rid: ontologies_models.AttachmentRid,
        *,
        stream: bool,
        artifact_repository: typing.Optional[ontologies_models.ArtifactRepositoryRid] = None,
        package_name: typing.Optional[ontologies_models.SdkPackageName] = None,
        chunk_size: typing.Optional[int] = None,
        request_timeout: typing.Optional[core.Timeout] = None,
        _sdk_internal: core.SdkInternal = {},
    ) -> typing.Union[bytes, core.BinaryStream]:
        """
        Get the content of an attachment by its RID.

        The RID must exist in the attachment array of the property.

        Third-party applications using this endpoint via OAuth2 must request the
        following operation scopes: `api:ontologies-read`.

        :param ontology: The API name of the ontology. To find the API name, use the **List ontologies** endpoint or check the **Ontology Manager**.
        :type ontology: OntologyIdentifier
        :param object_type: The API name of the object type. To find the API name, use the **List object types** endpoint or check the **Ontology Manager**.
        :type object_type: ObjectTypeApiName
        :param primary_key: The primary key of the object containing the attachment.
        :type primary_key: PropertyValueEscapedString
        :param property: The API name of the attachment property. To find the API name for your attachment, check the **Ontology Manager** or use the **Get object type** endpoint.
        :type property: PropertyApiName
        :param attachment_rid: The RID of the attachment.
        :type attachment_rid: AttachmentRid
        :param artifact_repository: The repository associated with a marketplace installation.
        :type artifact_repository: Optional[ArtifactRepositoryRid]
        :param package_name: The package name of the generated SDK.
        :type package_name: Optional[SdkPackageName]
        :param stream: Whether to stream back the binary data in an iterator. This avoids reading the entire content of the response into memory at once.
        :type stream: bool
        :param chunk_size: The number of bytes that should be read into memory for each chunk. If set to None, the data will become available as it arrives in whatever size is sent from the host.
        :type chunk_size: Optional[int]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: typing.Union[bytes, core.BinaryStream]
        """
        ...

    @core.maybe_ignore_preview
    @pydantic.validate_call
    @errors.handle_unexpected
    def read_attachment_by_rid(
        self,
        ontology: ontologies_models.OntologyIdentifier,
        object_type: ontologies_models.ObjectTypeApiName,
        primary_key: ontologies_models.PropertyValueEscapedString,
        property: ontologies_models.PropertyApiName,
        attachment_rid: ontologies_models.AttachmentRid,
        *,
        artifact_repository: typing.Optional[ontologies_models.ArtifactRepositoryRid] = None,
        package_name: typing.Optional[ontologies_models.SdkPackageName] = None,
        stream: bool = False,
        chunk_size: typing.Optional[int] = None,
        request_timeout: typing.Optional[core.Timeout] = None,
        _sdk_internal: core.SdkInternal = {},
    ) -> typing.Union[bytes, core.BinaryStream]:
        """
        Get the content of an attachment by its RID.

        The RID must exist in the attachment array of the property.

        Third-party applications using this endpoint via OAuth2 must request the
        following operation scopes: `api:ontologies-read`.

        :param ontology: The API name of the ontology. To find the API name, use the **List ontologies** endpoint or check the **Ontology Manager**.
        :type ontology: OntologyIdentifier
        :param object_type: The API name of the object type. To find the API name, use the **List object types** endpoint or check the **Ontology Manager**.
        :type object_type: ObjectTypeApiName
        :param primary_key: The primary key of the object containing the attachment.
        :type primary_key: PropertyValueEscapedString
        :param property: The API name of the attachment property. To find the API name for your attachment, check the **Ontology Manager** or use the **Get object type** endpoint.
        :type property: PropertyApiName
        :param attachment_rid: The RID of the attachment.
        :type attachment_rid: AttachmentRid
        :param artifact_repository: The repository associated with a marketplace installation.
        :type artifact_repository: Optional[ArtifactRepositoryRid]
        :param package_name: The package name of the generated SDK.
        :type package_name: Optional[SdkPackageName]
        :param stream: Whether to stream back the binary data in an iterator. This avoids reading the entire content of the response into memory at once.
        :type stream: bool
        :param chunk_size: The number of bytes that should be read into memory for each chunk. If set to None, the data will become available as it arrives in whatever size is sent from the host.
        :type chunk_size: Optional[int]
        :param request_timeout: timeout setting for this request in seconds.
        :type request_timeout: Optional[int]
        :return: Returns the result object.
        :rtype: typing.Union[bytes, core.BinaryStream]
        """

        if stream:
            warnings.warn(
                f"client.ontologies.AttachmentProperty.read_attachment_by_rid(..., stream=True, chunk_size={chunk_size}) is deprecated. Please use:\n\nwith client.ontologies.AttachmentProperty.with_streaming_response.read_attachment_by_rid(...) as response:\n    response.iter_bytes(chunk_size={chunk_size})\n",
                DeprecationWarning,
                stacklevel=2,
            )

        return self._api_client.call_api(
            core.RequestInfo(
                method="GET",
                resource_path="/v2/ontologies/{ontology}/objects/{objectType}/{primaryKey}/attachments/{property}/{attachmentRid}/content",
                query_params={
                    "artifactRepository": artifact_repository,
                    "packageName": package_name,
                },
                path_params={
                    "ontology": ontology,
                    "objectType": object_type,
                    "primaryKey": primary_key,
                    "property": property,
                    "attachmentRid": attachment_rid,
                },
                header_params={
                    "Accept": "*/*",
                },
                body=None,
                body_type=None,
                response_type=bytes,
                stream=stream,
                chunk_size=chunk_size,
                request_timeout=request_timeout,
                throwable_errors={},
                response_mode=_sdk_internal.get("response_mode"),
            ),
        )


class _AttachmentPropertyClientRaw:
    def __init__(self, client: AttachmentPropertyClient) -> None:
        def get_attachment(_: ontologies_models.AttachmentMetadataResponse): ...
        def get_attachment_by_rid(_: ontologies_models.AttachmentV2): ...
        def read_attachment(_: bytes): ...
        def read_attachment_by_rid(_: bytes): ...

        self.get_attachment = core.with_raw_response(get_attachment, client.get_attachment)
        self.get_attachment_by_rid = core.with_raw_response(
            get_attachment_by_rid, client.get_attachment_by_rid
        )
        self.read_attachment = core.with_raw_response(read_attachment, client.read_attachment)
        self.read_attachment_by_rid = core.with_raw_response(
            read_attachment_by_rid, client.read_attachment_by_rid
        )


class _AttachmentPropertyClientStreaming:
    def __init__(self, client: AttachmentPropertyClient) -> None:
        def get_attachment(_: ontologies_models.AttachmentMetadataResponse): ...
        def get_attachment_by_rid(_: ontologies_models.AttachmentV2): ...
        def read_attachment(_: bytes): ...
        def read_attachment_by_rid(_: bytes): ...

        self.get_attachment = core.with_streaming_response(get_attachment, client.get_attachment)
        self.get_attachment_by_rid = core.with_streaming_response(
            get_attachment_by_rid, client.get_attachment_by_rid
        )
        self.read_attachment = core.with_streaming_response(read_attachment, client.read_attachment)
        self.read_attachment_by_rid = core.with_streaming_response(
            read_attachment_by_rid, client.read_attachment_by_rid
        )

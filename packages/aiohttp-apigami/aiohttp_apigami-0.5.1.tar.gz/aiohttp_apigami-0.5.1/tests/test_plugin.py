from typing import Any

import pytest
from aiohttp import web
from apispec import APISpec
from apispec.core import VALID_METHODS
from marshmallow import Schema, fields

from aiohttp_apigami.constants import API_SPEC_ATTR
from aiohttp_apigami.data import RouteData
from aiohttp_apigami.plugin import ApigamiPlugin


class SampleSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class SampleResponseSchema(Schema):
    status = fields.Str()
    data = fields.Dict()


class TestApigamiPlugin:
    def test_init(self) -> None:
        """Test basic initialization of the plugin."""
        plugin = ApigamiPlugin()
        assert isinstance(plugin, ApigamiPlugin)

    def test_path_parameters_v2(self) -> None:
        """Test path parameters generation for OpenAPI v2."""
        plugin = ApigamiPlugin()

        # Initialize with v2
        spec = APISpec(
            title="Test API",
            version="1.0.0",
            openapi_version="2.0",
            plugins=[plugin],
        )
        assert spec.plugins == [plugin]

        # Access the private method for testing
        # We're using type: ignore because we're testing a private method
        params = plugin._path_parameters("test_id")

        # Check v2 format
        assert params["in"] == "path"
        assert params["name"] == "test_id"
        assert params["required"] is True
        assert params["type"] == "string"
        assert "schema" not in params

    def test_path_parameters_v3(self) -> None:
        """Test path parameters generation for OpenAPI v3."""
        plugin = ApigamiPlugin()

        # Initialize with v3
        spec = APISpec(
            title="Test API",
            version="1.0.0",
            openapi_version="3.0.0",
            plugins=[plugin],
        )
        assert spec.plugins == [plugin]

        # Access the private method for testing
        params = plugin._path_parameters("test_id")

        # Check v3 format
        assert params["in"] == "path"
        assert params["name"] == "test_id"
        assert params["required"] is True
        assert "type" not in params
        assert "schema" in params
        assert params["schema"]["type"] == "string"

    def test_response_parameters_v2(self) -> None:
        """Test response parameters generation for OpenAPI v2."""
        plugin = ApigamiPlugin()

        # Initialize with v2
        spec = APISpec(
            title="Test API",
            version="1.0.0",
            openapi_version="2.0",
            plugins=[plugin],
        )
        assert spec.plugins == [plugin]

        schema = SampleResponseSchema()
        params = plugin._response_parameters(schema)

        # Check v2 format
        assert "schema" in params
        assert params["schema"] == schema
        assert "content" not in params

    def test_response_parameters_v3(self) -> None:
        """Test response parameters generation for OpenAPI v3."""
        plugin = ApigamiPlugin()

        # Initialize with v3
        spec = APISpec(
            title="Test API",
            version="1.0.0",
            openapi_version="3.0.0",
            plugins=[plugin],
        )
        assert spec.plugins == [plugin]

        schema = SampleResponseSchema()
        params = plugin._response_parameters(schema)

        # Check v3 format
        assert "content" in params
        assert "application/json" in params["content"]
        assert "schema" in params["content"]["application/json"]
        assert params["content"]["application/json"]["schema"] == schema

    @pytest.mark.parametrize(
        "openapi_version,expected_methods",
        [
            ("2.0", VALID_METHODS[2]),
            ("3.0.0", VALID_METHODS[3]),
        ],
    )
    def test_valid_methods(self, openapi_version: str, expected_methods: list[str]) -> None:
        """Test valid methods handling based on OpenAPI version."""
        plugin = ApigamiPlugin()
        spec = APISpec(
            title="Test API",
            version="1.0.0",
            openapi_version=openapi_version,
            plugins=[plugin],
        )
        assert spec.plugins == [plugin]

        # Check that valid methods are correctly determined based on OpenAPI version
        assert plugin.openapi_version is not None
        valid_methods = VALID_METHODS[plugin.openapi_version.major]
        assert valid_methods == expected_methods

    def test_process_body_v2(self) -> None:
        """Test body processing for OpenAPI v2."""
        # Set up plugin
        plugin = ApigamiPlugin()

        # Set up spec with v2
        spec = APISpec(
            title="Test API",
            version="1.0.0",
            openapi_version="2.0",
            plugins=[plugin],
        )
        assert spec.plugins == [plugin]

        # Mock handler with API spec attribute
        async def handler() -> web.StreamResponse:
            return web.Response()

        setattr(
            handler,
            API_SPEC_ATTR,
            {
                "schemas": [
                    {
                        "schema": SampleSchema(),
                        "location": "json",
                        "options": {},
                    }
                ]
            },
        )

        # For v2, body should be empty (body is part of parameters)
        body = plugin._process_body(handler)
        assert body == {}

    def test_process_body_v3(self) -> None:
        """Test body processing for OpenAPI v3."""
        # Set up plugin
        plugin = ApigamiPlugin()

        # Set up spec with v3
        spec = APISpec(
            title="Test API",
            version="1.0.0",
            openapi_version="3.0.0",
            plugins=[plugin],
        )
        assert spec.plugins == [plugin]

        # Mock handler with API spec attribute
        async def handler() -> web.StreamResponse:
            return web.Response()

        schema = SampleSchema()
        setattr(
            handler,
            API_SPEC_ATTR,
            {
                "schemas": [
                    {
                        "schema": schema,
                        "location": "json",
                        "options": {"required": True},
                    }
                ]
            },
        )

        # For v3, body should be formatted as a requestBody
        body = plugin._process_body(handler)
        assert "requestBody" in body
        assert "content" in body["requestBody"]
        assert "application/json" in body["requestBody"]["content"]
        assert "schema" in body["requestBody"]["content"]["application/json"]
        assert body["requestBody"]["content"]["application/json"]["schema"] == schema
        assert body["requestBody"]["required"] is True

    def test_process_body_v3_no_body(self) -> None:
        """Test body processing for OpenAPI v3 without body schema."""
        plugin = ApigamiPlugin()

        # Set up spec with v3
        spec = APISpec(
            title="Test API",
            version="1.0.0",
            openapi_version="3.0.0",
            plugins=[plugin],
        )
        assert spec.plugins == [plugin]

        # Mock handler with API spec attribute but no body schema
        async def handler() -> web.StreamResponse:
            return web.Response()

        setattr(
            handler,
            API_SPEC_ATTR,
            {
                "schemas": [
                    {
                        "schema": SampleSchema(),
                        "location": "querystring",
                        "options": {},
                    }
                ]
            },
        )

        # No body schema, should return empty dict
        body = plugin._process_body(handler)
        assert body == {}

    def test_process_parameters(self) -> None:
        """Test parameters processing."""
        # Set up plugin
        plugin = ApigamiPlugin()

        # Set up spec
        spec = APISpec(
            title="Test API",
            version="1.0.0",
            openapi_version="2.0",
            plugins=[plugin],
        )
        assert spec.plugins == [plugin]

        # Mock handler with API spec attribute
        async def handler() -> web.StreamResponse:
            return web.Response()

        setattr(
            handler,
            API_SPEC_ATTR,
            {
                "parameters": [{"in": "header", "name": "X-Custom-Header", "type": "string"}],
                "schemas": [
                    {
                        "schema": SampleSchema(),
                        "location": "querystring",
                        "example": None,
                        "options": {},
                    }
                ],
            },
        )

        # Process parameters
        params = plugin._process_parameters(handler)

        # Should include both explicit parameters and schema-derived parameters
        assert len(params) > 1  # Header + schema fields
        assert params[0]["in"] == "header"
        assert params[0]["name"] == "X-Custom-Header"

        # Check for schema fields in parameters (id and name from TestSchema)
        query_params = [p for p in params if p["in"] == "query"]
        param_names = [p["name"] for p in query_params]
        assert "id" in param_names
        assert "name" in param_names

    def test_process_responses(self) -> None:
        """Test responses processing."""
        plugin = ApigamiPlugin()

        # Set up spec
        spec = APISpec(
            title="Test API",
            version="1.0.0",
            openapi_version="2.0",
            plugins=[plugin],
        )
        assert spec.plugins == [plugin]

        # Mock handler with API spec attribute
        async def handler() -> web.StreamResponse:
            return web.Response()

        schema = SampleResponseSchema()
        setattr(
            handler,
            API_SPEC_ATTR,
            {
                "responses": {
                    "200": {
                        "schema": schema,
                        "description": "Successful response",
                    },
                    "404": {
                        "description": "Not found",
                    },
                }
            },
        )

        # Process responses
        responses = plugin._process_responses(handler)

        # Check responses format
        assert "200" in responses
        assert "404" in responses
        assert "schema" in responses["200"]
        assert responses["200"]["schema"] == schema
        assert responses["200"]["description"] == "Successful response"
        assert responses["404"]["description"] == "Not found"

    def test_process_extra_options(self) -> None:
        """Test processing of extra options."""

        # Mock handler with API spec attribute
        async def handler() -> web.StreamResponse:
            return web.Response()

        setattr(
            handler,
            API_SPEC_ATTR,
            {
                "tags": ["test"],
                "summary": "Test summary",
                "description": "Test description",
                "schemas": [],  # Should be ignored
                "responses": {},  # Should be ignored
                "parameters": [],  # Should be ignored
            },
        )

        # Process extra options
        options = ApigamiPlugin._process_extra_options(handler)

        # Check options
        assert "tags" in options
        assert options["tags"] == ["test"]
        assert options["summary"] == "Test summary"
        assert options["description"] == "Test description"
        assert "schemas" not in options
        assert "responses" not in options
        assert "parameters" not in options

    def test_path_helper(self) -> None:
        """Test path helper method."""
        plugin = ApigamiPlugin()

        # Set up spec
        spec = APISpec(
            title="Test API",
            version="1.0.0",
            openapi_version="2.0",
            plugins=[plugin],
        )
        assert spec.plugins == [plugin]

        # Mock handler with API spec attribute
        async def handler() -> web.StreamResponse:
            return web.Response()

        schema = SampleSchema()
        response_schema = SampleResponseSchema()
        setattr(
            handler,
            API_SPEC_ATTR,
            {
                "tags": ["test"],
                "summary": "Test endpoint",
                "parameters": [],
                "schemas": [
                    {
                        "schema": schema,
                        "location": "json",
                        "example": None,
                        "options": {},
                    }
                ],
                "responses": {
                    "200": {
                        "schema": response_schema,
                        "description": "Success",
                    }
                },
            },
        )

        # Create route data
        route = RouteData(method="get", path="/test/{test_id}", handler=handler)

        # Call path helper
        operations: dict[str, Any] = {}
        parameters: list[dict[str, Any]] = []
        path = plugin.path_helper(path=None, operations=operations, parameters=parameters, route=route)

        # Check results
        assert path == "/test/{test_id}"
        assert "get" in operations
        assert "parameters" in operations["get"]
        assert "responses" in operations["get"]
        assert "tags" in operations["get"]
        assert operations["get"]["tags"] == ["test"]
        assert operations["get"]["summary"] == "Test endpoint"

        # Check that path parameters were added
        path_params = [p for p in operations["get"]["parameters"] if p["in"] == "path"]
        assert len(path_params) == 1
        assert path_params[0]["name"] == "test_id"

        # Check responses
        assert "200" in operations["get"]["responses"]
        assert "schema" in operations["get"]["responses"]["200"]
        assert operations["get"]["responses"]["200"]["schema"] == response_schema

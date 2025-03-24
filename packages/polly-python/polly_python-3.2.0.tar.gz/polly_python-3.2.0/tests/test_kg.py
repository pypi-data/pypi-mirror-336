# from polly import polly_kg
from polly.polly_kg import PollyKG
import pytest

import os
from polly.errors import InvalidParameterException, RequestException

key = "POLLY_API_KEY"
token = os.getenv(key)

test_key = "TEST_POLLY_API_KEY"
testpolly_token = os.getenv(test_key)


def test_obj_initialised():
    assert PollyKG(testpolly_token, env="testpolly") is not None


def test_get_engine_status():
    obj = PollyKG(testpolly_token, env="testpolly")
    assert dict(obj.get_engine_status()) is not None


def test_get_graph_summary():
    obj = PollyKG(testpolly_token, env="testpolly")
    response = obj.get_graph_summary()

    assert response is not None
    assert isinstance(response, dict)
    assert response["numNodes"] is not None
    assert response["numEdges"] is not None


def test_run_gremlin_query_success(mocker):
    # Mocked response from API
    mocked_response = {
        "data": {
            "requestId": "ab81155d-9f64-4717-a1e3-4e70bf5e6dff",
            "status": {
                "message": "",
                "code": 200,
                "attributes": {"@type": "g:Map", "@value": []},
            },
            "result": {
                "data": {
                    "@type": "g:List",
                    "@value": [
                        {
                            "@type": "g:Map",
                            "@value": [
                                "id",
                                "9796",
                                "properties",
                                {
                                    "@type": "g:Map",
                                    "@value": [
                                        "name",
                                        {"@type": "g:List", "@value": ["PHYHIP"]},
                                    ],
                                },
                            ],
                        },
                        {
                            "@type": "g:Map",
                            "@value": [
                                "id",
                                "5297",
                                "properties",
                                {
                                    "@type": "g:Map",
                                    "@value": [
                                        "name",
                                        {"@type": "g:List", "@value": ["PI4KA"]},
                                    ],
                                },
                            ],
                        },
                    ],
                },
                "meta": {"@type": "g:Map", "@value": []},
            },
        }
    }

    obj = PollyKG(testpolly_token, env="testpolly")

    # Test invalid query (empty query should raise an exception)
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.run_gremlin_query("")

    # Test invalid query (wrong query should raise an exception)
    with pytest.raises(RequestException):
        obj.run_gremlin_query("g.V().liit(5).project('id').by(id).by(valueMap())")

    # Mock the post request in session
    response_post = mocker.patch.object(obj.session, "post")
    response_post.return_value.status_code = 200
    response_post.return_value.json.return_value = mocked_response

    # Test valid query
    query = "g.V().count()"
    result = obj.run_gremlin_query(query)

    # Expected result from mocked response
    expected_result = {
        "data": {
            "@type": "g:List",
            "@value": [
                {
                    "@type": "g:Map",
                    "@value": [
                        "id",
                        "9796",
                        "properties",
                        {
                            "@type": "g:Map",
                            "@value": [
                                "name",
                                {"@type": "g:List", "@value": ["PHYHIP"]},
                            ],
                        },
                    ],
                },
                {
                    "@type": "g:Map",
                    "@value": [
                        "id",
                        "5297",
                        "properties",
                        {
                            "@type": "g:Map",
                            "@value": [
                                "name",
                                {"@type": "g:List", "@value": ["PI4KA"]},
                            ],
                        },
                    ],
                },
            ],
        },
        "meta": {"@type": "g:Map", "@value": []},
    }

    assert result == expected_result


def test_run_opencypher_query_success(mocker):
    # Mocked response from API
    mocked_response = {
        "data": {
            "ResponseMetadata": {
                "HTTPStatusCode": 200,
                "HTTPHeaders": {
                    "transfer-encoding": "chunked",
                    "content-type": "application/json;charset=UTF-8",
                },
                "RetryAttempts": 0,
            },
            "results": [
                {
                    "node": {
                        "~id": "5555",
                        "~entityType": "node",
                        "~labels": ["Gene"],
                        "~properties": {
                            "EnsemblGeneID": "EEEEEEEEEEEEEEEE",
                            "Symbol": "PPPPPPPPP",
                            "LocusTag": "-",
                            "Synonyms": "CCCCCCCCC",
                        },
                    }
                }
            ],
        }
    }

    obj = PollyKG(testpolly_token, env="testpolly")

    # Test invalid query (empty query should raise an exception)
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.run_opencypher_query("")

    with pytest.raises(RequestException):
        obj.run_opencypher_query("abcd")

    # Mock the post request in session
    response_post = mocker.patch.object(obj.session, "post")
    response_post.return_value.status_code = 200
    response_post.return_value.json.return_value = mocked_response

    # Test valid query
    query = "MATCH (node) RETURN node LIMIT 1"
    result = obj.run_opencypher_query(query)

    # Expected result from mocked response
    expected_result = mocked_response["data"]["results"]

    assert result == expected_result

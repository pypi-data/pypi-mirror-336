import os
import time

import pytest
from crow_client.clients import (
    JobNames,
    JobResponseVerbose,
    PQAJobResponse,
)
from crow_client.clients.rest_client import JobFetchError, RestClient
from crow_client.models.app import JobRequest, Stage
from pytest_subtests import SubTests

ADMIN_API_KEY = os.environ["PLAYWRIGHT_ADMIN_API_KEY"]
PUBLIC_API_KEY = os.environ["PLAYWRIGHT_PUBLIC_API_KEY"]


@pytest.mark.timeout(300)
@pytest.mark.flaky(reruns=3)
def test_futurehouse_dummy_env_crow():
    client = RestClient(
        stage=Stage.DEV,
        api_key=ADMIN_API_KEY,
    )

    job_data = JobRequest(
        name=JobNames.from_string("dummy"),
        query="How many moons does earth have?",
    )
    client.create_job(job_data)

    while (job_status := client.get_job().status) in {"queued", "in progress"}:
        time.sleep(5)

    assert job_status == "success"


def test_insufficient_permissions_request():
    # Create a new instance so that cached credentials aren't reused
    client = RestClient(
        stage=Stage.DEV,
        api_key=PUBLIC_API_KEY,
    )
    job_data = JobRequest(
        name=JobNames.from_string("dummy"),
        query="How many moons does earth have?",
    )

    with pytest.raises(JobFetchError) as exc_info:
        client.create_job(job_data)

    assert "Error creating job" in str(exc_info.value)


# @pytest.mark.timeout(30)
def test_job_response(subtests: SubTests):
    client = RestClient(
        stage=Stage.DEV,
        api_key=ADMIN_API_KEY,
    )
    job_data = JobRequest(
        name=JobNames.from_string("crow"),
        query="How many moons does earth have?",
    )
    job_id = client.create_job(job_data)

    with subtests.test("Test JobResponse with queued job"):
        job_response = client.get_job(job_id)
        assert job_response.status in {"queued", "in progress"}
        assert job_response.crow == job_data.name
        assert job_response.task == job_data.query

    while (job_status := client.get_job(job_id).status) in {"queued", "in progress"}:
        time.sleep(5)

    with subtests.test("Test PQA job response"):
        job_response = client.get_job(job_id)
        assert isinstance(job_response, PQAJobResponse)
        # assert it has general fields
        assert job_response.status == "success"
        assert job_data.name in job_response.crow
        assert job_data.query in job_response.task
        # assert it has PQA specific fields
        assert job_response.answer is not None
        # assert it's not verbose
        assert not hasattr(job_response, "environment_frame")
        assert not hasattr(job_response, "agent_state")

    with subtests.test("Test job response with verbose"):
        job_response = client.get_job(job_id, verbose=True)
        assert isinstance(job_response, JobResponseVerbose)
        assert job_response.status == "success"
        assert job_response.environment_frame is not None
        assert job_response.agent_state is not None

import requests;
from typing import Dict, List;
from ..types.enums import (
    PuppetRegion, 
);
from ..types.job_types import (
    WebAgentConfig, Job, 
    JobSchedule, JobNavigation,
    JobNavigationType, JobSchedulePolicy, 
    GetJobResponse, GetJobsResponse, 
    JobExecutionResponse, GetJobResultResponse
);
from .utils import dict_to_camel_case, dict_to_snake_case

# Grabba SDK Class
class Grabba:
    def __init__(self, api_key: str, region: PuppetRegion = PuppetRegion.US):
        if not api_key:
            raise ValueError("API key is required")
        self.api_key = api_key
        self.api_url = "https://api.grabba.dev/v1"
        self.default_puppet_config = WebAgentConfig(region=region)
        self.default_job_navigation = JobNavigation(type=JobNavigationType.NONE)
        self.default_job_schedule = JobSchedule(policy=JobSchedulePolicy.IMMEDIATELY)

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "X-Api-Key": self.api_key,
        }

    def extract(self, job: Job) -> JobExecutionResponse:
        if not job.puppet_config:
            job.puppet_config = self.default_puppet_config
        if not job.navigation:
            job.navigation = self.default_job_navigation
        if not job.schedule:
            job.schedule = self.default_job_schedule
        complete_job = {
            "url": job.url,
            "tasks": job.tasks,
            "schedule": {
                "policy": job.schedule.policy.value,
                "specification": job.schedule.specification,
            },
            "navigation": {
                "type": job.navigation.type.value,
                "options": job.navigation.options,
            },
            "puppet_config": {
                "region": job.puppet_config.region.value,
            },
        }
        # convert job object keys to camelCase
        jobToCamelCase = dict_to_camel_case(complete_job)
        # Send request
        response = requests.post(
            f"{self.api_url}/extract",
            headers=self._get_headers(),
            json=jobToCamelCase,
        )
        response.raise_for_status()
        snake_case_response = dict_to_snake_case(response.json())
        return JobExecutionResponse(**snake_case_response)
    
    def schedule_job(self, job_id: str) -> JobExecutionResponse:
        response = requests.post(
            f"{self.api_url}/schedule-job/{job_id}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        snake_case_response = dict_to_snake_case(response.json())
        return JobExecutionResponse(**snake_case_response)

    def get_jobs(self) -> GetJobsResponse:
        response = requests.get(
            f"{self.api_url}/jobs",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return GetJobsResponse(**response.json())

    def get_job(self, job_id: str) -> GetJobResponse:
        response = requests.get(
            f"{self.api_url}/jobs/{job_id}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return GetJobResponse(**response.json())

    def get_job_result(self, job_result_id: str) -> GetJobResultResponse:
        response = requests.get(
            f"{self.api_url}/job-result/{job_result_id}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return GetJobResultResponse(**response.json())

    def get_available_regions(self) -> List[Dict[str, PuppetRegion]]:
        return [{k: v.value} for k, v in PuppetRegion.__members__.items()]
    

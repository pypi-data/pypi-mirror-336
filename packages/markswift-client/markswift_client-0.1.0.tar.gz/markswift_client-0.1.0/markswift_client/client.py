"""
MarkSwift API Client implementation
"""

import os
import json
import time
from typing import Dict, List, Optional, Union, BinaryIO, Any
import requests


class MarkSwiftError(Exception):
    """Exception raised for errors in the MarkSwift API."""
    pass


class MarkSwiftClient:
    """
    Client for the MarkSwift API.
    
    This class provides methods to interact with the MarkSwift API for document conversion.
    """
    
    def __init__(self, api_key: str = None, base_url: str = "https://api.datavisionlabs.ai"):
        """
        Initialize the MarkSwift API client.
        
        Args:
            api_key: Your MarkSwift API key. If not provided, it will look for the 
                    MARKSWIFT_API_KEY environment variable.
            base_url: The base URL for the MarkSwift API. Defaults to https://api.datavisionlabs.ai.
        
        Raises:
            ValueError: If no API key is provided and the MARKSWIFT_API_KEY environment variable is not set.
        """
        self.api_key = api_key or os.environ.get("MARKSWIFT_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key must be provided either as an argument or through the MARKSWIFT_API_KEY environment variable."
            )
        
        self.base_url = base_url.rstrip("/")
    
    def _get_headers(self) -> Dict[str, str]:
        """
        Get the headers for API requests.
        
        Returns:
            Dict[str, str]: The headers for API requests.
        """
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }
    
    def convert_file(self, file_path: str, conversion_type: str = "basic") -> str:
        """
        Convert a file to Markdown.
        
        Args:
            file_path: Path to the file to convert.
            conversion_type: Type of conversion to perform. Options are "basic" or "enhanced".
                            Defaults to "basic".
        
        Returns:
            str: The job ID for the conversion.
        
        Raises:
            MarkSwiftError: If the API request fails.
            FileNotFoundError: If the file does not exist.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        url = f"{self.base_url}/api/convert"
        
        with open(file_path, "rb") as file:
            files = {"file": (os.path.basename(file_path), file)}
            data = {"job_type": conversion_type}
            
            try:
                response = requests.post(
                    url,
                    headers=self._get_headers(),
                    files=files,
                    data=data
                )
                response.raise_for_status()
                result = response.json()
                
                if "job_id" not in result:
                    raise MarkSwiftError(f"Unexpected response from API: {result}")
                
                return result["job_id"]
            except requests.exceptions.RequestException as e:
                raise MarkSwiftError(f"Error converting file: {str(e)}")
    
    def convert_files(self, file_paths: List[str], conversion_type: str = "basic") -> List[str]:
        """
        Convert multiple files to Markdown.
        
        Args:
            file_paths: List of paths to the files to convert.
            conversion_type: Type of conversion to perform. Options are "basic" or "enhanced".
                            Defaults to "basic".
        
        Returns:
            List[str]: The job IDs for the conversions.
        
        Raises:
            MarkSwiftError: If the API request fails.
            FileNotFoundError: If any of the files do not exist.
        """
        for file_path in file_paths:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
        
        url = f"{self.base_url}/api/convert/batch"
        
        files = []
        for file_path in file_paths:
            with open(file_path, "rb") as file:
                files.append(("files", (os.path.basename(file_path), file.read())))
        
        data = {"job_type": conversion_type}
        
        try:
            response = requests.post(
                url,
                headers=self._get_headers(),
                files=files,
                data=data
            )
            response.raise_for_status()
            result = response.json()
            
            if "job_ids" not in result and "successful_jobs" not in result:
                raise MarkSwiftError(f"Unexpected response from API: {result}")
            
            if "job_ids" in result:
                return result["job_ids"]
            else:
                return [job["job_id"] for job in result["successful_jobs"]]
        except requests.exceptions.RequestException as e:
            raise MarkSwiftError(f"Error converting files: {str(e)}")
    
    def check_status(self, job_id: str) -> Dict[str, Any]:
        """
        Check the status of a conversion job.
        
        Args:
            job_id: The job ID to check.
        
        Returns:
            Dict[str, Any]: The status of the job.
        
        Raises:
            MarkSwiftError: If the API request fails.
        """
        url = f"{self.base_url}/api/status/{job_id}"
        
        try:
            response = requests.get(
                url,
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise MarkSwiftError(f"Error checking job status: {str(e)}")
    
    def check_batch_status(self, job_ids: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Check the status of multiple conversion jobs.
        
        Args:
            job_ids: The job IDs to check.
        
        Returns:
            Dict[str, List[Dict[str, Any]]]: The status of the jobs.
        
        Raises:
            MarkSwiftError: If the API request fails.
        """
        url = f"{self.base_url}/api/status/batch"
        
        try:
            response = requests.post(
                url,
                headers={**self._get_headers(), "Content-Type": "application/json"},
                json={"job_ids": job_ids}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise MarkSwiftError(f"Error checking batch job status: {str(e)}")
    
    def fetch_markdown(self, job_id: str) -> str:
        """
        Fetch the Markdown content for a completed job.
        
        Args:
            job_id: The job ID to fetch.
        
        Returns:
            str: The Markdown content.
        
        Raises:
            MarkSwiftError: If the API request fails or the job is not complete.
        """
        url = f"{self.base_url}/api/fetch-markdown/{job_id}"
        
        try:
            response = requests.get(
                url,
                headers=self._get_headers()
            )
            response.raise_for_status()
            result = response.json()
            
            if "markdown" not in result:
                raise MarkSwiftError(f"Unexpected response from API: {result}")
            
            return result["markdown"]
        except requests.exceptions.RequestException as e:
            raise MarkSwiftError(f"Error fetching markdown: {str(e)}")
    
    def fetch_batch_markdown(self, job_ids: List[str]) -> Dict[str, str]:
        """
        Fetch the Markdown content for multiple completed jobs.
        
        Args:
            job_ids: The job IDs to fetch.
        
        Returns:
            Dict[str, str]: A dictionary mapping job IDs to Markdown content.
        
        Raises:
            MarkSwiftError: If any of the API requests fail.
        """
        results = {}
        
        for job_id in job_ids:
            try:
                markdown = self.fetch_markdown(job_id)
                results[job_id] = markdown
            except MarkSwiftError as e:
                # Continue with other jobs even if one fails
                results[job_id] = f"Error: {str(e)}"
        
        return results
    
    def cancel_job(self, job_id: str) -> bool:
        """
        Cancel a conversion job.
        
        Args:
            job_id: The job ID to cancel.
        
        Returns:
            bool: True if the job was successfully canceled, False otherwise.
        
        Raises:
            MarkSwiftError: If the API request fails.
        """
        url = f"{self.base_url}/api/cancel/{job_id}"
        
        try:
            response = requests.post(
                url,
                headers=self._get_headers()
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException:
            return False
    
    def cancel_batch_job(self, batch_id: str) -> Dict[str, Any]:
        """
        Cancel a batch conversion job.
        
        Args:
            batch_id: The batch ID to cancel.
        
        Returns:
            Dict[str, Any]: Information about the canceled batch job.
        
        Raises:
            MarkSwiftError: If the API request fails.
        """
        url = f"{self.base_url}/api/cancel/batch/{batch_id}"
        
        try:
            response = requests.post(
                url,
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise MarkSwiftError(f"Error canceling batch job: {str(e)}")
    
    def export_html(self, job_id: str) -> str:
        """
        Export the markdown as HTML.
        
        Args:
            job_id: The job ID to export.
        
        Returns:
            str: The HTML content.
        
        Raises:
            MarkSwiftError: If the API request fails.
        """
        url = f"{self.base_url}/api/export/{job_id}/html"
        
        try:
            response = requests.get(
                url,
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            raise MarkSwiftError(f"Error exporting HTML: {str(e)}")
    
    def list_documents(self) -> List[Dict[str, Any]]:
        """
        List all documents processed by the user.
        
        Returns:
            List[Dict[str, Any]]: List of documents.
        
        Raises:
            MarkSwiftError: If the API request fails.
        """
        url = f"{self.base_url}/api/documents"
        
        try:
            response = requests.get(
                url,
                headers=self._get_headers()
            )
            response.raise_for_status()
            result = response.json()
            
            if "documents" not in result:
                raise MarkSwiftError(f"Unexpected response from API: {result}")
            
            return result["documents"]
        except requests.exceptions.RequestException as e:
            raise MarkSwiftError(f"Error listing documents: {str(e)}")
    
    def delete_document(self, job_id: str) -> bool:
        """
        Delete a document and its associated resources.
        
        Args:
            job_id: The job ID to delete.
        
        Returns:
            bool: True if the document was successfully deleted, False otherwise.
        
        Raises:
            MarkSwiftError: If the API request fails.
        """
        url = f"{self.base_url}/api/documents/{job_id}/delete"
        
        try:
            response = requests.delete(
                url,
                headers=self._get_headers()
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException:
            return False
    
    def get_user_credits(self) -> int:
        """
        Get the current user's credit balance.
        
        Returns:
            int: The user's credit balance.
        
        Raises:
            MarkSwiftError: If the API request fails.
        """
        url = f"{self.base_url}/api/user/credits"
        
        try:
            response = requests.get(
                url,
                headers=self._get_headers()
            )
            response.raise_for_status()
            result = response.json()
            
            if "credits" not in result:
                raise MarkSwiftError(f"Unexpected response from API: {result}")
            
            return result["credits"]
        except requests.exceptions.RequestException as e:
            raise MarkSwiftError(f"Error getting user credits: {str(e)}")
    
    def wait_for_completion(self, job_id: str, timeout: int = 300, poll_interval: int = 2) -> str:
        """
        Wait for a job to complete and return the Markdown content.
        
        Args:
            job_id: The job ID to wait for.
            timeout: Maximum time to wait in seconds. Defaults to 300 seconds (5 minutes).
            poll_interval: Time between status checks in seconds. Defaults to 2 seconds.
        
        Returns:
            str: The Markdown content.
        
        Raises:
            MarkSwiftError: If the job fails or times out.
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.check_status(job_id)
            
            if status["status"] == "completed":
                return self.fetch_markdown(job_id)
            elif status["status"] == "failed":
                raise MarkSwiftError(f"Job failed: {status.get('error', 'Unknown error')}")
            
            time.sleep(poll_interval)
        
        raise MarkSwiftError(f"Job timed out after {timeout} seconds")

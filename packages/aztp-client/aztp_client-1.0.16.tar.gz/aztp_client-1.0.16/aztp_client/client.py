import socket
from datetime import datetime
from typing import Optional, Callable, Any, Dict, List, Union
import requests
from uuid import uuid4
import urllib3
import json
from dataclasses import dataclass
from pprint import pprint
import asyncio
from termcolor import colored
import warnings

# Global variable
globalName = None

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from aztp_client.common.config import ClientConfig, whiteListTrustDomains
from aztp_client.common.types import (
    Identity,
    SecuredAgent,
    IssueIdentityRequest,
    Metadata,
)

class SecureConnection:
    """Secure wrapper for agents that provides identity verification while maintaining original functionality."""
    
    def __init__(self, agent: Any, identity: Identity, verify: Callable):
        """Initialize secure connection.
        
        Args:
            agent: The original agent being wrapped
            identity: AZTP identity information
            verify: Identity verification function
        """
        self._agent = agent
        self.identity = identity
        self.verify = verify
    
    def make_callable(self, func: Callable) -> Callable:
        """Create a secure callable that verifies identity before execution.
        
        Args:
            func: The original function to wrap
            
        Returns:
            Callable: A wrapped function that performs identity verification
        """
        async def wrapped(*args, **kwargs):
            # Verify identity before executing the function
            if not await self.verify():
                raise PermissionError("Identity verification failed")
            return await func(*args, **kwargs)
        return wrapped
    
    def __getattr__(self, name: str) -> Any:
        """Delegate any unknown attributes/methods to the wrapped agent.
        
        This enables transparent method delegation - any method call not handled
        by SecureConnection is passed through to the original agent with identity verification.
        
        Args:
            name: Name of the attribute/method being accessed
            
        Returns:
            The attribute/method from the wrapped agent, wrapped with identity verification if callable
        """
        attr = getattr(self._agent, name)
        if callable(attr) and asyncio.iscoroutinefunction(attr):
            return self.make_callable(attr)
        return attr

class Aztp:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        environment: Optional[str] = None,
        timeout: Optional[int] = None,
    ):
        """Initialize AZTP client with optional configuration."""
        self.config = ClientConfig.create(
            api_key=api_key,
            base_url=base_url,
            environment=environment,
            timeout=timeout,
        )
        self.session = requests.Session()
        self.session.headers.update({
            "api_access_key": f"{self.config.api_key}",
            "Content-Type": "application/json",
        })
        print(colored("API Key:", "cyan"), f"{self.config.api_key[:8]}...")

    def _get_url(self, endpoint: str) -> str:
        """Get full URL for an endpoint."""
        # Just join the base URL with the endpoint
        base_url = self.config.base_url.rstrip('/')
        endpoint = endpoint.lstrip('/')
        return f"{base_url}/{endpoint}"

    async def secure_connect(self, crew_agent: Optional[object] = None, name: Optional[str] = None, config: Optional[dict] = None) -> SecureConnection:
        """Create a secure connection for a workload.
        
        Args:
            crew_agent: Optional object representing the crew agent
            name: Name of the agent (required)
            config: Dictionary containing configuration options:
                - linkedIdentities: Optional list of AZTP IDs of linked agents
                - trustDomain: Optional trust domain for the agent
                - isGlobalIdentity: Whether this is a global identity (default: False)
            
        Returns:
            SecureConnection: An object containing identity information and verify function
        """
        if not config or not isinstance(config, dict):
            raise ValueError("config parameter must be a dictionary")
            
        metadata = Metadata(
            hostname=socket.gethostname(),
            environment=self.config.environment,
        )

        globalName = name if config.get("isGlobalIdentity", False) else None
        
        request = IssueIdentityRequest(
            workload_id=name,
            agent_id="aztp",
            timestamp=datetime.now().astimezone().isoformat(),
            method="node",
            metadata=metadata,
        )
        
        # Convert request to dict and ensure proper casing for JSON
        request_data = {
            "workloadId": request.workload_id,
            "agentId": request.agent_id,
            "timestamp": request.timestamp,
            "isGlobalIdentity": config.get("isGlobalIdentity", False),
            "method": request.method,
            "metadata": {
                "hostname": request.metadata.hostname,
                "environment": request.metadata.environment,
                "extra": request.metadata.extra,
                "trustDomain": None,
                "linkTo": None
            }
        }

        # Add optional parameters if provided
        if config.get("linkedIdentities"):
            request_data["metadata"]["linkTo"] = config["linkedIdentities"]
        if config.get("trustDomain"):
            request_data["metadata"]["trustDomain"] = config["trustDomain"]
        

        url = self._get_url("issue-identity")
        
        try:
            response = self.session.post(
                url,
                json=request_data,
                timeout=self.config.timeout,
                verify=False,  # Disable SSL verification
            )
            
            response.raise_for_status()
            
            identity_data = response.json()
            
            # Get the data field from the response
            if isinstance(identity_data, dict) and 'data' in identity_data:
                identity_info = identity_data['data']

                if(identity_info.get("valid") is False):
                    aztp_id = identity_info.get("error")
                    valid = False
                else:
                    aztp_id = identity_info.get("aztpId")
                    valid = True
                
                # Create identity object
                identity = Identity(
                    aztp_id=aztp_id,
                    valid=valid,
                    certificate="",
                    private_key="",
                    ca_certificate=""
                )
                
                # Create secured agent instance for verify function
                secured_agent = SecuredAgent(
                    name=name,
                    identity=identity,
                    metadata=metadata,
                )
                
                # Return SecureConnection instance with the original agent
                return SecureConnection(
                    agent=crew_agent,
                    identity=identity,
                    verify=lambda: self.verify_identity(secured_agent)
                )
            else:
                raise Exception("Invalid response format: missing 'data' field")
        except requests.exceptions.RequestException as e:
            print(f"\nRequest failed: {str(e)}")
            if hasattr(e.response, 'text'):
                print(f"Error response: {e.response.text}")
            raise

    async def verify_identity(self, agent: SecuredAgent) -> bool:
        """Verify the identity of a secured agent."""
        if not agent.identity:
            return False
        
        if(agent.identity.valid is False):
            return False
            
        response = self.session.post(
            self._get_url("verify-identity"),
            json={"aztpId": agent.identity.aztp_id},
            timeout=self.config.timeout,
            verify=False,  # Disable SSL verification
        )
        response.raise_for_status()
        
        result = response.json()
        
        if isinstance(result, dict) and 'data' in result:
            if result.get("success") is True:
                return result['data'].get("valid", False)
            else:
                # Check if data exists and has a message before trying to access it
                if isinstance(result.get('data'), dict) and 'message' in result['data']:
                    print(result['data']['message'])
                elif 'message' in result:
                    print(result['message'])
                else:
                    print("Verification failed with no detailed message")
                return False
        else:
            return result.get("valid", False)

    async def verify_identity_using_agent_name(
        self,
        name: str,
        trust_domain: str = "aztp.network",
        workload: str = "workload",
        environment: str = "production",
        method: str = "node"
    ) -> bool:
        """Verify identity using agent name and optional parameters.
        
        This method allows verification of an agent's identity in two ways:
        1. Using a full AZTP ID (e.g., "aztp://aztp.network/workload/production/node/my-service")
        2. Using just the agent name with optional parameters to construct the AZTP ID
        
        Args:
            name: The agent name or full AZTP ID
                - If it starts with "aztp://", it will be used as-is
                - Otherwise, it will be combined with other parameters to form a full AZTP ID
            trust_domain: The trust domain (default: "aztp.network")
                This is typically your organization's domain
            workload: The workload identifier (default: "workload")
                This groups related services/agents
            environment: The deployment environment (default: "production")
                Common values: production, staging, development
            method: The authentication method (default: "node")
                Typically left as "node" unless using a different auth method
        
        Returns:
            bool: True if identity is valid, False otherwise
        """
        # If already a full AZTP ID, use as-is
        if name.startswith("aztp://"):
            print("Using existing AZTP ID:", name)
            aztp_id = name
        else:
            # Otherwise, construct the full AZTP ID with default values
            aztp_id = f"aztp://{trust_domain}/{workload}/{environment}/{method}/{name}"
            
        response = self.session.post(
            self._get_url("verify-identity"),
            json={"aztpId": aztp_id},
            timeout=self.config.timeout,
            verify=False,  # Disable SSL verification
        )
        response.raise_for_status()
        
        result = response.json()
        if isinstance(result, dict) and 'data' in result:
            return result['data'].get("valid", False)
        return result.get("valid", False)

    async def verify_identity_connection(self, fromAgentID: str, toAgentID: str) -> bool:
        """Verify the connection between two secured agent's identity.
        
        This method verifies that the connection between two agents is valid.
        It checks if the fromAgentID is valid and if the fromAgentID is connected to the toAgentID.
    
        Args:
            fromAgentID: The AZTP ID of the agent to verify connection for
            toAgentID: The AZTP ID of the agent to verify connection request from
            
        Returns:
            bool: True if connection is valid, False otherwise
        """

        if not fromAgentID.startswith("aztp://") or not toAgentID.startswith("aztp://"):
            return False
        
        response = self.session.post(
            self._get_url("verify-identity-for-connection"),
            json={
                "aztpId": fromAgentID,
                "requestAztpId": toAgentID
            },
            timeout=self.config.timeout,
            verify=False,  # Disable SSL verification
        )
        response.raise_for_status()
        
        result = response.json()
        if isinstance(result, dict) and 'data' in result:
            # Check if data is not None before trying to access it
            if result['success'] is True and isinstance(result['data'], dict):
                return result['data'].get("valid", False)
            else:
                return False
        return result.get("valid", False)   
    

    async def get_identity(self, agent: SecureConnection) -> dict:
        """Get the identity details for a secured agent.
        
        Args:
            agent: The SecureConnection object to get identity for
            
        Returns:
            dict: The identity information including metadata and workload info
        """
        if not agent.identity:
            return None
        
        # Pretty print the agent object with color
        print("\n" + colored("=== Agent Details ===", "cyan", attrs=["bold"]))
        agent_info = {
            "identity": {
                "aztp_id": agent.identity.aztp_id,
                "valid": agent.identity.valid
            }
        }
        print(json.dumps(agent_info, indent=2))

        workload_id = agent.identity.aztp_id.split('/')[-1] if agent.verify else globalName
        print(colored("\nWorkload ID:", "cyan"), workload_id)
            
        response = self.session.get(
            self._get_url(f"get-identity/{workload_id}"),
            timeout=self.config.timeout,
            verify=False,  # Disable SSL verification
        )
        response.raise_for_status()
        
        identity_data = response.json()
        
        # Get the data field from the response
        if isinstance(identity_data, dict) and 'data' in identity_data:
            identity_info = identity_data['data']
            
            # Check if identity_info is a string (error message) or not a dict
            if isinstance(identity_info, str) or not isinstance(identity_info, dict):
                print(colored("\nError retrieving identity:", "red"), identity_info)
                return None
            
            # Print the formatted identity information with colors
            print(colored("\n=== Identity Information ===", "cyan", attrs=["bold"]))
            formatted_info = {
                "Basic Info": {
                    "AZTP ID": identity_info.get("aztpId"),
                    "Status": colored(identity_info.get("status", "unknown"), "green" if identity_info.get("status") == "active" else "yellow"),
                    "Environment": identity_info.get("environment")
                },
                "Timestamps": {
                    "Created": identity_info.get("createdAt"),
                    "Updated": identity_info.get("updatedAt"),
                    "Rotate At": identity_info.get("rotateAt")
                },
                "Metadata": identity_info.get("metadata", {}),
                "Workload Info": identity_info.get("workloadInfo", {})
            }
            
            # Print each section
            for section, data in formatted_info.items():
                print(colored(f"\n{section}:", "yellow", attrs=["bold"]))
                print(json.dumps(data, indent=2))
            
            # Convert response to match required format
            return {
                "aztpId": identity_info.get("aztpId"),
                "createdAt": identity_info.get("createdAt"),
                "environment": identity_info.get("environment"),
                "issuedAt": identity_info.get("issuedAt"),
                "metadata": identity_info.get("metadata", {}),
                "rotateAt": identity_info.get("rotateAt"),
                "selectors": identity_info.get("selectors", []),
                "status": identity_info.get("status", "active"),
                "updatedAt": identity_info.get("updatedAt"),
                "workloadInfo": identity_info.get("workloadInfo", {})
            }
        else:
            raise Exception("Invalid response format: missing 'data' field") 
        
    async def discover_identity(self, trust_domain: str = None, requestor_identity: str = None) -> dict:
        """Discover identities based on requestor identity and optional trust domain.
        
        This method allows agents to discover identities based on a requestor identity.
        It can optionally filter identities by a specified trust domain.
        
        Args:
            trust_domain: Optional trust domain to filter identities by (optional)
            requestor_identity: The AZTP ID of the requestor agent (optional)
            
        Returns:
            dict: List of discovered identities
        """

        if trust_domain and requestor_identity:
            response = self.session.get(
                self._get_url("discover-with-trust-domain"),
                params={
                    "trustDomain": trust_domain,
                    "requestorIdentity": requestor_identity,
                },
                timeout=self.config.timeout,
                verify=False,  # Disable SSL verification
            )
        else:
            response = self.session.get(
                self._get_url("discoverable"),
                params={
                    "discoverable": True
                },
                timeout=self.config.timeout,
            verify=False,  # Disable SSL verification
        )
        response.raise_for_status()
        
        result = response.json()
        if isinstance(result, dict) and 'data' in result:
            return result['data']
        else:
            raise Exception("Invalid response format: missing 'data' field") 
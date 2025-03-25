import sys
import os

# Get the absolute path of the codegens folder
codegens_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "codegens"))

# Add it to sys.path
if codegens_path not in sys.path:
    sys.path.append(codegens_path)

from mcp.server.fastmcp import FastMCP
from google.protobuf.json_format import MessageToJson
import json
import requests
import codegens.gravi.rest.model.platform_rest_pb2 as platform_rest
import codegens.gravi.rest.model.login_pb2 as login_rest
import codegens.gravi.rest.auth.auth_pb2 as auth_rest
from codegens.gravi.models import gravi_model_pb2 as gravi_model


mcp = FastMCP("landingpad")

endpoint = "https://platform-dev.landingpad.me/platform/api"
# endpoint = "http://localhost:8080/platform/api"
class AuthTicket:
    def __init__(self, stoken: str | None = None, userId: str=""):
        self.stoken = stoken
        self.userId = userId

from enum import Enum
class WorkSpace(Enum):
    PRIVATE = 1
    SHARED = 2

authTicket = AuthTicket()

def make_request(req: platform_rest.PlatformRestRequest) -> platform_rest.PlatformRestResponse | None:
    global authTicket

    """
    Sends a serialized protobuf request to a specified endpoint via an HTTP POST request 
    and deserializes the response into a PlatformRestResponse object.
    Args:
        req (platform_rest.PlatformRestRequest): The protobuf request object to be serialized and sent.
    Returns:
        platform_rest.PlatformRestResponse | None: The deserialized response object if the request is successful 
        (HTTP 200), or None if an error occurs.
    """
    from codegens.gravi.models import gravi_model_pb2 as gravi_model
    import uuid
    
    # req.deviceInfo = gravi_model.DeviceInfo(browser = "gs-cli", os = "MacOS")
    req.deviceInfo.deviceId = "gs-cli"
    req.deviceInfo.browser = "gs-cli"
    req.deviceInfo.os = "MacOS"

    if authTicket.stoken is not None:
        req.ticket.stoken = authTicket.stoken
    req.clientVersion = "6.4.6-gscli"
    req.reqId = uuid.uuid4().hex

    # Serialize the protobuf object to a byte array
    serialized_req = req.SerializeToString()
    
    # Send the serialized data in the HTTP POST request
    headers = {"Content-Type": "application/octet-stream"}
    response = requests.post(endpoint, data=serialized_req, headers=headers)
    
    # Deserialize the response binary stream into a PlatformRestResponse object
    if response.status_code == 200:
        platform_response = platform_rest.PlatformRestResponse()
        platform_response.ParseFromString(response.content)
        return platform_response
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

@mcp.tool("authentication-status")
def authentication_status():
    """
    Returns the authentication status of the user.
    Returns:
        dict: A json dictionary containing the authentication status of the user in key called status.
    """
    global authTicket
    if authTicket.stoken is not None:
        return """{"status": "authenticated"}"""
    return """{"status": "unauthenticated"}"""

@mcp.tool("login")
def login(email: str, password: str):
    """
    Logs in the user with the specified email and password to Gravity Sketch Cloud.
    Args:
        email (str): The email of the user.
        password (str): The password of the user.
    Returns:
        dict: A json dictionary containing:
            result: the result of the login operation,
            ticket: the authentication ticket if the login is successful and the expiry time of the ticket.
            authDetail: the authentication details of the user if the login is successful, which includes the user ID.
    """
    global authTicket  # Declare stoken as global to modify its value
    req = platform_rest.PlatformRestRequest()
    req.restType = platform_rest.PlatformRestType.LoginByEmail
    req.loginByEmailRequest.email = email
    req.loginByEmailRequest.password = password
    
    platform_response = make_request(req)
    
    # Deserialize the response binary stream into a PlatformRestResponse object
    if platform_response is not None:     
        if platform_response.loginResponse.result == login_rest.LoginResult.LoginSuccess:
            authTicket.stoken = platform_response.loginResponse.ticket.stoken
            authTicket.userId = platform_response.loginResponse.authDetail.userId
        return MessageToJson(platform_response.loginResponse)
    return """{"result": %s}""" % login_rest.LoginResult.LoginFailure

@mcp.tool("logout")
def logout():
    """
    Logs out the user from Gravity Sketch Cloud.
    Returns:
        dict: A json dictionary containing the result of the logout operation.
    """
    global authTicket
    if authTicket.stoken is None:
        return {"result": "NotAuthenticated", "errorMessage": "User is not authenticated."}
        
    req = platform_rest.PlatformRestRequest()
    req.restType = platform_rest.PlatformRestType.Logout    

    platform_response = make_request(req)
    if platform_response is not None and platform_response.errorCode == platform_rest.PlatformRestError.Ok:
        authTicket.stoken = None
        authTicket.userId = ""
        return """{"result": "success"}"""
    return """{"result": "failure"}"""

@mcp.tool("get-user-profile")
def get_user_profile():
    """
    Gets the user profile of the logged-in user.
    Returns:
        dict: A json dictionary containing
            result: the result of the operation
            userProfile: the user profile if the operation is successful. 
    """
    req = platform_rest.PlatformRestRequest()
    req.restType = platform_rest.PlatformRestType.GetLoggedInUserV2

    platform_response = make_request(req)
    if platform_response is not None and platform_response.errorCode == platform_rest.PlatformRestError.Ok:
        return """{"result": "success", "userProfile": %s}""" % MessageToJson(platform_response.getLoggedInUserResponseV2)
    return """{"result": "failure"}"""
    

@mcp.tool("list-docs")
def list_docs(folder: str, workspace: WorkSpace = WorkSpace.PRIVATE, page_size: int = 10, offset: int = 0):
    """
    Lists the documents in the specified folder from Gravity Sketch Cloud.
    Args:
        folder (str): The folder to list the documents from. Default is an empty string for the root folder.
        workspace (WorkSpace): The workspace to list the documents from. Default is WorkSpace.PRIVATE.
        page_size (int): The number of documents to list per page.
        offset (int): The offset of the documents to list.
    Returns:
        dict: A json dictionary containing:
            result: the result of the operation,
            docs: the list of documents if the operation is successful.
    """
    req = platform_rest.PlatformRestRequest()
    req.restType = platform_rest.PlatformRestType.ListDocs
    req.listDocsRequest.spaceId.ownerId = authTicket.userId
    req.listDocsRequest.spaceId.ownerIdType = gravi_model.IdType.UserId
    if workspace == WorkSpace.PRIVATE:
        req.listDocsRequest.spaceId.partitionId = authTicket.userId
        req.listDocsRequest.spaceId.partitionIdType = gravi_model.IdType.UserId
    else:
        # Shared workspace is not unsupported currently as orgs and teams are not exposed by mcp
        req.listDocsRequest.spaceId.partitionId = authTicket.userId
        # req.listDocsRequest.spaceId.partitionIdType = gravi_model.IdType.OrgTeamId   
        req.listDocsRequest.spaceId.partitionIdType = gravi_model.IdType.UserId

    req.listDocsRequest.folder = folder
    req.listDocsRequest.pageSize = page_size
    req.listDocsRequest.offset = offset
    
    platform_response = make_request(req)

    def summariseDoc(doc: gravi_model.DocumentTO):
        return {"documentId": doc.documentId, "name": doc.docName, "type": doc.docType, "size": doc.fileSize, "created": doc.createdBy}
    
    if platform_response is not None and platform_response.errorCode == platform_rest.PlatformRestError.Ok:
        response_summary = [summariseDoc(doc) for doc in platform_response.listDocsResponse.docs]
        return """{"result": "success", "documents": %s}""" % json.dumps(response_summary) # MessageToJson(platform_response.listDocsResponse)
    return """{"result": "failure"}"""

@mcp.tool("download-doc")
def download_doc(doc_id: str, destination_path: str):
    """
    Downloads the document with the specified ID to the specified destination path from Gravity Sketch Cloud.
    Args:
        doc_id (str): The ID of the document to download.
        destination_path (str): The path to save the downloaded document.
    Returns:
        dict: A json dictionary containing:
            result: the result of the operation,
            message: the message indicating the result of the operation.
    """
    req = platform_rest.PlatformRestRequest()
    req.restType = platform_rest.PlatformRestType.DownloadDoc
    req.downloadDocRequest.docId = doc_id

    platform_response = make_request(req)
    if platform_response is not None and platform_response.errorCode == platform_rest.PlatformRestError.Ok:
        download_url = platform_response.DownloadDocResponse.downloadUrl
        response = requests.get(download_url, stream=True)
        if response.status_code == 200:
            with open(destination_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            return """{"result": "success", "message": f"File downloaded to {%s}"}""" % destination_path
        else:
            return """{"result": "failure", "errorMessage": f"Failed to download file. HTTP {%s}"}""" % response.status_code

    return """{"result": "failure to get doc url"}"""

# Main execution

def main():
    """Run the MCP server"""
    mcp.run()

if __name__ == "__main__":
    main()

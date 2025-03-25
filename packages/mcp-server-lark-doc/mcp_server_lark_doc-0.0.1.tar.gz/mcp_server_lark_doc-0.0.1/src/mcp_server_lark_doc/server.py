import time
from mcp.server.fastmcp import FastMCP
import re
import lark_oapi as lark
from lark_oapi.api.docx.v1 import *
from lark_oapi.api.auth.v3 import *
from lark_oapi.api.wiki.v2 import *
import json
import os
import asyncio  # Add to imports at the beginning
from lark_oapi.api.search.v2 import *

# Get configuration from environment variables
# Add global variables below imports
LARK_APP_ID = os.getenv("LARK_APP_ID", "")
LARK_APP_SECRET = os.getenv("LARK_APP_SECRET", "")
token_lock = asyncio.Lock()  # Add token lock
TENANT_ACCESS_TOKEN = None
TOKEN_EXPIRES_AT = None
try:
    larkClient = client = lark.Client.builder() \
        .app_id(LARK_APP_ID) \
        .app_secret(LARK_APP_SECRET) \
        .log_level(lark.LogLevel.INFO) \
        .build()
except Exception as e:
    print(f"Failed to initialize Lark client: {str(e)}")
    larkClient = None

# Initialize FastMCP server
mcp = FastMCP("lark_doc")

@mcp.tool()
async def get_lark_doc_content(documentUrl: str) -> str:
    """Get Lark document content
    
    Args:
        documentUrl: Lark document URL
    """
    if not larkClient or not larkClient.auth or not larkClient.docx or not larkClient.wiki:
        return "Lark client not properly initialized"
                
    async with token_lock:
        current_token = TENANT_ACCESS_TOKEN
    if not current_token or await _check_token_expired():
        try:
            current_token = await _auth_flow()
        except Exception as e:
            return f"Failed to get user access token: {str(e)}"

    # 1. Extract document ID
    docMatch = re.search(r'/(?:docx|wiki)/([A-Za-z0-9]+)', documentUrl)
    if not docMatch:
        return "Invalid Lark document URL format"

    docID = docMatch.group(1)
    isWiki = '/wiki/' in documentUrl

    # 3. For wiki documents, need to make an additional request to get the actual docID
    if isWiki:
        # Construct request object
        wikiRequest: GetNodeSpaceRequest = GetNodeSpaceRequest.builder() \
            .token(docID) \
            .obj_type("wiki") \
            .build()
        wikiResponse: GetNodeSpaceResponse = larkClient.wiki.v2.space.get_node(wikiRequest)    
        if not wikiResponse.success():
            return f"Failed to get wiki document real ID: code {wikiResponse.code}, message: {wikiResponse.msg}"
            
        if not wikiResponse.data or not wikiResponse.data.node or not wikiResponse.data.node.obj_token:
            return f"Failed to get wiki document node info, response: {wikiResponse.data}"
        docID = wikiResponse.data.node.obj_token    

    # 4. Get actual document content
    docRequest: RawContentDocumentRequest = RawContentDocumentRequest.builder() \
        .document_id(docID) \
        .lang(0) \
        .build()

    # 发起请求
    docResponse: RawContentDocumentResponse = larkClient.docx.v1.document.raw_content(docRequest)

    if not docResponse.success():
        return f"Failed to get document content: code {docResponse.code}, message: {docResponse.msg}"
 
    if not docResponse.data or not docResponse.data.content:
        return f"Document content is empty, {docResponse}"
        
    return docResponse.data.content


# 添加一个检查 token 是否过期的函数
async def _check_token_expired() -> bool:
    """Check if the current token has expired"""
    async with token_lock:
        if not TOKEN_EXPIRES_AT or not TENANT_ACCESS_TOKEN:
            return True
        # 提前 60 秒认为 token 过期，以避免边界情况
        return time.time() + 60 >= TOKEN_EXPIRES_AT


async def _start_oauth_server() -> tuple[str, int]:
    """Start local server to handle OAuth callback"""
    
    try:
        request: InternalTenantAccessTokenRequest = InternalTenantAccessTokenRequest.builder() \
            .request_body(InternalTenantAccessTokenRequestBody.builder()
                .app_id(LARK_APP_ID)
                .app_secret(LARK_APP_SECRET)
                .build()) \
            .build()

        # 发起请求
        response: InternalTenantAccessTokenResponse = client.auth.v3.tenant_access_token.internal(request)

        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"client.auth.v3.tenant_access_token.internal failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return None, None

        tenant_access_token = json.loads(response.raw.content).get("tenant_access_token", None)
        tenant_access_token_expires_in = json.loads(response.raw.content).get("expire", None)

        # get unix timestamp in seconds
        tenant_access_token_expires_at = time.time() + tenant_access_token_expires_in

        return tenant_access_token, tenant_access_token_expires_at

    except Exception as e:
        lark.logger.error(f"Failed to get tenant access token: {str(e)}")
        return None, None


# Update _auth_flow to use the server
async def _auth_flow() -> str:
    """Internal method to handle Feishu authentication flow"""
    global TENANT_ACCESS_TOKEN, TOKEN_EXPIRES_AT
    
    async with token_lock:
        if TENANT_ACCESS_TOKEN and not await _check_token_expired():
            return TENANT_ACCESS_TOKEN

    if not larkClient:
        raise Exception("Lark client not properly initialized")
        
    token, expires_at = await _start_oauth_server()
    if not token:
        raise Exception("Failed to get user access token")
    
    TENANT_ACCESS_TOKEN = token
    TOKEN_EXPIRES_AT = expires_at
        
    return token
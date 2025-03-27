"""
Microsoft Graph API 邮件客户端模块
"""

import time
import requests
import functools
from typing import Dict, Any, Callable

from .config import config
from .code_utils import extract_verification_code


class GraphConfig:
    """Graph API 配置常量"""
    # API 端点
    TOKEN_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    MESSAGES_ENDPOINT = "https://graph.microsoft.com/v1.0/me/messages"
    
    # 默认请求头
    DEFAULT_HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}


def time_request(func: Callable) -> Callable:
    """
    请求耗时装饰器
    
    仅在启用计时时生效
    """
    @functools.wraps(func) # 保留原函数的元信息，不至于被 wrapper 替换
    def wrapper(self, *args, **kwargs):
        # 如果未启用计时，直接执行原函数
        if not config.get_timing_enabled():
            return func(self, *args, **kwargs)
        
        # 记录开始时间
        start_time = time.time()
        
        # 执行原函数
        result = func(self, *args, **kwargs)
        
        # 计算耗时（毫秒）
        elapsed_time = (time.time() - start_time) * 1000  # 转换为毫秒
        print(f"{func.__name__} 耗时: {elapsed_time:.2f} ms")
        
        return result
    
    return wrapper


class GraphMailClient:
    """Microsoft Graph API 邮件客户端类"""

    def __init__(self, client_id: str, refresh_token: str):
        """
        初始化邮件客户端
        
        参数:
            client_id: 应用程序客户端 ID
            refresh_token: 刷新令牌
        """
        self.client_id = client_id
        self.refresh_token = refresh_token
        self.access_token = ""
        # 代理配置
        self.proxies = config.get_proxies()
        self.verify_ssl = False if self.proxies else True
    
    @time_request
    def get_tokens(self) -> Dict[str, str]:
        """
        获取访问令牌和刷新令牌
        
        返回:
            包含 access_token 和 refresh_token 的字典
        """
        data = {
            "client_id": self.client_id,
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
        }

        try:
            response = requests.post(
                GraphConfig.TOKEN_URL, 
                data=data, 
                proxies=self.proxies,
                verify=self.verify_ssl
            )

            if response.status_code == 200:
                result = response.json()
                self.access_token = result.get("access_token", "")
                new_refresh_token = result.get("refresh_token", "")
                
                return {
                    "code": 0, 
                    "data": {"access_token": self.access_token, "refresh_token": new_refresh_token},
                    "message": "获取令牌成功"
                }
            else:
                error_msg = f"获取令牌失败: {response.status_code} - {response.text}"
                # print(error_msg)
                return {"code": -1, "data": {}, "message": error_msg}
        except Exception as e:
            error_msg = f"获取令牌异常: {str(e)}"
            # print(error_msg)
            return {"code": -1, "data": {}, "message": error_msg}

    @time_request
    def get_emails(self, only_latest: bool = True) -> Dict[str, Any]:
        """
        获取邮件
        
        参数:
            only_latest: 是否只获取最新一封邮件
            
        返回:
            邮件数据字典，包含 emails 和可能的 error
        """
        if not self.access_token:
            error_msg = "无法获取访问令牌，请检查凭据"
            # print(error_msg)
            return {"code": -1, "data": {}, "message": error_msg}

        # 构建请求头
        headers = {
            **GraphConfig.DEFAULT_HEADERS,
            "Authorization": f"Bearer {self.access_token}",
        }

        # 构建请求参数
        params = {
            "$top": 1 if only_latest else 10, # 如果不指定，最多返回10封邮件
            "$orderby": "receivedDateTime DESC", # 按接收时间降序排序
        }

        try:
            response = requests.get(
                GraphConfig.MESSAGES_ENDPOINT,
                headers=headers,
                params=params,
                proxies=self.proxies,
                verify=self.verify_ssl
            )

            if response.status_code == 200:
                raw_emails = response.json().get("value", [])
                processed_emails = [self._extract_data(email) for email in raw_emails]
                return {"code": 0, "data": processed_emails, "message": "获取邮件成功"}
            else:
                error_msg = f"获取邮件失败: {response.status_code} - {response.text}"
                # print(error_msg)
                return {"code": -1, "data": {}, "message": error_msg}
        except Exception as e:
            error_msg = f"获取邮件异常: {str(e)}"
            # print(error_msg)
            return {"code": -1, "data": {}, "message": error_msg}
    
    @time_request
    def get_latest_unread_email(self) -> Dict[str, Any]:
        """
        获取最新的一封未读邮件
        
        返回:
            包含邮件数据和可能的错误信息的字典
        """
        if not self.access_token:
            error_msg = "无法获取访问令牌，请检查凭据"
            # print(error_msg)
            return {"code": -1, "data": {}, "message": error_msg}

        # 构建请求头
        headers = {
            **GraphConfig.DEFAULT_HEADERS,
            "Authorization": f"Bearer {self.access_token}",
        }

        # 构建请求参数 - 筛选未读邮件，只获取最新的一封
        params = {
            "$filter": "isRead eq false",
            "$orderby": "receivedDateTime DESC",
            "$top": 1
        }
        
        # 获取超时配置
        timeout = config.get_unread_timeout()
        
        # 开始时间
        start_time = time.time()
        
        while True:
            try:
                response = requests.get(
                    GraphConfig.MESSAGES_ENDPOINT,
                    headers=headers,
                    params=params,
                    proxies=self.proxies,
                    verify=self.verify_ssl
                )

                if response.status_code == 200:
                    emails = response.json().get("value", [])
                    if emails:
                        # 处理字段，提取嵌套字段
                        processed_email = self._extract_data(emails[0])
                        return {"code": 0, "data": processed_email, "message": "获取未读邮件成功"}
                    
                    # 检查是否超时
                    current_time = time.time()
                    if current_time - start_time > timeout:
                        error_msg = f"等待未读邮件超时（{timeout}秒）"
                        # print(error_msg)
                        return {"code": -1, "data": {}, "message": error_msg}
                    
                    # 等待一秒后再次尝试
                    time.sleep(1)
                    continue
                else:
                    error_msg = f"获取未读邮件失败: {response.status_code} - {response.text}"
                    print(error_msg)
                    return {"code": -1, "data": {}, "message": error_msg}
            except Exception as e:
                error_msg = f"获取未读邮件异常: {str(e)}"
                print(error_msg)
                return {"code": -1, "data": {}, "message": error_msg}

    def _extract_data(self, email: Dict[str, Any]) -> Dict[str, Any]:
        """
        提取邮件字段
        
        参数:
            email: 邮件数据字典
            
        返回:
            包含提取数据的字典
        """
        return {
            "subject": email.get("subject"),
            "from": email.get("from", {}).get("emailAddress", {}).get("address"),
            "date": email.get("receivedDateTime"),
            "isRead": email.get("isRead"),
            "preview": email.get("bodyPreview"),
            "html": email.get("body", {}).get("content"),
        }


def with_client(func):
    """
    创建客户端并获取令牌的装饰器
    
    参数:
        func: 被装饰的函数
    
    返回:
        装饰后的函数
    """
    @functools.wraps(func)
    def wrapper(client_id: str, refresh_token: str, *args, **kwargs):
        # 创建客户端
        client = GraphMailClient(client_id, refresh_token)
        
        # 获取令牌
        result = client.get_tokens()
        if result["code"] != 0:
            return result
        
        # 设置访问令牌
        client.access_token = result["data"]["access_token"]
        
        # 调用原函数
        return func(client, *args, **kwargs)
    
    return wrapper


@with_client
def get_latest_unread_email(client: GraphMailClient) -> Dict[str, Any]:
    """
    获取最新未读邮件的便捷函数
    
    参数:
        client: 邮件客户端实例
        
    返回:
        包含邮件数据和可能的错误信息的字典
    """
    return client.get_latest_unread_email()


@with_client
def get_verification_code_from_email(client: GraphMailClient) -> Dict[str, Any]:
    """
    从最新未读邮件中获取验证码
    
    参数:
        client: 邮件客户端实例
        
    返回:
        包含验证码和可能的错误信息的字典
    """
    # 获取最新未读邮件
    result = client.get_latest_unread_email()
    if result["code"] != 0:
        return result
    
    email = result.get("data", {})
    if not email:
        return {"code": -1, "data": {}, "message": "没有未读邮件"}
    
    return extract_verification_code(email)


@with_client
def get_emails(client: GraphMailClient, only_latest: bool = True) -> Dict[str, Any]:
    """
    获取邮件的便捷函数
    
    参数:
        client: 邮件客户端实例
        only_latest: 是否只获取最新一封邮件
        
    返回:
        包含邮件列表和可能的错误信息的字典
    """
    return client.get_emails(only_latest=only_latest)

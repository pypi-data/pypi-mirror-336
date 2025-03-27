import re
from typing import Dict, Any, List
from graph_mail_client.config import config

def extract_verification_code(email: Dict[str, Any]) -> Dict[str, Any]:
    """
    从邮件内容中提取验证码
    
    参数:
        email: 邮件字典
        
    返回:
        包含验证码和可能的错误信息的字典
    """
    # 获取验证码配置
    verification_config = config.get_verification_config()
    keywords = verification_config.get("keywords", [])
    
    # 检查邮件内容是否包含关键词
    if not _has_verification_code(email, keywords):
        return {"code": -1, "data": {}, "message": "邮件内容不包含验证码关键词"}
    
    patterns = verification_config.get("patterns", [])

    # 尝试各种模式提取验证码
    for pattern in patterns:
        matches = re.findall(pattern, email["preview"])
        if matches:
            return {"code": 0, "data": {"code": matches[0]}, "message": "提取验证码成功"}
    
    return {"code": -1, "data": email.get("html", {}), "message": "未能从邮件中提取到验证码，返回源 html"}


def _has_verification_code(email: Dict[str, Any], keywords: List[str]) -> bool:
    """
    检查邮件是否包含验证码
    
    参数:
        email: 邮件字典
        keywords: 验证码关键词列表
        
    返回:
        是否包含验证码
    """
    # 检查主题和预览内容
    for field in ["subject", "preview"]:
        content = email.get(field, "").lower()
        if any(keyword.lower() in content for keyword in keywords):
            return True
    
    return False


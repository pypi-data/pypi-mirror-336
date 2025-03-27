"""
配置加载模块
"""

import yaml
from pathlib import Path
from typing import Dict, Any, List


class Config:
    """配置类，使用单例模式"""
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """加载配置文件"""
        config_path = Path(__file__).parent.parent / "config.yaml"
        
        # 确保配置文件存在
        if not config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_path}")
        
        # 加载配置文件
        with open(config_path, 'r', encoding='utf-8') as f:
            self._config = yaml.safe_load(f)
    
    def get(self, key_path, default=None):
        """
        通过路径获取配置值
        
        参数:
            key_path: 配置键路径，可以是字符串（用.分隔）或列表
            default: 默认值，如果配置不存在则返回此值
            
        返回:
            配置值或默认值
        """
        if isinstance(key_path, str):
            keys = key_path.split('.')
        else:
            keys = key_path
            
        value = self._config
        for key in keys:
            if not isinstance(value, dict) or key not in value:
                return default
            value = value[key]
        
        # 注意！如果键存在，但是没有值，会返回空字符串！这里让它返回默认值！
        return value if value is not "" else default
    
    def get_timing_enabled(self) -> bool:
        """
        获取是否启用请求计时
        
        返回:
            是否启用请求计时
        """
        return self.get("timing", False)
    
    def get_unread_timeout(self) -> int:
        """
        获取未读邮件超时时间
        
        返回:
            未读邮件超时时间（秒）
        """
        return self.get("mail.unread_timeout", 10)
    
    def get_verification_config(self) -> Dict[str, List[str]]:
        """
        获取验证码配置
        
        返回:
            验证码配置字典，包含 keywords 和 patterns 两个键
        """
        return self.get("mail.verification", {})
    
    def get_proxies(self) -> Dict[str, Any]:
        """获取代理配置"""
        return self.get("proxy", {})


# 创建全局配置实例，便于导入使用
config = Config()

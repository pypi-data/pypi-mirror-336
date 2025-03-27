# Graph Mail Client

Microsoft Graph API 邮件客户端，用于获取 Outlook 邮箱中的邮件。

## 功能特点

- 支持获取最新一封邮件或所有邮件
- 支持配置代理服务器
- 支持请求耗时统计
- 可作为 Python 库集成到其他项目中

## 安装方法

### 从源码安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/graph-mail-client.git
cd graph-mail-client

# 安装
pip install -e .
```

### 使用 pip 安装（发布后）

```bash
pip install graph-mail-client
```

## 配置

配置文件位于 `config.yaml`，支持以下配置项：

```yaml
# 调试模式配置
debug:
  enabled: true  # 是否启用调试模式
  timing: true   # 是否记录请求耗时
  
# 代理配置
proxy:
  enabled: true  # 是否使用代理
  http: "http://192.168.0.102:9000"
  https: "http://192.168.0.102:9000"
  verify_ssl: false  # 是否验证 SSL 证书
```

## 使用方法

### 作为 Python 库使用

```python
from graph_mail_client import GraphMailClient, get_emails

# 方法一：使用 GraphMailClient 类
client = GraphMailClient("YOUR_CLIENT_ID", "YOUR_REFRESH_TOKEN")
latest_emails = client.get_emails(only_latest=True)
all_emails = client.get_emails(only_latest=False)

# 方法二：使用便捷函数
latest_emails = get_emails("YOUR_CLIENT_ID", "YOUR_REFRESH_TOKEN", only_latest=True)
all_emails = get_emails("YOUR_CLIENT_ID", "YOUR_REFRESH_TOKEN", only_latest=False)
```

## 示例

请参考 `example.py` 文件，其中包含了详细的使用示例。

## 获取 Client ID 和 Refresh Token

1. 在 [Microsoft Azure Portal](https://portal.azure.com/) 注册应用程序
2. 获取 Client ID
3. 使用 OAuth 2.0 授权流程获取 Refresh Token

## 许可证

MIT

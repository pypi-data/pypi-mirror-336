# Amazon Listing Optimizer

基于MCP协议标准的亚马逊Listing优化服务，提供智能化的Listing优化建议。

## 功能特点

- 基于MCP协议标准开发
- 支持多市场（US, UK, DE, FR, IT, ES, JP, CA, MX, BR, AU, IN）
- 智能关键词分析
- 竞品分析
- 多版本优化建议
- 详细的优化理由说明

## 安装

```bash
npm install @modelcontextprotocol/server-amazon-listing
```

## 使用方法

### 1. 初始化配置

```bash
npx mcp-server-amazon-listing init
```

这将创建必要的配置文件和目录结构。

### 2. 启动服务

```bash
npx mcp-server-amazon-listing start
```

### 3. 优化Listing

```bash
npx mcp-server-amazon-listing optimize <ASIN> [--marketplace <MARKETPLACE_ID>]
```

例如：
```bash
npx mcp-server-amazon-listing optimize B0CKWM4F9Q --marketplace ATVPDKIKX0DER
```

### 4. 检查服务状态

```bash
npx mcp-server-amazon-listing health
```

## 配置说明

配置文件位于 `config/mcp_config.yaml`，包含以下主要配置项：

```yaml
server:
  host: "0.0.0.0"
  port: 8000
  log_level: "INFO"

database:
  host: "localhost"
  port: 5432
  name: "amazon_listing"
  user: "postgres"
  password: "your_password"

api:
  base_url: "https://api.example.com"
  api_key: "your_api_key"
  timeout: 30

optimization:
  max_competitors: 20
  min_keyword_rank: 1000
  max_title_length: 200
  max_bullet_length: 500
```

## 开发说明

### 环境要求

- Node.js >= 14.0.0
- Python >= 3.8
- PostgreSQL >= 12.0

### 本地开发

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/amazon-listing-optimizer.git
cd amazon-listing-optimizer
```

2. 安装依赖：
```bash
npm install
pip install -r requirements.txt
```

3. 运行测试：
```bash
npm test
pytest tests/
```

4. 启动开发服务器：
```bash
npm run dev
```

## API文档

### 健康检查

```http
POST /mcp/v1/execute
Content-Type: application/json

{
  "request_id": "test-001",
  "version": "1.0.0",
  "action": "health_check",
  "parameters": {}
}
```

### 优化Listing

```http
POST /mcp/v1/execute
Content-Type: application/json

{
  "request_id": "test-002",
  "version": "1.0.0",
  "action": "optimize_listing",
  "parameters": {
    "asin": "B0CKWM4F9Q",
    "marketplace_id": "ATVPDKIKX0DER"
  }
}
```

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

MIT License - 详见 LICENSE 文件

## 联系方式

- 项目维护者：[Your Name]
- 邮箱：[your.email@example.com]
- 项目链接：[https://github.com/yourusername/amazon-listing-optimizer](https://github.com/yourusername/amazon-listing-optimizer)

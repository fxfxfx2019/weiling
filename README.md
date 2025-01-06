# Weiling 项目

基于 FastAPI 和 MongoDB 的用户认证系统。

## 功能特性

- 用户注册和登录
- JWT 认证
- 用户信息管理
- 并发测试支持
- 密码强度验证
- 邮箱唯一性校验
- 完整的测试覆盖
- Docker 支持

## 技术栈

- Python 3.11
- FastAPI
- MongoDB
- JWT
- Docker
- pytest

## 项目结构

```
weiling/
├── app/                    # 应用主目录
│   ├── api/               # API路由层
│   │   ├── auth.py       # 认证相关路由
│   │   └── user.py       # 用户相关路由
│   ├── core/             # 核心功能层
│   │   ├── auth.py       # 认证核心功能
│   │   ├── config.py     # 配置管理
│   │   ├── database.py   # 数据库操作
│   │   ├── events.py     # 事件处理
│   │   └── security.py   # 安全相关
│   ├── models/           # 数据模型层
│   │   └── user.py       # 用户模型
│   ├── services/         # 服务层
│   │   └── user.py       # 用户服务
│   └── utils/            # 工具函数
│       └── helpers.py    # 通用辅助函数
├── tests/                # 测试目录
│   ├── user_test/       # 用户相关测试
│   ├── conftest.py      # 测试配置
│   └── run_tests.py     # 测试运行脚本
├── docs/                # 文档目录
│   └── api.md          # API文档
├── docker/             # Docker配置
│   ├── Dockerfile     # 应用容器配置
│   └── docker-compose.yml  # 容器编排配置
├── app.py              # 应用入口
├── requirements.txt    # 项目依赖
└── README.md          # 项目说明
```

## 快速开始

1. 克隆项目:

```bash
git clone https://github.com/yourusername/weiling.git
cd weiling
```

2. 安装依赖:

```bash
pip install -r requirements.txt
```

3. 配置环境变量:

创建 `.env` 文件并添加以下配置:

```env
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=weiling
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=10080
```

4. 启动服务:

本地开发：
```bash
python app.py
```

使用 Docker：
```bash
cd docker
docker-compose up -d
```

## API 文档

详细的 API 文档请参考 [docs/api.md](docs/api.md)。

主要接口：
- POST /api/auth/register - 用户注册
- POST /api/auth/login - 用户登录
- POST /api/auth/refresh - 刷新令牌
- GET /api/user/me - 获取用户信息
- PUT /api/user/me - 更新用户信息

## 测试

1. 运行单元测试:

```bash
pytest tests/
```

2. 运行特定测试:

```bash
# JWT认证测试
python tests/run_tests.py --jwt

# 用户API测试
python tests/run_tests.py --api

# 并发测试（指定用户数）
python tests/run_tests.py --concurrent 10
```

3. 运行所有测试并生成报告:

```bash
python tests/run_tests.py --all
```

## 开发指南

1. 代码风格
- 遵循 PEP 8 规范
- 使用类型注解
- 添加详细的文档字符串

2. 提交规范
- feat: 新功能
- fix: 修复问题
- docs: 文档更新
- test: 测试相关
- refactor: 代码重构

3. 分支管理
- main: 主分支，保持稳定
- develop: 开发分支
- feature/*: 功能分支
- bugfix/*: 修复分支

## 部署

1. 使用 Docker（推荐）:

```bash
cd docker
docker-compose up -d
```

2. 手动部署:

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 启动 MongoDB
# 启动应用
python app.py
```

## 贡献

欢迎提交 Issue 和 Pull Request。

## 许可证

MIT 
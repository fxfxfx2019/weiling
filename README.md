# 唯灵项目

唯灵项目是一个个性化的AI互动系统，用户将绑定专属的子AI，并与之进行互动以形成记忆与规则。

## 项目结构

```
weiling/
├── frontend/          # 前端代码
├── backend/           # 后端代码
├── docs/             # 项目文档
└── tests/            # 测试代码
```

## 技术栈

### 前端
- Vue 3
- Vite
- TypeScript
- Pinia (状态管理)
- Vue Router
- Element Plus (UI组件库)

### 后端
- Python 3.8+
- FastAPI
- MongoDB
- OpenAI API
- WebSocket

## 开发环境要求

- Node.js 16+
- Python 3.8+
- MongoDB 4.4+
- Docker & Docker Compose

## 快速开始

1. 克隆项目
```bash
git clone [项目地址]
cd weiling
```

2. 安装前端依赖
```bash
cd frontend
npm install
```

3. 安装后端依赖
```bash
cd backend
pip install -r requirements.txt
```

4. 启动开发服务器
```bash
# 前端
cd frontend
npm run dev

# 后端
cd backend
python main.py
```

## 功能特性

- 用户认证与授权
- AI互动与对话
- 记忆管理系统
- 个性化设置
- 实时对话
- 知识反馈与优化

## 开发规范

### Git 提交规范
- feat: 新功能
- fix: 修复
- docs: 文档更改
- style: 代码格式
- refactor: 重构
- test: 测试
- chore: 构建过程或辅助工具的变动

### 代码规范
- 前端遵循 Vue 3 风格指南
- 后端遵循 PEP 8 规范
- 所有代码必须通过 ESLint/Pylint 检查
- 提交前必须通过单元测试

## 项目文档

详细的项目文档位于 `docs` 目录：
- 项目描述
- API文档
- 数据库设计
- 部署指南

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

[待定] 
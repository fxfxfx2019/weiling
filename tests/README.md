# 测试说明文档

## 环境准备

### 1. 启动MongoDB
```bash
# 进入项目目录
cd weiling

# 启动MongoDB容器
docker-compose up -d mongo
```

MongoDB连接信息：
- URL: mongodb://localhost:27017
- 数据库名: weiling
- 默认无需认证
- 数据库版本要求：4.4+

### 2. 启动后端服务
```bash
# 进入项目目录
cd weiling

# 启动服务
python app.py
```
服务将在 http://localhost:8000 启动

## API规则说明

### 1. 用户注册
- 接口：POST `/api/user/register`
- 请求格式：
```json
{
    "username": "用户名",  // 必填，长度3-32字符，只允许字母、数字、下划线，必须以字母开头
    "email": "邮箱",      // 必填，有效的邮箱格式，最大长度64字符
    "password": "密码"    // 必填，长度8-32字符，必须包含大小写字母和数字
}
```

- 验证规则：
  - 用户名：
    - 长度：3-32字符
    - 格式：^[a-zA-Z][a-zA-Z0-9_]*$
    - 唯一性：数据库中不能存在相同用户名
    - 不允许使用的关键字：admin, root, system 等
  
  - 邮箱：
    - 格式：必须是有效的邮箱格式
    - 长度：最大64字符
    - 唯一性：数据库中不能存在相同邮箱
    - 域名验证：必须包含有效的域名部分
  
  - 密码：
    - 长度：8-32字符
    - 复杂度：必须包含大小写字母和数字
    - 特殊字符：允许但不强制要求
    - 不允许包含用户名
    - 不允许连续重复字符超过3次

- 响应格式：
```json
{
    "id": "string",          // MongoDB ObjectId字符串
    "username": "string",    // 用户名
    "email": "string",       // 邮箱
    "avatar": "string|null", // 头像URL，可为null
    "bind_status": false,    // 是否绑定AI，布尔值
    "sub_ai_id": "string|null", // 绑定的AI ID，可为null
    "created_at": "string",  // ISO格式的创建时间
    "updated_at": "string",  // ISO格式的更新时间
    "status": "string",      // 用户状态：active/inactive/banned
    "version": "integer"     // 数据版本号
}
```

- 错误响应：
```json
{
    "detail": {
        "code": "string",    // 错误代码
        "message": "string", // 错误信息
        "fields": {          // 字段错误详情（可选）
            "field_name": ["错误信息"]
        }
    }
}
```

### 2. 用户登录
- 接口：POST `/api/user/login`
- 请求格式：form-data
```
username: 用户名或邮箱（必填，3-64字符）
password: 密码（必填，8-32字符）
grant_type: 授权类型（可选，默认为"password"）
scope: 权限范围（可选，默认为空）
client_id: 客户端ID（可选）
client_secret: 客户端密钥（可选）
```

- 验证规则：
  - 用户名/邮箱：
    - 支持用户名或邮箱登录
    - 大小写不敏感
    - 自动移除首尾空格
  
  - 密码：
    - 大小写敏感
    - 不允许空格
    - 失败次数限制：5次/小时
    - 账户锁定：连续失败5次后锁定30分钟

- 响应格式：
```json
{
    "access_token": "string",   // JWT访问令牌
    "refresh_token": "string",  // JWT刷新令牌
    "token_type": "string",     // 令牌类型，固定为"bearer"
    "expires_in": integer,      // 访问令牌有效期（秒）
    "scope": "string|null",     // 权限范围（可选）
    "user": {                   // 用户基本信息（可选）
        "id": "string",
        "username": "string",
        "email": "string",
        "avatar": "string|null"
    }
}
```

### 3. JWT认证
- 访问令牌（Access Token）：
  - 有效期：30分钟
  - 格式：JWT格式
  - 载荷（Payload）：
    ```json
    {
        "sub": "string",    // 用户名
        "exp": integer,     // 过期时间戳
        "iat": integer,     // 签发时间戳
        "type": "access",   // 令牌类型
        "jti": "string"     // 令牌唯一标识符
    }
    ```

- 刷新令牌（Refresh Token）：
  - 有效期：7天
  - 格式：JWT格式
  - 载荷（Payload）：
    ```json
    {
        "sub": "string",    // 用户名
        "exp": integer,     // 过期时间戳
        "iat": integer,     // 签发时间戳
        "type": "refresh",  // 令牌类型
        "jti": "string"     // 令牌唯一标识符
    }
    ```

- 令牌刷新：
  - 接口：POST `/api/user/refresh`
  - 请求格式：
    ```json
    {
        "refresh_token": "string"  // 有效的刷新令牌
    }
    ```
  - 响应格式：
    ```json
    {
        "access_token": "string",   // 新的访问令牌
        "refresh_token": "string",  // 原刷新令牌或新的刷新令牌
        "token_type": "bearer"
    }
    ```

### 4. 用户信息更新
- 接口：PUT `/api/user/profile`
- 需要认证：是（Bearer Token）
- 请求格式：
```json
{
    "nickname": "string",     // 可选，2-32字符，允许中文
    "avatar": "string",      // 可选，有效的URL格式，最大长度256字符
    "bio": "string",         // 可选，个人简介，最大长度500字符
    "gender": "string",      // 可选，male/female/other
    "birthday": "string",    // 可选，ISO格式日期
    "location": "string",    // 可选，最大长度100字符
    "website": "string"      // 可选，有效的URL格式，最大长度256字符
}
```

- 验证规则：
  - nickname：
    - 长度：2-32字符
    - 允许中文、字母、数字、下划线
    - 敏感词过滤
  
  - avatar：
    - 必须是有效的URL格式
    - 支持的图片格式：jpg, jpeg, png, gif
    - 文件大小限制：2MB
  
  - bio：
    - 最大长度：500字符
    - 支持基本HTML标签
    - 敏感词过滤
  
  - website：
    - 必须是有效的URL格式
    - 必须包含协议（http/https）

- 响应格式：
```json
{
    "id": "string",
    "username": "string",
    "email": "string",
    "nickname": "string|null",
    "avatar": "string|null",
    "bio": "string|null",
    "gender": "string|null",
    "birthday": "string|null",
    "location": "string|null",
    "website": "string|null",
    "updated_at": "string"
}
```

### 5. 密码修改
- 接口：POST `/api/user/password/change`
- 需要认证：是（Bearer Token）
- 请求格式：
```json
{
    "current_password": "string",  // 当前密码
    "new_password": "string",      // 新密码
    "confirm_password": "string"   // 确认新密码
}
```

- 验证规则：
  - current_password：
    - 必须与当前密码匹配
    - 连续失败3次后需要重新登录
  
  - new_password：
    - 长度：8-32字符
    - 必须包含大小写字母和数字
    - 不能与最近3次使用的密码相同
    - 不能与当前密码相同
    - 复杂度要求同注册密码
  
  - confirm_password：
    - 必须与new_password完全匹配

- 响应格式：
```json
{
    "message": "string",     // 成功消息
    "timestamp": "string",   // 修改时间
    "require_relogin": true  // 是否需要重新登录
}
```

## 测试命令

### 运行所有测试
```bash
python tests/run_tests.py --all
```

### 运行特定测试
```bash
# JWT认证测试
python tests/run_tests.py --jwt

# 用户API测试
python tests/run_tests.py --user

# 基础API测试
python tests/run_tests.py --basic

# AI功能测试
python tests/run_tests.py --ai

# 并发测试（可指定用户数）
python tests/run_tests.py --concurrent 100
```

## 测试文件说明

1. `test_jwt_flow.py`
   - JWT认证完整流程测试
   - 包含：注册、登录、令牌验证、令牌刷新等

2. `test_user_api.py`
   - 用户API功能测试
   - 包含：注册、登录、密码修改等

3. `test_api_basic.py`
   - 基础API功能测试
   - 包含：用户名登录、邮箱登录、信息获取等

4. `test_user_concurrent.py`
   - 并发性能测试
   - 测试用户系统在高并发下的表现

5. `test_ai.py`
   - AI功能测试
   - 包含：代码解释等AI相关功能

## 注意事项

1. 测试前确保：
   - MongoDB已正常启动
   - 后端服务正常运行
   - 环境变量配置正确（.env文件）

2. 测试数据：
   - 测试会自动生成临时用户
   - 用户名和邮箱使用时间戳确保唯一性
   - 测试完成后数据会保留在数据库中

3. 错误处理：
   - 所有测试都包含错误处理机制
   - 测试失败会显示具体原因
   - 单个测试失败不影响其他测试

4. 并发测试：
   - 默认并发用户数：100
   - 可通过参数调整并发量
   - 建议先进行小规模测试 
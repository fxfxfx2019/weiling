# API 文档

## 概述

本文档描述了用户认证系统的 API 接口。所有接口使用 JSON 格式进行数据交换，基础路径为 `/api`。

## 认证机制

系统使用 JWT (JSON Web Token) 进行认证。访问受保护的接口时，需要在请求头中添加 `Authorization: Bearer {token}` 。

## 错误响应

所有接口在发生错误时会返回以下格式：

```json
{
  "detail": "错误信息描述"
}
```

常见状态码：
- 200: 成功
- 201: 创建成功
- 400: 请求参数错误
- 401: 未认证或认证失败
- 422: 数据验证错误

## 认证相关接口

### 用户注册

```http
POST /api/auth/register
```

注册新用户。

请求体:
```json
{
  "username": "string",     // 用户名，必填，唯一
  "email": "user@example.com",  // 邮箱，必填，唯一
  "password": "string",     // 密码，必填，至少8位，包含字母和数字
  "nickname": "string"      // 昵称，必填
}
```

成功响应 (201):
```json
{
  "username": "string",
  "email": "user@example.com",
  "nickname": "string",
  "_id": "string",
  "is_admin": false,
  "is_active": true,
  "created_at": "2023-12-31T12:00:00",
  "updated_at": "2023-12-31T12:00:00"
}
```

错误响应：
- 400: 用户名或邮箱已存在
- 422: 请求数据验证失败

### 用户登录

```http
POST /api/auth/login
```

用户登录获取令牌。

请求体:
```json
{
  "username": "string",  // 用户名
  "password": "string"   // 密码
}
```

成功响应 (200):
```json
{
  "access_token": "string",   // 访问令牌
  "refresh_token": "string",  // 刷新令牌
  "token_type": "bearer"      // 令牌类型
}
```

错误响应：
- 401: 用户名或密码错误
- 422: 请求数据验证失败

### 刷新令牌

```http
POST /api/auth/refresh
```

使用刷新令牌获取新的访问令牌。

请求体:
```json
{
  "refresh_token": "string"  // 刷新令牌
}
```

成功响应 (200):
```json
{
  "access_token": "string",  // 新的访问令牌
  "token_type": "bearer"     // 令牌类型
}
```

错误响应：
- 401: 无效的刷新令牌

## 用户相关接口

### 获取当前用户信息

```http
GET /api/user/me
```

获取当前登录用户的信息。

请求头:
```
Authorization: Bearer {access_token}
```

成功响应 (200):
```json
{
  "username": "string",
  "email": "user@example.com",
  "nickname": "string",
  "_id": "string",
  "is_admin": false,
  "is_active": true,
  "created_at": "2023-12-31T12:00:00",
  "updated_at": "2023-12-31T12:00:00"
}
```

错误响应：
- 401: 未认证或令牌无效

### 更新当前用户信息

```http
PUT /api/user/me
```

更新当前登录用户的信息。

请求头:
```
Authorization: Bearer {access_token}
```

请求体:
```json
{
  "email": "user@example.com",  // 可选
  "nickname": "string",         // 可选
  "password": "string"          // 可选，更新密码
}
```

成功响应 (200):
```json
{
  "username": "string",
  "email": "user@example.com",
  "nickname": "string",
  "_id": "string",
  "is_admin": false,
  "is_active": true,
  "created_at": "2023-12-31T12:00:00",
  "updated_at": "2023-12-31T12:00:00"
}
```

错误响应：
- 400: 邮箱已被使用
- 401: 未认证或令牌无效
- 422: 请求数据验证失败 
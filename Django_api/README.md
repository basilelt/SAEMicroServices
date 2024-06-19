# Airline Reservation System API

This project is a microservices-based airline reservation system. The system allows clients to view flights, make reservations, and manage their bookings. Staff members can manage flights, airports, planes, and view all bookings. The project is structured into three main services: `api_client`, `api_staff`, and `api_common`.

## API Overview

### API Client

The `api_client` service handles all client-side operations, including user registration, login, viewing flights, and managing user-specific bookings.

#### Endpoints

- **Register**: `/api/client/register/`
  - Method: POST
  - Description: Registers a new user.

- **Login**: `/api/client/login/`
  - Method: POST
  - Description: Authenticates a user and returns JWT tokens.

- **User List**: `/api/client/users/`
  - Method: GET
  - Description: Retrieves a list of all users. (Admin only)

- **Update User**: `/api/client/update-user/<int:pk>/`
  - Method: PUT
  - Description: Updates user details.

- **Delete User**: `/api/client/delete-user/<int:pk>/`
  - Method: DELETE
  - Description: Deletes a user.

- **Flight List**: `/api/client/flights/`
  - Method: GET
  - Description: Retrieves a list of all available flights.

- **User Booking List**: `/api/client/bookings/`
  - Method: GET
  - Description: Retrieves a list of all bookings made by the authenticated user.

- **User Booking Detail**: `/api/client/bookings/<int:pk>/`
  - Method: GET, PUT, DELETE
  - Description: Retrieves, updates, or deletes a specific booking made by the authenticated user.

### API Staff

The `api_staff` service handles all staff-side operations, including managing flights, airports, planes, and viewing all bookings.

#### Endpoints

- **Add Flight**: `/api/staff/add-flight/`
  - Method: POST
  - Description: Adds a new flight.

- **Delete Flight**: `/api/staff/delete-flight/<int:pk>/`
  - Method: DELETE
  - Description: Deletes a flight.

- **Update Flight**: `/api/staff/update-flight/<int:pk>/`
  - Method: PUT
  - Description: Updates a flight's details.

- **Flight List**: `/api/staff/flights/`
  - Method: GET
  - Description: Retrieves a list of all flights.

- **Staff Login**: `/api/staff/login/`
  - Method: POST
  - Description: Authenticates a staff member and returns JWT tokens.

- **Airport List**: `/api/staff/airports/`
  - Method: GET
  - Description: Retrieves a list of all airports.

- **Airport Detail**: `/api/staff/airports/<int:pk>/`
  - Method: GET, PUT, DELETE
  - Description: Retrieves, updates, or deletes a specific airport's details.

- **Plane List**: `/api/staff/planes/`
  - Method: GET
  - Description: Retrieves a list of all planes.

- **Plane Detail**: `/api/staff/planes/<int:pk>/`
  - Method: GET, PUT, DELETE
  - Description: Retrieves, updates, or deletes a specific plane's details.

- **Booking List**: `/api/staff/bookings/`
  - Method: GET
  - Description: Retrieves a list of all bookings.


# 航班预订系统 API

本项目是一个基于微服务的航班预订系统。系统允许客户查看航班、进行预订和管理他们的预订。工作人员可以管理航班、机场、飞机，并查看所有的预订记录。项目主要分为三个服务：`api_client`、`api_staff`和`api_common`。

## API 概述

### API 客户端

`api_client`服务处理所有客户端操作，包括用户注册、登录、查看航班和管理用户特定的预订。

#### 端点

- **注册**: `/api/client/register/`
  - 方法: POST
  - 描述: 注册新用户。

- **登录**: `/api/client/login/`
  - 方法: POST
  - 描述: 认证用户并返回JWT令牌。

- **用户列表**: `/api/client/users/`
  - 方法: GET
  - 描述: 获取所有用户的列表。（仅管理员）

- **更新用户**: `/api/client/update-user/<int:pk>/`
  - 方法: PUT
  - 描述: 更新用户详细信息。

- **删除用户**: `/api/client/delete-user/<int:pk>/`
  - 方法: DELETE
  - 描述: 删除用户。

- **航班列表**: `/api/client/flights/`
  - 方法: GET
  - 描述: 获取所有可用航班的列表。

- **用户预订列表**: `/api/client/bookings/`
  - 方法: GET
  - 描述: 获取当前认证用户的所有预订列表。

- **用户预订详情**: `/api/client/bookings/<int:pk>/`
  - 方法: GET, PUT, DELETE
  - 描述: 获取、更新或删除当前认证用户的特定预订。

### API 工作人员

`api_staff`服务处理所有工作人员操作，包括管理航班、机场、飞机和查看所有预订记录。

#### 端点

- **添加航班**: `/api/staff/add-flight/`
  - 方法: POST
  - 描述: 添加新航班。

- **删除航班**: `/api/staff/delete-flight/<int:pk>/`
  - 方法: DELETE
  - 描述: 删除航班。

- **更新航班**: `/api/staff/update-flight/<int:pk>/`
  - 方法: PUT
  - 描述: 更新航班详细信息。

- **航班列表**: `/api/staff/flights/`
  - 方法: GET
  - 描述: 获取所有航班的列表。

- **登录**: `/api/staff/login/`
  - 方法: POST
  - 描述: 认证工作人员并返回JWT令牌。

- **机场列表**: `/api/staff/airports/`
  - 方法: GET
  - 描述: 获取所有机场的列表。

- **机场详情**: `/api/staff/airports/<int:pk>/`
  - 方法: GET, PUT, DELETE
  - 描述: 获取、更新或删除特定机场的详细信息。

- **飞机列表**: `/api/staff/planes/`
  - 方法: GET
  - 描述: 获取所有飞机的列表。

- **飞机详情**: `/api/staff/planes/<int:pk>/`
  - 方法: GET, PUT, DELETE
  - 描述: 获取、更新或删除特定飞机的详细信息。

- **预订列表**: `/api/staff/bookings/`
  - 方法: GET
  - 描述: 获取所有预订的列表。

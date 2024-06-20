API 端点设计
用户管理
注册
端点: /api/register/
方法: POST
描述: 注册新用户。
请求参数:
username: string
password: string
email: string
登录
端点: /api/login/
方法: POST
描述: 认证用户并返回JWT令牌。
请求参数:
username: string
password: string
获取用户列表（仅管理员）
端点: /api/users/
方法: GET
描述: 获取所有用户的列表。
更新用户
端点: /api/users/<int:pk>/
方法: PUT
描述: 更新用户详细信息。
请求参数:
email: string
is_staff: boolean
is_superuser: boolean
删除用户
端点: /api/users/<int:pk>/
方法: DELETE
描述: 删除用户。
航班管理
获取所有航班
端点: /api/flights/
方法: GET
描述: 获取所有可用航班的列表。
添加新航班（仅工作人员）
端点: /api/flights/
方法: POST
描述: 添加新航班。
请求参数:
flight_number: string
departure: datetime
arrival: datetime
plane: int (plane ID)
track_origin: int (track ID)
track_destination: int (track ID)
更新航班信息（仅工作人员）
端点: /api/flights/<int:pk>/
方法: PUT
描述: 更新航班详细信息。
请求参数:
flight_number: string
departure: datetime
arrival: datetime
plane: int (plane ID)
track_origin: int (track ID)
track_destination: int (track ID)
删除航班（仅工作人员）
端点: /api/flights/<int:pk>/
方法: DELETE
描述: 删除航班。
预订管理
获取用户预订列表
端点: /api/bookings/
方法: GET
描述: 获取当前认证用户的所有预订列表。
获取预订详情
端点: /api/bookings/<int:pk>/
方法: GET
描述: 获取特定预订的详细信息。
创建预订
端点: /api/bookings/
方法: POST
描述: 创建新预订。
请求参数:
price: float
booking_type: int (booking type ID)
client: int (client ID)
flight: int (flight ID)
更新预订
端点: /api/bookings/<int:pk>/
方法: PUT
描述: 更新预订详细信息。
请求参数:
price: float
booking_type: int (booking type ID)
flight: int (flight ID)
删除预订
端点: /api/bookings/<int:pk>/
方法: DELETE
描述: 删除预订。
机场管理（仅工作人员）
获取所有机场
端点: /api/airports/
方法: GET
描述: 获取所有机场的列表。
获取机场详情
端点: /api/airports/<int:pk>/
方法: GET
描述: 获取特定机场的详细信息。
添加机场
端点: /api/airports/
方法: POST
描述: 添加新机场。
请求参数:
name: string
location: string
更新机场信息
端点: /api/airports/<int:pk>/
方法: PUT
描述: 更新机场详细信息。
请求参数:
name: string
location: string
删除机场
端点: /api/airports/<int:pk>/
方法: DELETE
描述: 删除机场。
飞机管理（仅工作人员）
获取所有飞机
端点: /api/planes/
方法: GET
描述: 获取所有飞机的列表。
获取飞机详情
端点: /api/planes/<int:pk>/
方法: GET
描述: 获取特定飞机的详细信息。
添加飞机
端点: /api/planes/
方法: POST
描述: 添加新飞机。
请求参数:
model: string
second_class_capacity: int
first_class_capacity: int
更新飞机信息
端点: /api/planes/<int:pk>/
方法: PUT
描述: 更新飞机详细信息。
请求参数:
model: string
second_class_capacity: int
first_class_capacity: int
删除飞机
端点: /api/planes/<int:pk>/
方法: DELETE
描述: 删除飞机。
所有预订记录（仅工作人员）
获取所有预订记录
端点: /api/all-bookings/
方法: GET
描述: 获取所有预订记录的列表。
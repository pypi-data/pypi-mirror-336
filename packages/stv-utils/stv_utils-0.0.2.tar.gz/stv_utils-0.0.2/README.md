# stv_utils

一个包含常用实用函数的Python库。

## 功能列表

- **`is_ch()`**  
  检测当前系统是否为Windows且中文环境。  
  *返回类型*: `bool`

- **`system_check()`**  
  检查当前操作系统是否为Windows。  
  *返回类型*: `bool`

- **`is_idle()`**  
  判断当前是否在IDLE环境中运行。  
  *返回类型*: `bool`

- **`system_clear()`**  
  根据系统执行清屏命令（Windows使用`cls`，其他系统使用`clear`），若在IDLE中则跳过。

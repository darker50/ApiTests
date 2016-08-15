# ApiTests
**ApiTests**是一个快速验证接口正确性的框架，主要用于回归验证，亦可用于接口测试（需要拓展，目前还未支持，考虑后面加上）。



#### 关于这个框架

**设计初衷：**

解决我们项目的接口测试痛点。从之前的1-2小时测试时间压缩到现在的1分钟以内，效率提升，效果显著

**对于读者：**

- 完全符合你们项目
  - 庆幸的是入手即用，方便快捷
  - 需要注意的是，不要做伸手党，可以了解这个框架后，再去针对性的优化，让它更符合你们项目
- 部分符合你们项目
  - 提取出部分内容，加入到你们项目中
- 完全不符合你们项目
  - 提供一种思路，虽然可能没什么用，但是能了解到别人对这件事是怎么思考的

**关于框架代码结构：**

- 非程序出身，能写成这样我自己还是比较满意的
- 结构设计可能有些问题，但是不影响使用
  - 如发现设计不合理之处，欢迎指正
  - 先出成果再作优化


- 此框架服务于测试流程、效率，是一个工具
- 至少目前认为手工+自动化才是最符合我们项目

#### 功能

具体查看框架思路

- 接口只需录制一次，后续只需维护变动的接口


- 目前仅支持http的post请求方式，get以及https后续考虑加上，亦可自己完善
- 快速的接口反馈，通常一分钟内完成，取决于机器/网络因素
- 日常监控，后续加上
- 可以屏蔽特殊接口
- 创建的数据清理
- 重试机制


#### 接口流程走向

```
接口回归测试启动...
读取配置文件中...
读取接口数据中...
接口请求中，请等待...
接口请求完成！
发现diff接口，重试机制启动...
读取配置文件中...
diff sessions: iscanchatbymulit.txt
发现录制异常接口：iscanchatbymulit.txt
执行移除操作，移除重试队列
diff sessions: GetGroupDynamicCommentList.txt
发现录制异常接口：GetGroupDynamicCommentList.txt
执行移除操作，移除重试队列
第1次尝试请求diff...
diff请求完成...
正在整理创建的数据...
清理创建的接口数据...
读取配置文件中...
接口数据清理完成！
测试报告准备中...
接口回归测试完成！
耗时： 21s
```

#### 请求接口后写入本地的数据说明

```
FieldChange >> 字段改变的接口写入该文件
ProgramCrash >> 程序异常接口写入该文件
Unexpected >> 未达到预期字段校验的接口写入该文件
VerifyRequest >> 需要再次确认的接口写入该文件
GetUserInfoV2 >> 正常接口（一个接口一个文件）
```



#### 关于接口回放的数据

- 第一次的数据来自fiddler录制
- 第二次及以后的数据来自第一次请求写入本地的正常接口文件 + fiddler继续录制需要检查的接口
- 一般来说不要一直拿第一次fiddler录制的数据使用，目的在于测试接口对各个客户端版本的兼容情况
- 接口回放可以跑线上运行的客户端全部版本接口（一个版本一套接口）

#### 框架的下一步

- 优雅的Html报告
- 邮件通知
- 持续集成
- 测试数据另存，方便后续查阅

#### 框架的更下一步

- 接口压测
- 接口自动化（api测试）pass：目前只是回归验证
- 简单的GUI界面


#### 框架思路

![ApiTests 框架思路](./http api test.jpg)



#### 使用方式

- 环境配置
  - Python 3.x
  - fiddler一枚（配置抓取手机请求）
  - PyCharm 


- 替换fiddler js

  - 项目根目录的fiddler js整个文件内容替换fiddler的js
    - 打开fiddler的Customize Rules功能
    - 删除所有内容，并把fiddler js内容全部拷贝进去
    - 修改拦截的host等信息
    - [fiddler保存请求](https://testerhome.com/topics/5481)

  fiddler js自定义信息

  ```javascript

  	//自定义参数设置
  	public static var filterUrl = "a-webapi.test.b.com";
  	public static var filePath = "D:\\Fiddler Sessions\\Api\\";
  	public static var filePathForRequested = "D:\\Fiddler Sessions\\Requested.txt";
  	public static var filePathForErrorResponse = "D:\\Fiddler Sessions\\ErrorResponse.txt";
  	public static var filePathForVerifyRequset = "D:\\Fiddler Sessions\\VerifyRequset.txt";
  	public static var filePathForRemoveSession = "D:\\Fiddler Sessions\\RemoveSession.txt";
  	public static var filePathForAddSession = "D:\\Fiddler Sessions\\AddSession.txt";
  ```

  ​

- token/session替换

  - 替换成你们项目对应的token等
  - 修改配置文件
  - 修改response body json 判断逻辑


- 运行方式
  - 总入口在项目的launcher文件夹下面的RequestApi.py
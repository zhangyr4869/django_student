django 学生管理
===
学完官网投票教程后的实战项目。使用之前所有知识的综合。

任务：
1. 创建项目
2. 创建 "admin", "student", "teacher",等app
3. student下创建表结构："student(id,no,name,age,gender,avatar,phone,class_id,teacher_id,join_time,备注)" "classes(id,no,name,grade，capacity，address)" "teacher(id,no,name,age,gender,avatar,salary,subject,address,phone)"

### 表结构
表名 student
字段名    字段类型      含义         值示例         备注       
id         integer      表id主键
no         integer      学号        0001        (111100001111110 biginteger)  如果整数存储学号、vip会员号，考虑长度。或用字符串类型。
name        char
age        smallint_positive      默认-125 125，正数0-255        (选做)数据库约束，0-150岁， 搞不清楚，一般情况int。长数字用bigint。
gender     integer                  smallinteger(0未填写1男2女3xx) 或 char(4) 'male' 'female' 或 bool（false 女 True 男） 三种设计方案均可
phone      int或char               +8613733177926     0371-56662222  400-300-222111
avatar     char            头像     'd:/project/static/xxxavatar.jpg'   request.POST.['file''] .read()  open('.jpg'')  write() 得到一张图表，把路径存到数据库表
join_time   datetiem    添加/入学时间     
last_modified_time  datetiem   上次修改时间
[fk]class_id    学生所在班级

class表
id
no   001
name   三年二班
grade  年级
capacity  容纳
address  xx校区xx号教学楼


teacher表
一些字段同student 。可以用继承，但表较少，看表结构时还需要看两个类，这里没必要用。
salary  工资
subject     主讲科目


student-teacher  多对多
id 
fk]student_id       1
fk]teacher_id       2


结论：一对多关系，多的一方建立外键
多对多关系， 新建第三张表（id, t1_id, t2_id）,包含两表的外键。



基础需求：
0. 使用bootstrap成熟的web
1. 放着自带的后台管理，实现学生管理（增删改查）
2. 分页
追加需求：
1. excel导入导出功能
2. 教师管理，班级管理
3. 过滤查找
4. 注册登录
5. 权限
6. 附件
7. 访问量
新知识：
分页，
excel导入导出

后续：
接口，手机短信，登录注册（session cookie）和权限



## 任务
第一天： 
1. 需求分析
2. 创建表结构
3. 新建django项目和app和模板、静态文件夹
4. 生成迁移脚本
5. 执行内置app和自定义模块的脚本
6. 写一个首页，配置全局url和app中的url和视图函数和index.html，跑通。
7. index.html书写学生列表，引入bootstrap4和fontawesome图标
8. 注册model，创建后台管理员，添加5个学生测试数据
9. 完成views.index(),前台的数据变为数据库取出的数据，完成学生列表功能。

第二天:
1. 添加功能
2. 修改
3. 删除
（选做）追加需求，添加表单的学号列 自动生成下一个学号即数据库已存在学号的最大值+1。
（选做），do_add时判断用户输入数据是否合法，如学号是否重复。 如果错误重定向到添加表单页并在某处红字提示错误信息。
（选做 优先级较低），限制用户上传文件的后缀为.jpg或.png，不大于2MB。
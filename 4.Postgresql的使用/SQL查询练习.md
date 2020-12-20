# sql 查询
1. 找出所有供应商(S)的姓名和所在的城市；
2. 找出所有零件的名称，颜色和重量；
3. 找出使用供应商S1所供应零件的工程号码；



----
1. 在零件表的视图中找出weight < 20 的零件名字(PNAME)
2. 查询供应商表(S)中城市为北京的供应商姓名(SNAME) 
3. 在零件表中查询平均重量在15以上的零件名字(PNAME)和零件代码（PNO）
groupby p_number
为什么要groupby ，因为需要聚集函数(AVG),正也因为AVG函数，更需要GROUPBY了。
4. 查询全体供应商的姓名（SNAME）和状态(STATUS)
5. 查询所有weight在13到20（含13和20）的零件代码（PNO）、零件名（PNAME）和颜色(COLOR)
6. 查询所有“螺”开头的的零件代码（PNO）和零件名（PNAME）
7. 查询所有零件的平均重量
8. 查询同在“天津”的工程项目名（JNAME）
9. 查询在“精益”供应商下的零件，且质量小于15的零件详细信息

---
create table Student(Sid varchar(10),Sname varchar(10),Sage varchar(15),Ssex nvarchar(10));
insert into Student values('01' , '赵雷' , '1990-01-01' , '男');
insert into Student values('02' , '钱电' , '1990-12-21' , '男');
insert into Student values('03' , '孙风' , '1990-05-20' , '男');
insert into Student values('04' , '李云' , '1990-08-06' , '男');
insert into Student values('05' , '周梅' , '1991-12-01' , '女');
insert into Student values('06' , '吴兰' , '1992-03-01' , '女');
insert into Student values('07' , '郑竹' , '1989-07-01' , '女');
insert into Student values('08' , '王菊' , '1990-01-20' , '女');
---

create table Student(Sid varchar(10),Sname varchar(10),Sage varchar(10),Ssex nvarchar(10));
insert into Student values('01' , '赵雷' , '1990-01-01' , '男');
insert into Student values('02' , '钱电' , '1990-12-21' , '男');
insert into Student values('03' , '孙风' , '1990-05-20' , '男');
insert into Student values('04' , '李云' , '1990-08-06' , '男');
insert into Student values('05' , '周梅' , '1991-12-01' , '女');
insert into Student values('06' , '吴兰' , '1992-03-01' , '女');
insert into Student values('07' , '郑竹' , '1989-07-01' , '女');
insert into Student values('08' , '王菊' , '1990-01-20' , '女');
## 批量上传文件至知识库中
## 使用方法
1.克隆本项目<br>
2.进入文件夹后，和`main.py`同级创建文件夹`upload`，把批量上传的文件（使用通用模式，支持上传
`doc,docx,html,htm,txt,pdf,png,jpg,jpeg,ppt,pptx,ofd,wps`
格式文件）放入其中。并修改空文本文档`.env.example`为`.env`<br>
3.使用记事本打开`.env`，填写如下内容：<br>
```
id=(你的学号，用于登录）
key=(你的密码，用于登录）
target=(知识库界面，例如：https://coze.nankai.edu.cn/product/llm/personal/personal-411/knowledge/xxx）
```

4.安装playwright：<br>
```bash
pip install playwright==1.50.0
playwright install
```
5.运行<br>
```
python main.py
```

代码修订日期：2025-11-30
## 更新说明：
- 修复了使用飞连的快速登录界面导致的登录失败问题
- 修复了新版本NK-GeniOS上传文件时候的界面UI变化问题
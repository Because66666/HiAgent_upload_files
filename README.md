## 批量上传文件至知识库中
## 使用方法
1.克隆本项目<br>
2.进入文件夹后，和`main.py`同级创建文件夹`upload`，把批量上传的文件（默认是CSV文件，其他请修改代码）放入其中。并创建空文本文档`.env`<br>
3.使用记事本打开`.env`，复制如下内容：<br>
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

from playwright.sync_api import Playwright, sync_playwright
from dotenv import load_dotenv
import os
from tqdm import tqdm
# 加载 .env 文件
load_dotenv()
import re
def load_env():
    return os.getenv('id'),os.getenv('key'),os.getenv('target')
def get_files():
    files = []
    for file in os.listdir('./upload'):
        files.append(os.path.abspath(os.path.join('./upload', file)))
    return files
def run(playwright: Playwright):
    data = []
    id_,key,target = load_env()
    if not id_ or id_=='':
        print('id未定义')
        return
    if not key or key=='':
        print('key未定义')
        return
    if not target:
        print('target未定义')
        return
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://coze.nankai.edu.cn/login")
    page.get_by_text("SSO登录").click()
    page.get_by_role("textbox", name="请输入学号/工号").click()
    page.get_by_role("textbox", name="请输入学号/工号").fill(id_)
    page.get_by_role("textbox", name="请输入密码").click()
    page.get_by_role("textbox", name="请输入密码").fill(key)
    page.locator(".arco-checkbox-mask").first.click()
    page.get_by_role("button", name="登 录").click()
    page.wait_for_timeout(3000)

    page.goto(target)
    # page.pause()

    for file in get_files():
        page.wait_for_timeout(1500)
        page.get_by_role("button", name="导入文件").click()
        page.wait_for_timeout(1000)
        page.get_by_test_id("c-m-form-item-step.ProcessRuleFileType").locator("div").filter(has_text=re.compile(r"^表格$")).first.click()
        page.wait_for_timeout(1000)
        page.get_by_test_id("c-m-modal-ok-btn").click()
        page.wait_for_timeout(1000)
        page.get_by_text("点击或拖拽文件到此处上传支持 csv，xls，xlsx").click()
        page.locator("input[type='file']").set_input_files(file)

        page.wait_for_timeout(3000)
        success = False
        while not success:
            try:
                page.get_by_role('button', name='下一步').click()  # 尝试点击按钮
                success = True  # 如果点击成功，标记为成功
                print('点击成功！')
            except Exception as e:
                page.wait_for_timeout(3000)
        page.get_by_role("button", name="确定").click()


    # ---------------------
    context.close()
    browser.close()
    return data



with sync_playwright() as playwright:
    data = run(playwright)

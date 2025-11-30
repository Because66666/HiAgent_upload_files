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

def click_import_button(page):
    """
    检测“导入文件”按钮是否在可视区域，必要时滚动后点击
    """
    buttons = page.get_by_role("button", name="导入文件")
    btn = buttons.first
    bbox = btn.bounding_box()
    vw = page.evaluate("window.innerWidth")
    vh = page.evaluate("window.innerHeight")
    if not bbox or bbox["x"] < 0 or bbox["y"] < 0 or (bbox["x"] + bbox["width"]) > vw or (bbox["y"] + bbox["height"]) > vh:
        btn.scroll_into_view_if_needed()
        page.wait_for_timeout(200)
    btn.click()
    
def run(playwright: Playwright):
    """
    使用 Playwright 登录目标站点并批量上传文件
    """
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
    page.wait_for_load_state('networkidle')
    # page.pause()
    # 检测是否使用浏览器快捷登录
    if page.get_by_text("浏览器快捷登录").is_visible():
        page.get_by_role("button", name="一键登录").click()
    else:
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
    page.wait_for_load_state('networkidle')
    for file in get_files():
        page.wait_for_timeout(1500)
        click_import_button(page)
        page.wait_for_timeout(1000)
        page.get_by_role("menuitem", name="标准导入 通过原始文件导入知识数据").locator("div").nth(3).click()
        page.wait_for_load_state('networkidle')
        page.get_by_test_id("c-m-modal-ok-btn").click()
        page.wait_for_timeout(1000)
        page.get_by_text("点击或拖拽文件到此处上传").click()
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

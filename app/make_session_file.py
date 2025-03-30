import asyncio
import nodriver as uc
from dotenv import load_dotenv
import os
# 環境変数の読み込み
load_dotenv()

import time

async def wait_for_element(tab, selector, timeout=30, check_interval=0.5):
    """
    ページ上に要素が表示されるまで待機します。
    
    引数:
        tab: ブラウザタブオブジェクト
        selector: 要素のCSSセレクタ
        timeout: 待機する最大時間（秒）
        check_interval: 要素をチェックする間隔（秒）
        
    戻り値:
        見つかった場合は要素オブジェクト、タイムアウトした場合はNone
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        element = await tab.query_selector(selector)
        if element:
            return element
        await asyncio.sleep(check_interval)
    return None

async def wait_for_find(tab, str, timeout=30, check_interval=0.5):
    """
    ページ上に要素が表示されるまで待機します。
    
    引数:
        tab: ブラウザタブオブジェクト
        str: 検出文字列
        timeout: 待機する最大時間（秒）
        check_interval: 要素をチェックする間隔（秒）
        
    戻り値:
        見つかった場合は要素オブジェクト、タイムアウトした場合はNone
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        element = await tab.find(str, best_match=True)
        if element:
            return element
        await asyncio.sleep(check_interval)
    return None
async def main():
    browser = await uc.start()
    page = await browser.get('https://chatgpt.com/')
    login_btn = await wait_for_find(page,'Login')
    await login_btn.click()
    await page.sleep(3)
    mail = await wait_for_element(page,'input[id="email-input"]')
    await mail.send_keys(os.getenv('MAIL'))
    await page.sleep(3)
    send = await wait_for_find(page,'Continue')
    await send.click()
    await page.sleep(3)
    password = await wait_for_element(page,'input[id="password"]')
    await password.send_keys(os.getenv('PASSWORD'))
    await page
    send = await wait_for_find(page,'Continue')
    await send.click()
    await page.sleep(10)
    await wait_for_find(page,'Search')
    await page.sleep(2)
    await browser.cookies.save()
    browser.stop()

    


if __name__ == '__main__':
    # since asyncio.run never worked (for me)
    uc.loop().run_until_complete(main())

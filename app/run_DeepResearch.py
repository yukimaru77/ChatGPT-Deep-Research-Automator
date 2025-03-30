import nodriver as uc
import asyncio
import pyperclip
import subprocess
import yaml
import argparse
import os
from pathlib import Path
from nodriver.cdp.input_ import dispatch_key_event

def sanitize_path(path_str):
    """パス名から使用できない文字を除去する関数
    
    Args:
        path_str: 処理するパス文字列
    
    Returns:
        安全なパス文字列
    """
    # Windowsで使用できない文字を置換
    invalid_chars = r'<>:"/\\|?*'
    for char in invalid_chars:
        path_str = path_str.replace(char, '_')
    
    # 先頭と末尾の空白と「.」を削除
    path_str = path_str.strip().strip('.')
    
    # 空の場合はデフォルト名を使用
    if not path_str:
        path_str = "unnamed_output"
    
    return path_str

def setup_output_directory(config, prompt_path, output_dir):
    """出力ディレクトリを設定する関数
    
    Args:
        config: 設定ディクショナリ
        prompt_path: プロンプトファイルのパス
    
    Returns:
        output_dir: 出力ディレクトリのパス
        html_path: HTML出力ファイルのパス
        md_path: Markdown出力ファイルのパス
    """
    # プロンプトファイル名を取得（拡張子なし）
    prompt_path = Path(prompt_path)
    prompt_filename = sanitize_path(prompt_path.stem)
    
    # 出力ディレクトリを作成
    if output_dir is None:
        output_dir = Path(config['output']['base_dir']) / prompt_filename
    else:
        output_dir = Path(output_dir) / prompt_filename
    
    # ディレクトリ名を安全に
    output_dir = Path(str(output_dir))
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 出力ファイルパスを生成
    html_path = output_dir / sanitize_path(config['output']['html_file'])
    md_path = output_dir / sanitize_path(config['output']['markdown_file'])
    
    return output_dir, html_path, md_path

async def send_text_with_newlines(tab, textarea, text, is_shift=True):
    """
    既存のsend_keysメソッドを使いながら、改行文字を適切に処理する関数
    Shift+Enterを使用して改行を実現
    
    Args:
        textarea: テキストエリア要素
        text: 送信するテキスト
    """
    # テキストを改行で分割
    lines = text.split('\n')
    
    # 各行を送信し、改行はShift+Enterキーとして送信
    for i, line in enumerate(lines):
        if line:  # 空の行でなければ通常通りsend_keys
            await textarea.send_keys(line)
        
        # 最後の行でなければShift+Enterキーを送信
        if i < len(lines) - 1:
            if is_shift:
                # Shift+Enterキーのシミュレーション
                # Shiftキーを押す (modifiers=8 は Shift)
                await tab.send(
                    dispatch_key_event(
                        type_='keyDown',
                        modifiers=8,  # Shift key
                        windows_virtual_key_code=16, # VK_SHIFT
                        key="Shift",
                        code="ShiftLeft" # 一般的な左Shiftキーのコード
                    )
                )
                # Enterキーを押す (Shiftが押された状態で)
                await tab.send(
                    dispatch_key_event(
                        type_='keyDown',
                        modifiers=8,  # Shift key is still pressed
                        windows_virtual_key_code=13, # VK_RETURN (Enter)
                        key="Enter",
                        code="Enter",
                        # text='\r' # text属性が必要な場合がある (テキストエリアなど)
                                # '\r' (CR) または '\n' (LF) を試す
                    )
                )

                # Enterキーを離す
                await tab.send(
                    dispatch_key_event(
                        type_='keyUp',
                        modifiers=8,  # Shift key is still pressed
                        windows_virtual_key_code=13,
                        key="Enter",
                        code="Enter"
                    )
                )

                # Shiftキーを離す
                await tab.send(
                    dispatch_key_event(
                        type_='keyUp',
                        modifiers=0,  # No modifiers pressed anymore
                        windows_virtual_key_code=16,
                        key="Shift",
                        code="ShiftLeft"
                    )
                )
            else:
                # Enterキーを押す (Shiftが押された状態で)
                await tab.send(
                    dispatch_key_event(
                        type_='keyDown',
                        modifiers=8,  # Shift key is still pressed
                        windows_virtual_key_code=13, # VK_RETURN (Enter)
                        key="Enter",
                        code="Enter",
                        # text='\r' # text属性が必要な場合がある (テキストエリアなど)
                                # '\r' (CR) または '\n' (LF) を試す
                    )
                )

                # Enterキーを離す
                await tab.send(
                    dispatch_key_event(
                        type_='keyUp',
                        modifiers=8,  # Shift key is still pressed
                        windows_virtual_key_code=13,
                        key="Enter",
                        code="Enter"
                    )
                )

async def main(config_path="config.yaml", prompt_path=None, output_dir=None):
    # 設定ファイルを読み込む
    config_path = Path(config_path)
    with config_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    # プロンプトファイルのパスを決定
    if prompt_path is None:
        prompt_path = Path(config['prompt']['default_path'])
    else:
        prompt_path = Path(prompt_path)
    
    # プロンプトファイルが存在するか確認
    if not prompt_path.exists():
        print(f"⚠️ プロンプトファイル '{prompt_path}' が見つかりません")
        return
    
    # 出力ディレクトリを設定
    output_dir, html_path, md_path = setup_output_directory(config, prompt_path, output_dir)
    print(f"📂 出力ディレクトリ: {output_dir}")
    
    # プロンプトファイルを読み込む
    with prompt_path.open("r", encoding=config['prompt']['encoding']) as f:
        prompt_text = f.read()
    
    # ブラウザを起動
    browser = await uc.start(headless=config['browser']['headless'])
    await browser.cookies.load()
    
    # ChatGPTのWebページを開く
    tab = await browser.get(config['urls']['chatgpt'])
    await tab.sleep(config['timings']['initial_wait'])
    
    # 入力フィールドを見つける
    element = await tab.select(config['selectors']['text_input_placeholder'])
    elem = await tab.select(config['selectors']['text_input_placeholder'])
    await elem.update()

    # 親コンテナを見つける
    while elem.parent:
        elem = elem.parent
        if elem == None:
            break
        await elem.update()
        if config['selectors']['parent_container'] in elem.attributes:
            break
            
    if elem:
        await elem.update()
        container = elem
        await container.update()
        html = await container.get_html()

    # テキストエリアを探してプロンプトを送信
    textarea = await container.query_selector('textarea')
    #await textarea.send_keys(prompt_text)
    await send_text_with_newlines(tab, textarea, prompt_text)

    # Deep Researchボタンをクリック
    deep_research_button = await tab.find(config['buttons']['deep_research'], best_match=True)
    await deep_research_button.click()
    await tab.sleep(config['timings']['initial_wait'])

    # 送信ボタンをクリック
    send_button = await container.query_selector(config['selectors']['send_button'])
    await send_button.click()
    await tab.sleep(config['timings']['initial_wait'])
    
    # レスポンスが完了するまで待機
    await wait_for_response(tab, config, True,False)
    
    # フォローアップのプロンプトを送信
    elem = await tab.select(config['selectors']['followup_placeholder'])
    if elem == None: #再リロードが走ると消えるため
        deep_research_button = await tab.find(config['buttons']['deep_research'], best_match=True)
        await deep_research_button.click()
        elem = await tab.select(config['selectors']['followup_placeholder'])
    await elem.update()

    # 親コンテナを見つける
    while elem.parent:
        elem = elem.parent
        if elem == None:
            break
        await elem.update()
        if config['selectors']['parent_container'] in elem.attributes:
            break

    if elem:
        await elem.update()
        container = elem
        await container.update()
        html = await container.get_html()
        
    # テキストエリアを探してフォローアップを送信
    textarea = await container.query_selector('textarea')
    #await textarea.send_keys(config['prompt']['revise'])
    if config['prompt']['revise'] != "":
        revise_prompt = config['prompt']['revise']
    else:    
        revise_prompt = "いい感じにお願いします。"
    await send_text_with_newlines(tab, textarea, revise_prompt)

    # 送信ボタンをクリック
    send_button = await container.query_selector(config['selectors']['send_button'])
    await send_button.click()
    await tab.sleep(config['timings']['initial_wait'])
    
    # レスポンスが完了するまで待機
    await wait_for_response(tab, config,False,True)
    
    # 結果を取得
    i = 0
    max_retry = 5
    while i < max_retry:
        i += 1
        is_result = await get_and_save_response(tab, config, html_path, md_path)
        if is_result:
            break
        await tab.reload()
        await tab.sleep(15)
        print("再トライします。現在 : ",i+1,"回目")

    # クッキーを保存して終了
    await browser.cookies.save()
    browser.stop()  

async def wait_for_response(tab, config, revise=False, is_reep_research = False):
    """レスポンスが完了するまで待機する関数"""
    if revise:
        max_wait = int(config['timings']['max_wait_time_revise'] / config['timings']['button_check_interval'])
    else:
        max_wait = int(config['timings']['max_wait_time'] / config['timings']['button_check_interval'])
    if is_reep_research:
        await tab.sleep(600)
    elapsed = 0
    await tab.sleep(10)
    
    while elapsed < max_wait:
        try:
            await tab
            speech_button = await tab.query_selector(config['selectors']['speech_button'])
            send_button = await tab.query_selector(config['selectors']['send_button'])
            if speech_button != None or send_button != None:
                break
        except Exception as e:
            print("⚠️ エラー発生:", e)
            break

        await tab.sleep(config['timings']['button_check_interval'])
        elapsed += 1
    else:
        #再リロードします
        await tab.reload()
        await tab.sleep(10)
        elapsed = 0
        while elapsed < max_wait:
            try:
                await tab
                speech_button = await tab.query_selector(config['selectors']['speech_button'])
                send_button = await tab.query_selector(config['selectors']['send_button'])
                if speech_button != None or send_button != None:
                    break
            except Exception as e:
                print("⚠️ エラー発生:", e)
                break

            await tab.sleep(config['timings']['button_check_interval'])
            elapsed += 1
        else:
            print("⌛ タイムアウト：レスポンスが完了しませんでした")
    if elapsed == 0:
        print("待ち時間はありませんでした。")
        await tab.sleep(config['timings']['initial_wait'])
        return False
    await tab.sleep(config['timings']['initial_wait'])
    return True

    

async def get_and_save_response(tab, config, html_path, md_path):
    """レスポンスを取得して保存する関数
    
    Args:
        tab: ブラウザタブ
        config: 設定ディクショナリ
        html_path: HTML出力ファイルのパス
        md_path: Markdown出力ファイルのパス
    """
    #URLを保存
    html_path = Path(html_path)
    current_url = await tab.evaluate('window.location.href')
    current_url = current_url[0].value
    url_txt_path = html_path.parent / Path("url.txt")
    print(current_url)
    with url_txt_path.open("w", encoding="utf-8") as f:
        f.write(current_url)

    # 記事を取得
    articles = await tab.select_all(config['selectors']['main_article'])
    last_article = articles[-1]

    # 最後のdivを取得
    current = last_article
    for _ in range(5):
        await current.update()
        divs = [child for child in current.children if child.tag_name == "div"]
        if not divs:
            break
        current = divs[0]

    # 最も深い階層のdivを取得
    deep_divs = [child for child in current.children if child.tag_name == "div"]
    if deep_divs:
        last_div = deep_divs[-1]
        #await last_div.highlight_overlay()
        
        # ホバー状態にする
        html_before = await tab.get_content()
        await last_div.focus()
        await tab.sleep(config['timings']['short_wait'])
        html_after = await tab.get_content()
        await tab.sleep(config['timings']['button_check_interval'])
        
        # HTMLとして保存
        
        with html_path.open("w", encoding="utf-8") as f:
            f.write(await last_div.get_html())
        print(f"💾 HTML出力を保存: {html_path}")
    else:
        print("❌ レスポンスが見つかりませんでした")
    
    # スクロールして最後の記事を表示
    await tab.sleep(config['timings']['short_wait'])
    await tab
    articles = await tab.select_all(config['selectors']['main_article'])
    first_article = articles[0]
    await first_article.scroll_into_view()
    await tab.sleep(config['timings']['initial_wait'])
    await last_article.scroll_into_view()
    await tab.sleep(config['timings']['initial_wait'])

    
    # コピーボタンを見つけてクリック
    last_article = articles[-1]
    await last_article.send_keys(" ")
    await last_article.mouse_move()
    await last_article.focus()
    await tab.sleep(config['timings']['short_wait'])
    copy_buttons = await tab.select_all(config['selectors']['copy_button'])
    
    if copy_buttons:
        await copy_buttons[-1].mouse_click()
        await tab.sleep(config['timings']['button_check_interval'])
        await copy_buttons[-1].focus()
        await tab.sleep(config['timings']['short_wait'])
        await copy_buttons[-1].mouse_click()
        await tab.sleep(config['timings']['short_wait'])
        
        # クリップボードから保存
        custom_command = config['clipboard']['command'].replace('output.md', str(md_path))
        subprocess.run(custom_command, shell=True)
        print(f"💾 Markdown出力を保存: {md_path}")
    else:
        print("❌ コピーボタンが見つかりませんでした")
        await tab.sleep(config['timings']['short_wait'])
        return False
    
    await tab.sleep(config['timings']['short_wait'])
    return True

def parse_arguments():
    """コマンドライン引数を解析する関数"""
    parser = argparse.ArgumentParser(description='ChatGPT自動化スクリプト')
    parser.add_argument('--config', type=str, default='config.yaml',
                        help='設定ファイルのパス (デフォルト: config.yaml)')
    parser.add_argument('--prompt_path', type=str, default=None,
                        help='プロンプトファイルのパス (デフォルト: 設定ファイルに記載のパス)')
    parser.add_argument('--output_dir', type=str, default=None,
                        help='プロンプトファイルのパス (デフォルト: 設定ファイルに記載のパス)')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    uc.loop().run_until_complete(main(config_path=args.config, prompt_path=args.prompt_path, output_dir=args.output_dir))

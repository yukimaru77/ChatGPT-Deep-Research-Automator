#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import subprocess
from pathlib import Path
import argparse
import concurrent.futures
import threading

def show_usage():
    """使用方法を表示する"""
    print(f"使い方: {sys.argv[0]} /path/to/prompt/directory [出力ディレクトリのベースパス]")
    print(f"  例: {sys.argv[0]} /app/SSLピンニング /app/response")
    print("  指定したディレクトリ内のすべての.txtファイルに対してDeepResearchを実行します")
    sys.exit(1)

def process_prompt_file(prompt_file, output_dir):
    """1つのプロンプトファイルを処理する関数"""
    print(f"処理開始: {prompt_file.name}")
    
    # DeepResearchスクリプトを実行
    cmd = [
        'python', 
        'run_DeepResearch.py', 
        '--prompt_path', str(prompt_file), 
        '--output_dir', str(output_dir)
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"処理完了: {prompt_file.name}")
        print("----------------------------------------")
        return True
    except subprocess.CalledProcessError as e:
        print(f"エラー: {prompt_file.name} の処理中にエラーが発生しました")
        print(f"詳細: {e}")
        print("----------------------------------------")
        return False

def main():
    # 引数解析
    parser = argparse.ArgumentParser(description='指定ディレクトリ内の全txtファイルに対してDeepResearchを実行')
    parser.add_argument('--prompt_dir', help='プロンプトファイルが格納されたディレクトリ', default=None)
    parser.add_argument('--output_base_dir', nargs='?', default='/app/response', 
                        help='出力ディレクトリのベースパス (デフォルト: /app/response)')
    parser.add_argument('--interval', type=int, default=10,
                        help='新しいジョブを開始する間隔（秒）(デフォルト: 10)')
    parser.add_argument('--max-workers', type=int, default=5,
                        help='同時に実行する最大プロセス数 (デフォルト: 5)')
    args = parser.parse_args()

    prompt_dir = Path(args.prompt_dir)
    output_base_dir = Path(args.output_base_dir)
    interval = args.interval
    max_workers = args.max_workers
    
    # ディレクトリが存在するか確認
    if not prompt_dir.is_dir():
        print(f"エラー: ディレクトリ '{prompt_dir}' が見つかりません")
        sys.exit(1)
    
    # ディレクトリ名（最後の部分）を取得
    parent_dir = prompt_dir.name
    output_dir = output_base_dir / parent_dir
    
    # 出力ディレクトリを作成
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # プロンプトディレクトリ内のすべての.txtファイルを処理
    print(f"処理を開始: {prompt_dir} 内のtxtファイル")
    print(f"出力先: {output_dir}")
    print(f"並列実行数: 最大{max_workers}プロセス、{interval}秒間隔で起動")
    print("----------------------------------------")
    
    # txtファイルを検索
    txt_files = list(prompt_dir.glob('*.txt'))
    
    if not txt_files:
        print("警告: .txtファイルが見つかりません")
        sys.exit(0)
    
    # 結果を保存するリスト
    results = []
    success_count = 0
    
    # ThreadPoolExecutorを使用して並列実行
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        
        # ファイルごとに処理を提出し、間隔を空けて実行
        for i, prompt_file in enumerate(txt_files):
            # 新しいタスクを提出
            future = executor.submit(process_prompt_file, prompt_file, output_dir)
            futures.append(future)
            
            # インターバルを空ける（最後のファイル以外）
            if i < len(txt_files) - 1:
                time.sleep(interval)
        
        # すべてのタスクの完了を待つ
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                success_count += 1
    
    # 結果の表示
    if success_count == 0:
        print("警告: 処理に成功したtxtファイルがありませんでした")
    else:
        print(f"すべての処理が完了しました。合計 {len(txt_files)} 個中 {success_count} 個のファイルの処理に成功しました。")
        print(f"結果は {output_dir} に保存されています")

if __name__ == "__main__":
    main()
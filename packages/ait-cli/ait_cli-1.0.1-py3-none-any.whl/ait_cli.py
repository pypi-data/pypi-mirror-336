import subprocess
import sys
import argparse
import os
import platform
from typing import List

# ait-templateのURL
AIT_TEMPLATE_URL = 'https://github.com/aistairc/ait-template.git'

def run_command(command: list[str], error_message: str) -> None:
    """
    指定されたコマンドを実行し、失敗した場合はエラーメッセージとともに終了する。
    
    Parameters:
        command (list): 実行するコマンドのリスト。バッシュ/シェル名とその引数を含む。
        error_message (str): コマンドが失敗した場合に表示するエラーメッセージ。
    """
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {error_message}")
        print(f"Details: Command execution failed with error code: {e.returncode}")
        print(f"Command: {' '.join(command)}")
        sys.exit(1)

def script_run(file_name: str, script_args: List[str] = []) -> None:
    """
    OSに応じて適切なスクリプトを実行する。
    
    Parameters:
        file_name (str): 実行するスクリプトの基本ファイル名（拡張子は自動で追加される）。
        script_args (List[str], optional): バッチ/シェルスクリプトに渡す追加の引数。デフォルトは空リスト。
    """
    current_os = platform.system().lower()
    # windowsとそれ以外で拡張子を変更する
    script_name = file_name + '.bat' if current_os == 'windows' else './' + file_name + '.sh'
    # fileの存在チェック
    if not os.path.isfile(script_name):
        print(f"Error: Script '{script_name}' not found. Please verify the path.")
        sys.exit(1)

    # シェルスクリプトに実行権限を付与 
    if current_os != 'windows':
        os.chmod(script_name, 0o744)

    run_command([script_name, *script_args], f"Failed to execute script '{file_name}'.")

def change_directory(path: str) -> None:

    """
    スクリプトの場所にディレクトリを移動する。

    Parameters:
        path (str): 実行するAITのルートディレクトリ。
    """
    script_directory = os.path.join(path, 'tool')
    # ディレクトリの存在チェック
    if not os.path.exists(script_directory):
        print(f"Error: Directory '{script_directory}' not found. Please verify the path.")
        sys.exit(1)
    os.chdir(script_directory)

def create_template(args: argparse.Namespace) -> None:
    """
    ait_template Gitリポジトリをクローンしてセットアップする。
    
    Parameters:
        args (argparse.Namespace): コマンドライン引数を保持するNamespaceオブジェクト。
            - args.ait_name (str): クローンするリポジトリの名前。
    """
    # 指定されたパスまで移動
    os.chdir(args.path)
    run_command(['git', 'clone', AIT_TEMPLATE_URL, args.ait_name], "Failed to clone the repository. Please check your network connection or the repository URL.")

    # ait名のディレクトリに移動

    os.chdir(args.ait_name)
    # オリジナルのait-templateリポジトリとのリモート接続を切る
    run_command(['git', 'remote', 'remove', 'origin'], f"Failed to remove the 'origin' remote for repository '{args.ait_name}'.")

def launch_devenv(args: argparse.Namespace) -> None:
    """
    'launch_devenv'スクリプトを実行する。
    """
    change_directory(args.path)
    script_run('launch_devenv')

def generate_thirdparty_notices(args: argparse.Namespace) -> None:
    """
    'generate_thirdparty_notices'スクリプトを実行する。
    """
    change_directory(args.path)
    script_run('generate_thirdparty_notices')

def compress_ait_package(args: argparse.Namespace) -> None:
    """
    'compress_ait_package'スクリプトを実行する。
    """
    change_directory(args.path)
    script_run('compress_ait_package')

def github_push(args: argparse.Namespace) -> None:
    """
    'github_push'スクリプトを実行する。
    
    Parameters:
        args (argparse.Namespace): コマンドライン引数を保持するNamespaceオブジェクト。
            - args.github_repository (str, optional): GitHubのリポジトリURL。
                引数が渡されない場合、リポジトリURLは省略される。
    """
    change_directory(args.path)
    if args.github_repository:
        script_run('github_push', [args.github_repository])
    else:
        script_run('github_push')

def parse_arguments() -> argparse.ArgumentParser:
    """
    コマンドライン引数を解析する。
    
    Returns:
        argparse.ArgumentParser: 引数解析用のArgumentParserオブジェクト。
    """
    parser = argparse.ArgumentParser(prog='ait-cli', description="Command Line Tools for AIT")
    subparsers = parser.add_subparsers(dest='command')

    # 'create'サブコマンド
    create_parser = subparsers.add_parser("create", help="Create AIT Template")
    create_parser.add_argument("--ait_name", type=str, help="Your AIT name", required=True)
    create_parser.add_argument("--path", type=str, help="Your AIT directory path", default="./", required=False)

    # 'jupyter'サブコマンド
    jupyter_parser = subparsers.add_parser("jupyter", help="Launch the AIT Template in the Jupyter Notebook")
    jupyter_parser.add_argument("--path", type=str, help="Your AIT directory path", default="./", required=False)

    # 'thirdparty-notice'サブコマンド
    thirdparty_notice_parser = subparsers.add_parser("thirdparty-notice", help="Generate third-party notices")
    thirdparty_notice_parser.add_argument("--path", type=str, help="Your AIT directory path", default="./", required=False)

    # 'zip'サブコマンド
    zip_parser = subparsers.add_parser("zip", help="Zip the AIT package")
    zip_parser.add_argument("--path", type=str, help="Your AIT directory path", default="./", required=False)

    # 'git-push'サブコマンド
    git_push_parser = subparsers.add_parser("git-push", help="Push the AIT to GitHub")
    git_push_parser.add_argument("--github_repository", type=str, help="Your GitHub Repository URL. Be sure to specify this only for the first push.", required=False)
    git_push_parser.add_argument("--path", type=str, help="Your AIT directory path", default="./", required=False)

    return parser

def main() -> None:
    """
    メインプロセス。
    
    コマンドライン引数を解析して、指定されたコマンドを実行する。
    """
    args = parse_arguments().parse_args()

    if args.command == "create":
        create_template(args)
    elif args.command == "jupyter":
        launch_devenv(args)
    elif args.command == "thirdparty-notice":
        generate_thirdparty_notices(args)
    elif args.command == "zip":
        compress_ait_package(args)
    elif args.command == "git-push":
        github_push(args)
    else:
        print("=============================================")
        print("Error: Invalid command specified.")
        print("Available commands are as follows:")
        print("=============================================")
        parse_arguments().print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()

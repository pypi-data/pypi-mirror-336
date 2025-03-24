import sys
from rich.markdown import Markdown
from rich.console import Console
from rich.live import Live
from ta import TAClient

console = Console()


def cli():
    if len(sys.argv) < 2:
        console.print('使用方法: ta "你的问题"')
        return

    # 将所有参数组合成一个问题，保留空格
    question = " ".join(sys.argv[1:])
    try:
        client = TAClient()
        md = Markdown("对方正在输入...")
        with Live(md) as live:
            client.chat(question, live)
    except Exception as e:
        console.print(f"Error: {e}")


if __name__ == "__main__":
    cli()

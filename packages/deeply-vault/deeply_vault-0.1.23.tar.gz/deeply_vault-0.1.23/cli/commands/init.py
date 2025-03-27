import click
import os
import yaml
from pathlib import Path


@click.command()
@click.option("--vault", "-v", help="볼트 이름")
@click.option("--force", "-f", is_flag=True, help="기존 설정 덮어쓰기")
def init(vault, force):
    """프로젝트 초기화

    현재 디렉토리에 .env.vault.yml 설정 파일을 생성하고 프로젝트를 초기화합니다.
    """
    config_file = Path(".env.vault.yml")

    if config_file.exists() and not force:
        click.echo("이미 초기화된 프로젝트입니다. 덮어쓰려면 --force 옵션을 사용하세요.")
        return

    if not vault:
        vault = click.prompt(
            "볼트 이름을 입력하세요", default=os.path.basename(os.getcwd()))

    config = {
        "vault": vault,
        "server": "https://your-server-url",
    }

    with open(config_file, "w") as f:
        yaml.dump(config, f, sort_keys=False, indent=2, allow_unicode=True)

    click.echo(f"프로젝트가 초기화되었습니다. 볼트: {vault}")
    click.echo("다음 명령어로 로그인하세요: uv run deeply-vault login")

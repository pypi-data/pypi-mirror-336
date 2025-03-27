import click
import requests

from cli.utils.config import get_config, save_config
from cli.utils.token import save_token


@click.command()
@click.option("--server", "-s", help="서버 URL")
def login(server):
    """서버에 로그인

    API 인증 토큰을 발급받고 저장합니다.
    """
    try:
        # 설정 파일 읽기
        config = get_config()

        if server:
            config["server"] = server

        server_url = config.get("server")

        if not server_url:
            click.echo(
                "서버 URL이 설정되지 않았습니다. 명령어 예시: deeply login -s http://localhost:13500")
            return

        # 사용자 인증
        username = click.prompt("사용자명")
        password = click.prompt("비밀번호", hide_input=True)

        # 토큰 발급 요청
        response = requests.post(
            f"{server_url}/api/v1/auth/token",
            data={"username": username, "password": password}
        )

        if response.status_code != 200:
            click.echo(
                f"로그인 실패: {response.json().get('detail', '알 수 없는 오류')}", err=True)
            return

        # 토큰 저장
        token_data = response.json()
        token = token_data.get("access_token")
        save_token(token)

        # 설정 파일 업데이트 (토큰 제외)
        save_config(config)

        click.echo("Vault 로그인 성공! API 토큰이 ~/.deeply/vault/token.json에 저장되었습니다.")

    except Exception as e:
        click.echo(f"오류가 발생했습니다: {str(e)}", err=True)

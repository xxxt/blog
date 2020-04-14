from fabric import task
from invoke import Responder
from _credentials import github_username, github_password


def _get_github_auth_responders():
    """
    返回 GitHub 用户名密码自动填充器
    """
    username_responder = Responder(
        pattern="Username for 'https://github.com':",
        response='{}\n'.format(github_username)
    )
    password_responder = Responder(
        pattern="Password for 'https://{}@github.com':".format(github_username),
        response='{}\n'.format(github_password)
    )
    return [username_responder, password_responder]


@task()
def deploy(c):
    code_path = '/mnt/blog/blog'

    project_root_path = '/mnt/blog'

    # 进入项目根目录，从 Git 拉取最新代码
    with c.cd(code_path):
        cmd = 'git pull'
        responders = _get_github_auth_responders()
        c.run(cmd, watchers=responders)

    # 重新启动应用
    with c.cd(project_root_path):
        cmd = 'docker-compose down && docker-compose up -d'
        c.run(cmd)

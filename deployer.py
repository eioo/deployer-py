from webhook import Webhook
import git_utils
import process_utils
import time


class Deployer(object):
    def __init__(self, args):
        self.npm_client = args.npm_client
        self.remote_branch = args.remote_branch
        self.local_branch = args.local_branch
        self.script = args.script
        self.webhook_path = args.webhook_path

        self.deploy_in_progress = False
        self.git_repo_name = git_utils.get_git_repo_name(self.remote_branch)
        self.webhook = self.create_webhook()

    def create_webhook(self):
        path = self.webhook_path

        if '<reponame>' in path:
            path = path.replace('<reponame>', self.git_repo_name)

        webhook = Webhook(self.deploy, path=path, port=5234)
        webhook.listen()

        return webhook

    def deploy(self):
        if self.deploy_in_progress:
            while True:
                time.sleep(0.1)

        print('Deploy started')

        self.close_existing()
        self.fetch()
        self.install()
        self.start()

        print(f'Deploy done. Type \'pm2 logs {self.git_repo_name}\' to view logs.')

    def close_existing(self):
        process_utils.execute(f'pm2 delete {self.git_repo_name}')

    def fetch(self):
        print('Fetching from git')
        git_utils.fetch_and_reset(self.remote_branch, self.local_branch)

    def install(self):
        print(f'Installing with "{self.npm_client}"')
        process_utils.execute_and_print(f'{self.npm_client} install')

    def start(self):
        print(f'Running script "{self.script}" with "{self.npm_client}"')
        process_utils.execute(f'pm2 start {self.npm_client} --name {self.git_repo_name} -- start --color')

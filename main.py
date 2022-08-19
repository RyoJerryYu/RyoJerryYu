import datetime
import os
from jinja2 import PackageLoader, Environment
import urllib.parse
import github


def render(**kwargs):
  env = Environment(loader=PackageLoader('templates', '.'))
  template = env.get_template('README.md.j2')
  output = template.render(**kwargs)
  print(output)

  with open('README.md', 'w', encoding='utf-8') as f:
    f.write(output)
    f.close()


def badge_struct(name, logo):
  name = urllib.parse.quote(name)
  return {'name': name, 'logo': logo}


def github_info(token: str):
  a_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
  now = datetime.datetime.now()

  g = github.Github(token)
  most_star_repo = {
      'repo_name': '',
      'repo_url': '',
      'stars': 0,
  }
  most_forked_repo = {
      'repo_name': '',
      'repo_url': '',
      'forks': 0,
  }

  most_recent_committed_repo = {
      'repo_name': 'none',
      'repo_url': '',
      'datestr': '',
      'timestr': '',
  }

  recent_commit_cnt = 0
  recent_repo_cnt = 0

  # most starred and forked repo
  for repo in g.get_user().get_repos():
    if repo.private:
      continue

    if repo.stargazers_count > most_star_repo['stars']:
      most_star_repo['repo_name'] = repo.name
      most_star_repo['repo_url'] = repo.html_url
      most_star_repo['stars'] = repo.stargazers_count

    if repo.forks_count > most_forked_repo['forks']:
      most_forked_repo['repo_name'] = repo.name
      most_forked_repo['repo_url'] = repo.html_url
      most_forked_repo['forks'] = repo.forks_count

  # recent commits and repo count
  for repo in g.get_user().get_repos(sort='pushed', direction='desc'):
    if repo.pushed_at > a_week_ago:
      repo_recent_commit_cnt = repo.get_commits(
          since=a_week_ago, until=now, author=g.get_user()).totalCount
      if repo_recent_commit_cnt > 0:
        recent_repo_cnt += 1
        recent_commit_cnt += repo_recent_commit_cnt
    else:
      break

  # most recent committed repo
  for repo in g.get_user().get_repos(sort='pushed', direction='desc'):
    if repo.private:
      continue
    recent_committed_date = repo.get_branch(
        repo.default_branch).commit.commit.author.date

    most_recent_committed_repo['repo_name'] = repo.name
    most_recent_committed_repo['repo_url'] = repo.html_url
    most_recent_committed_repo['datestr'] = recent_committed_date.strftime(
        r'%m/%d')
    most_recent_committed_repo['timestr'] = recent_committed_date.strftime(
        r'%H:%M:%S')
    break

  return {
      'most_starred_repo': most_star_repo,
      'most_forked_repo': most_forked_repo,
      'most_recent_committed_repo': most_recent_committed_repo,
      'recent_commit_cnt': recent_commit_cnt,
      'recent_repo_cnt': recent_repo_cnt,
  }


if __name__ == '__main__':
  github_info_res = github_info(os.getenv('GH_TOKEN'))
  data = {
      'colors': {
          'background_color': '18244a',
          'logo_color': '4bbed5',
      },
      'languages': [
          badge_struct('Go', 'go'),
          badge_struct('Python', 'python'),
          badge_struct('Rust', 'rust'),
          badge_struct('TypeScript', 'TypeScript'),
          badge_struct('JavaScript', 'JavaScript'),
          badge_struct('Kotlin', 'Kotlin'),
          badge_struct('Java', 'Java'),
          badge_struct('C++', 'cplusplus'),
      ],
      'cloud_native': [
          badge_struct('Docker', 'Docker'),
          badge_struct('Kubernetes', 'Kubernetes'),
          badge_struct('Helm', 'helm'),
          badge_struct('Istio', 'istio'),
          badge_struct('OpenTelemetry', 'OpenTelemetry'),
          badge_struct('Prometheus', 'Prometheus'),
          badge_struct('Fluent Bit', 'fluentbit'),
          badge_struct('Pulumi', 'Pulumi'),
          badge_struct('Ansible', 'Ansible'),
      ],
      'skills': [
          badge_struct('Jenkins', 'Jenkins'),
          badge_struct('Grafana', 'grafana'),
          badge_struct('MySQL', 'MySQL'),
          badge_struct('PostgreSQL', 'postgresql'),
          badge_struct('Redis', 'Redis'),
          badge_struct('ClickHouse', 'clickhouse'),
          badge_struct('Apache Kafka', 'apachekafka'),
          badge_struct('React', 'React'),
          badge_struct('Vue.js', 'vue.js'),
      ],
      'github': github_info_res,
  }
  render(**data)

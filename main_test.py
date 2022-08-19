from main import github_info
import os


def test_github_info():
  res = github_info(os.getenv('GH_TOKEN'))
  with open('testres.txt', 'w', encoding='utf-8') as f:
    f.write(str(res))
    f.close()

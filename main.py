from jinja2 import PackageLoader, Environment
import urllib.parse


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


if __name__ == '__main__':

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
      ''
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
      ]
  }
  render(**data)

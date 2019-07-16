#! *-* utf-8 *-*
from app import create_app, init_logger
from flask import render_template
import requests
import markdown
import oss2

'''
从oss 取得md文档，转换为html，嵌入jinja 模版中
'''

SCHEMA = 'https'
endpoint = 'oss-cn-hangzhou.aliyuncs.com'
default_bucket_name = 'oops-markdown'

AccessKeyID = r'LTAIpJzEDMukYR9L'
AccessKeySecret = r'm8WNLAlu5yc7PFdYBVJarGsqBGjEOW'


def get_bucket_url(object_key, bucket_name=default_bucket_name):
    return f'{SCHEMA}://{bucket_name}.{endpoint}/{object_key}'


def get_bucket_object_map(bucket_name=default_bucket_name):
    bucket = oss2.Bucket(
        oss2.Auth(AccessKeyID, AccessKeySecret), endpoint, bucket_name)    
    return {o.key: get_bucket_url(o.key) for o in bucket.list_objects().object_list}


bucket_object_map=get_bucket_object_map()


def get_md_url(md_name):
    return bucket_object_map.get(md_name)


def get_text(url, encoding = 'utf-8'):
    r=requests.get(url)
    if r.ok is True:
        r.encoding=encoding
        return r.text
    return None


def markdown2html(md_content):
    config={
        'codehilite': {
            'use_pygments': False,
            'css_class': 'prettyprint code',
        }
    }

    return markdown.markdown(md_content, extensions=["codehilite"], extension_configs=config)


app = create_app(__name__)
init_logger(app)


@app.route('/')
def index():
    return render_template('base.html', md_list=bucket_object_map.keys())


@app.route('/md/<md_name>')
def md(md_name):
    url = get_md_url(md_name)
    return render_template('md.html', content=markdown2html(get_text(url)))


if __name__ == '__main__':
    app.run(debug=True)

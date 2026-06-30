#!/usr/bin/env python3
"""帮帮文档相关域名与接口常量。"""

DOCS_DOMAIN = 'docs.yukework.com'
DOCS_BASE_URL = f'https://{DOCS_DOMAIN}'
DOCS_EXPORT_URL = f'{DOCS_BASE_URL}/document-application/api/v2/file/export'
DOCS_REFERER = f'{DOCS_BASE_URL}/'

IPS_DOMAIN = 'ips.yukework.com'
IPS_BASE_URL = f'https://{IPS_DOMAIN}'

LOGIN_PAGE_PATTERNS = [
    f'{IPS_DOMAIN}/static/cas-fe/',
    IPS_DOMAIN,
    'login.zuoyebang.cc',
    '/cas/login',
    f'service=https%3A%2F%2F{DOCS_DOMAIN}',
    'document-application/api/ips/login/callback',
]

DOCS_SUCCESS_INDICATORS = [
    (f'{DOCS_DOMAIN}/doc?fileId=', '已登录并进入文档页面'),
    (f'{DOCS_DOMAIN}/doc/', '已登录并进入文档页面'),
    (f'{DOCS_DOMAIN}/edit', '已登录并进入编辑页面'),
    (f'{DOCS_DOMAIN}/d/', '已登录并进入文档查看页面'),
    (f'{DOCS_DOMAIN}/spaces', '已登录，进入空间列表'),
    (f'{DOCS_DOMAIN}/home', '已登录，进入首页'),
]


def get_export_progress_url(task_id: str) -> str:
    return f'{DOCS_BASE_URL}/document-application/api/v2/file/export/progress?taskId={task_id}'


def is_docs_cookie_domain(domain: str) -> bool:
    return domain.lstrip('.') == DOCS_DOMAIN

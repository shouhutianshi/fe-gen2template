import json
import sys
import html
import re
from collections import Counter


def strip_html(text):
    text = html.unescape(text)
    text = re.sub(r'<[^>]+>', '', text)
    return re.sub(r'\s+', ' ', text).strip()


data = json.load(sys.stdin)
bugs = data.get('data', [])
total = data.get('totalItem', len(bugs))

print(f'共 {total} 个 Bug\n')
print('=' * 120)

for b in bugs:
    bugid = b.get('bugid', b.get('id', ''))
    plevel = b.get('pLevel', '')
    status = b.get('status', b.get('statusName', ''))
    assignee = b.get('assignee', {}).get('displayName', '')
    summary = b.get('summary', '')
    
    # 附件信息 - 展示URL
    attachments = b.get('attachment', [])
    attach_urls = []
    if isinstance(attachments, list) and len(attachments) > 0:
        for att in attachments:
            url = att.get('content', '') if isinstance(att, dict) else str(att)
            if url:
                attach_urls.append(url)
    
    # 描述信息（去除HTML，但不截取）
    desc = strip_html(b.get('description', ''))
    
    print(f"Bug ID: {bugid}")
    print(f"标题: {summary}")
    print(f"严重程度: {plevel} | 状态: {status} | 经办人: {assignee}")
    if attach_urls:
        print(f"附件: {', '.join(attach_urls)}")
    else:
        print("附件: -")
    print(f"描述: {desc}")
    print('-' * 120)

print()
levels = Counter(b.get('pLevel', '') for b in bugs)
statuses = Counter(b.get('status', b.get('statusName', '')) for b in bugs)
print('按严重程度：', ' | '.join(f'{k}: {v}' for k, v in sorted(levels.items())))
print('按状态：    ', ' | '.join(f'{k}: {v}' for k, v in sorted(statuses.items())))

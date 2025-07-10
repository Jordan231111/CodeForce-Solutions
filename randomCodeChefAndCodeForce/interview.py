import urllib.request, re, html
url='https://docs.google.com/document/d/e/2PACX-1vTER-wL5E8YC9pxDx43gk8eIds59GtUUk4nJo_ZWagbnrH0NFvMXIw6VWFLpf5tWTZIT9P9oLIoFJ6A/pub'
html_data=urllib.request.urlopen(url).read().decode('utf-8')
# Extract td contents
rows=[]
pattern=re.compile(r'<tr[^>]*?>(.*?)</tr>',re.DOTALL)
for tr in pattern.findall(html_data):
    tds=re.findall(r'<td[^>]*?>(.*?)</td>',tr,re.DOTALL)
    if len(tds)==3:
        vals=[]
        for td in tds:
            # extract text
            text=html.unescape(re.sub(r'<[^>]+>','',td))
            text=text.strip()
            vals.append(text)
        x, ch, y=vals
        if x.isdigit() and y.isdigit():
            rows.append((int(x),int(y),ch))
print('rows',len(rows))
maxx=max(r[0] for r in rows)
maxy=max(r[1] for r in rows)
width=maxx+1
height=maxy+1
grid=[[' ']*width for _ in range(height)]
for x,y,ch in rows:
    grid[y][x]=ch
for row in grid:
    print(''.join(row))
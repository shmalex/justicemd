import path
import io
import os
import errno
import requests as r
import builtins
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

def get_doc(i):
    tries = 0
    while True:
        try:
            resp = r.get("http://lex.justice.md/viewdoc.php?action=view&view=doc&id="+str(i)+"&lang=2")
            return text_from_html(resp.text)
        except:
            tries += 1
            if tries > 3:
                return ''

str(1).zfill(10)

def get_name(i):
    return 'doc/'+str(i//10000).zfill(3)+'/'+str(i//100).zfill(5)+'/'+str(i).zfill(3)+".txt"

def make_dir(file):
    if not os.path.exists(os.path.dirname(file)):
        try:
            os.makedirs(os.path.dirname(file))
        except OSError as e:
            print(e)
            if e.errno != errno.EEXIST:
                raise

def save_doc(i, text):
    with open(get_name(i), 'w') as f:
        f.write(text)

def create_index():
    for i in range(40000, 1000000):
        file = get_name(i)
        if (os.path.exists(file)):
            continue
        make_dir(file)
        yield i

for iDoc in create_index():
    print(iDoc)
    save_doc(iDoc, "")
    save_doc(iDoc, get_doc(iDoc))
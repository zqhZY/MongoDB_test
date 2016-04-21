# -*- coding: utf-8 -*-
import urllib
import pymongo
import re
import os

def connectMongo():
    conn = pymongo.MongoClient("localhost" , 27017)#连接mogodb
    db = conn.post_db#连接数据库，没有则创建
    return db
    
def getHtml(url):
  blog = urllib.urlopen(url)
  html = blog.read()
  return html

def getPost(html):
  
  pattern = r'< h2 class="blog-post-title" >< a href="(.+)">(.+)</a></h2>'
  postre = re.compile(pattern)
  postlist = re.findall(postre, html)

  rootpath = r'https://justzqh.sinaapp.com'

  post_tosave = []#待存储的信息集合

  for posturl in postlist:

      postinfo = {}#待存数据

      postpath = rootpath + posturl[0]
      postname = posturl[1]
      #post_html = getHtml(postpath)#获取博客文章html，用于测试部分更新

      postinfo['name'] = postname
      postinfo['url'] = postpath
      #postinfo['context'] = post_html#博客文章html信息，用于测试部分更新

      post_tosave.append(postinfo)

  return post_tosave
  
 
  
if __name__ == '__main__':

  db = connectMongo()
  post_collection = db.post_collection#操作数据库集合，不存在则创建
  
  html = getHtml("https://justzqh.sinaapp.com/")
  post_tosaves = getPost(html)


  for post in post_tosaves:
      post_collection.insert(post)#插入数据
      #post_collection.update({"name":post['name']},{'$set':{"context":post['context']}})#部分更新数据库字段测试
      #post_collection.ensure_index([("context" , "text")])#为博客文本创建全文索引

  #findlist = list(post_collection.find({'$text':{'$search':"mongo"}}))#根据全文索引查找数据，返回所有满足条件的数据集合
  #print findlist

  print "save ok."
  
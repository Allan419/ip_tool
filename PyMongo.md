[PyMongo Docs](https://pymongo.readthedocs.io/en/stable/)


在抓取数据时遇到`tbody`要到network中确认源码中是否包含`tbody`标签，有些网站可能是`runtime`生成的

遇到`table`时，如果有多行数据需要提取，但是`tr[1]`代表标题需要排除，可以用下面👇的语法从第二个`tr`标签开始提取
> ./tr[positions()>1] 

`66ip`网页使用js+cookie反爬，重写父类的`get_page_from_url`方法 (https://www.bilibili.com/video/BV1y4411w7DX?p=13) 16集

`import js2py`

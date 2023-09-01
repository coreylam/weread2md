# weread2md
 
 - [weread2md](https://github.com/coreylam/weread2md)
获取微信读书的笔记与标注，并整理成markdown格式

## 背景

要做什么？
---
将微信读书中的读书笔记，标注内容，整理成 markdown 格式，可以同步到其他笔记软件，博客或者是 github 上面，方便做知识的梳理和汇总

有没有现成的？
---

- [weread2notion](https://github.com/DuckDuck88/weread2notion)

> 这个项目将微信读书笔记、划线等信息同步到notion数据库， 不过由于我自己不使用 notion 管理笔记，所以不是很适用，不过本项目中的获取读书笔记信息的脚本是从该项目中获取的。不想重复造轮子了，如果想自己造轮子，也可以参考: [微信读书部分网页接口](https://www.mdzz2048.com/2023/cae32cf67def/) 自己实现

- [Higurashi-kagome/wereader](https://github.com/Higurashi-kagome/wereader)

> 微信读书浏览器插件，使用起来也很便捷，可以比较灵活的导出对应的笔记或者标注，不过不支持全部导出，要一本一本自己导出，而且不同内容也需要自己一个个复制，更适合当天阅读完成后，导出并整理到笔记中（个人认为，如果这样的话，阅读这件事情就变的“重”了，阅读的心理负担会加大）。而我更希望是阅读完一本书之后，直接将整本书的内容按格式导出并同步到笔记上，方便后续回看。这个工具其实已经很好用了，微信读书本身也具备类似的功能，可以直接导出笔记信息，只不过在使用场景上跟我期望的不同

## 使用方法

1. 在 `md_tmpl.py` 文件中，可以自定义展示的模版，目前支持的关键字都在里面，如果需要扩展信息，需修改脚本

2. 设置环境变量
    - `WR_BOOK_NAME`: 导出的书名称（为空时导出全部）
    - `WR_VID`, `WR_SKEY`: 从网页登录微信读书，获取 `cookies` 中的 `wr_vid` 和 `wr_skey`, 其中 wr_vid 是用户固定的，获取一次就可以，每次只需获取 `wr_skey`
  
3. 运行 `run.py`， 导出的文件在 `books` 目录下

注意：如果要导出的书籍中不存在任何标注或者笔记，则不会被导出

## 效果

通过 CICD 平台，创建一个流水线，只需要触发流水线，就可以生成对应的摘要文件。

![](https://picgo-1256712489.cos.ap-chongqing.myqcloud.com/img/202308301559328.png)

![](https://picgo-1256712489.cos.ap-chongqing.myqcloud.com/img/202308301556801.png)

![](https://picgo-1256712489.cos.ap-chongqing.myqcloud.com/img/202308301559110.png)

*说明： 将生成的文件放到制品库不是最佳的选择，这里只是一个案例，主要是展示可以通过这种方式，将生成的文件放到任何一个地方（例如发布博客，或者提交github，或者发到指定的数据库等等）*

## 结合 pywebio

pywebio 可以简易的生成网站，结合 pywebio，可以编写拉取指定页面的工具，以及展示所有笔记的工具, 参考另一篇[文章](https://www.cnblogs.com/coreylin/p/17668505.html)效果如下：

![](https://picgo-1256712489.cos.ap-chongqing.myqcloud.com/img/202309010907922.png)

![](https://picgo-1256712489.cos.ap-chongqing.myqcloud.com/img/202309010909825.png)

![](https://picgo-1256712489.cos.ap-chongqing.myqcloud.com/img/202309010910636.png)

## todo
- 增加时间判断，支持获取某个时间段之后的所有读书笔记
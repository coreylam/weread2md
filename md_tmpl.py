# 书籍信息
bookinfo_md_tmpl = """
# {title}

> 作者： {author}
> 
> 发布时间： {publish_time}
> 
> 分类: {category_title}

![]({cover_image_url})

摘要: {summary}

目录: 
- {chapters}
"""

# 评论信息
review_md_tmpl = """
---
- 【章节】{chapterTitle}
- 【时间】 {createTime}
- 【原文】
  - {abstract}
- 【我的评论】 
  - {markText}
"""

# 划线信息
bookmark_md_tmpl = """
- 【{time}】 {text}
"""
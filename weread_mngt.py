from weread_api import WeRead
import md_tmpl
import datetime


class WeReadManager(object):

    def __init__(self, wr_vid: str, wr_skey: str) -> None:
        cookie = f"wr_vid={wr_vid};wr_skey={wr_skey}"
        self.update_cookies(cookie)

    def update_cookies(self, cookie: str):
        self.api = WeRead(cookie)

    def print_reviews(self, book_id):
        rsp = self.api.get_review_list(book_id)

    def get_bookids(self):
        rsp =  self.api.get_notebooklist()
        return [i['bookId'] for i in rsp]
    
    def get_bookinfo(self, book_id):
        """ 获取指定书籍的信息，包括摘要
        """
        rsp = self.api.get_notebooklist()
        book_info = [i for i in rsp if str(book_id) == i['bookId']][0]
        rsp = self.api.get_bookinfo(book_id)
        book_info['summary'] = rsp[2].strip()
        return book_info

    def get_chapters(self, book_id):
        """ 获取书籍的章节标题
        """
        rsp = self.api.get_chapter_info(book_id)
        self.chapter_map = {}
        for k, v in rsp.items():
            self.chapter_map[k] = v['title']
        return [i['title'] for i in rsp.values()]

    def timestamp_to_datetime(self, timestamp):
        """
        Convert a timestamp to a datetime string in the format 'YYYY-MM-DD HH:MM:SS'.
        
        Parameters:
            timestamp (int): The input timestamp in seconds.
            
        Returns:
            str: The converted datetime string.
        """
        datetime_obj = datetime.datetime.fromtimestamp(timestamp)
        datetime_str = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
        return datetime_str

    def get_bookmark_info(self, book_id):
        rsp = self.api.get_bookmark_list(book_id)
        data = {}
        for item in rsp[::-1]:
            if "chapterUid" not in item:
                continue
            cuid = item['chapterUid']
            if cuid not in data:
                data[cuid] = []
            data[cuid].append({
                "text": item['markText'],
                "time": self.timestamp_to_datetime(item['createTime'])
            })
        return data 

    def export(self, book_id, path="books"):
        book_info = self.get_bookinfo(book_id)
        book_title = book_info['book']['title']
        if not book_title:
            book_title = book_id
        book_info_str = md_tmpl.bookinfo_md_tmpl.format(
            title = book_info['book']['title'],
            author =  book_info['book']['author'],
            publish_time = book_info['book']['publishTime'],
            category_title = book_info['book'].get('categories',[{}])[0].get('title', ""),
            cover_image_url = book_info['book']['cover'],
            summary = book_info['summary'],
            chapters = "\n- ".join(self.get_chapters(book_id))
        )
        output = book_info_str.strip()

        rsp = self.api.get_review_list(book_id)[1]
        if not rsp and not self.get_bookmark_info(book_id):
            # 如果没有划线和评论，就不要导出
            return ""
        output += "\n\n# Comment\n\n"
        reviews = []
        for item in rsp:
            reviews.append(md_tmpl.review_md_tmpl.format(
                chapterTitle = item.get('chapterTitle', "None"),
                createTime = self.timestamp_to_datetime(item['createTime']),
                abstract = item['abstract'],
                markText = item['markText']
            ).strip())
        output += "\n\n".join(reviews)

        output += "\n\n# HighLight"
        rsp = self.get_bookmark_info(book_id)
        for k, v in rsp.items():
            chapter_info = self.chapter_map.get(k, k)
            output += "\n\n## {}".format(chapter_info)
            bookmarks = []
            for item in v:
                bookmarks.append(md_tmpl.bookmark_md_tmpl.format(
                    title = k,
                    time = item['time'],
                    text = item['text']
                ))
            output += "\n".join(bookmarks)
        with open(f"{path}/{book_title}.md", "w") as fid:
            fid.writelines(output)
        return output

    def export_all(self, path="books"):
        """ 导出所有书籍的划线和评论（如果没有划线和评论的书籍不会被导出）
        """
        book_ids = self.get_bookids()
        for book_id in book_ids:
            print(f"export {book_id}")
            self.export(book_id, path)

    def export_by_name(self, name, path="books"):
        """ 导出指定名称的书籍
        """
        book_id = self.get_bookid_by_name(name)
        if not book_id:
            return
        self.export(book_id, path)

    def get_bookid_by_name(self, name):
        """ 根据书籍名称，获取对应的ID
        """
        rsp = self.api.get_notebooklist()
        book_info = [i['bookId'] for i in rsp if str(name) == i['book']['title']]
        if not book_info:
            return None
        return book_info[0]

    def save_json(self, file_path, data, indent):
        import json
        with open(file_path, 'w') as fid:
            unicode_str = json.dumps(data, indent=indent)
            chinese_str = unicode_str.encode('utf-8').decode('unicode_escape')
            # print(chinese_str)
            fid.writelines(chinese_str)

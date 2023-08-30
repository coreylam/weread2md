import os
from weread_mngt import WeReadManager


book_name = os.environ.get("WR_BOOK_NAME", "")
wr_vid = os.environ.get("WR_VID", "")
wr_skey = os.environ.get("WR_SKEY", "")
if not book_name or not wr_vid or not wr_skey:
    raise RuntimeError("请先设置环境变量： WR_BOOK_NAME(导出的书名称), WR_VID, WR_SKEY(从cookies中获取)")
wrm = WeReadManager(wr_vid=wr_vid, wr_skey=wr_skey)
wrm.export_by_name(book_name)

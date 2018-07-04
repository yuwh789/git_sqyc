from django.core.paginator import Paginator

def Rtn_pages(order_list, page_index,):
    # 1进行分页
    paginator = Paginator(order_list, 20)
    # 2获取第n页内容
    order_list = paginator.page(int(page_index))
    # 3获取页码列表
    pages = paginator.page_range
    # 4.1获取总页数
    num_pages = paginator.num_pages
    current_num = int(page_index)

    if num_pages <= 10:
        # 总页数小于等于5
        pages = range(1, num_pages + 1)
    elif current_num <= 5:
        # 当前页为前5页
        pages = range(1, 11)
    elif num_pages - current_num <= 4:
        # 當前頁爲後5頁
        pages = range(num_pages - 10, num_pages + 1)
    else:
        # 既不是前5页，也不是后5页
        pages = range(current_num - 5, current_num + 5)

    return  order_list, pages
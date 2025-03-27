
#為集合的内容去重 無範圍值, 直接在内部去重  需重寫 def __eq__(self, other):
def remove_list_dunplicates(ls: list[any]) -> None:
    unique_list = []
    for item in ls:
        if item not in unique_list:
            unique_list.append(item)
    ls.clear()
    ls += unique_list
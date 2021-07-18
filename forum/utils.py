
def get_children(children_qs):
    res_children = []
    for comment in children_qs:
        com_dict = {
            'author': comment.author,
            'id': comment.id,
            'text': comment.text,
            'created': comment.created.strftime('%Y-%m-%d %H:%M'),
            'updated': comment.updated.strftime('%Y-%m-%d %H:%M'),
            'is_child': comment.is_child,
            'parent_id': comment.parent_id
        }
        next_children_qs = comment.comment_children.all()
        if next_children_qs:
            com_dict['children'] = get_children(next_children_qs)
        res_children.append(com_dict)
    return res_children




def create_comment_tree(qs):    #qs-queryset
    res = []
    for comment in qs:
        com_dict = {
            'author': comment.author,
            'id': comment.id,
            'text': comment.text,
            'created': comment.created.strftime('%Y-%m-%d %H:%M'),
            'updated': comment.updated.strftime('%Y-%m-%d %H:%M'),
            'is_child': comment.is_child,
            'parent_id': comment.parent_id
        }
        children_qs = comment.comment_children.all()
        if children_qs:
            com_dict['children'] = get_children(children_qs)
        if not comment.is_child:
            res.append(com_dict)
    return res

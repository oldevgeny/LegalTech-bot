from tree.models import Comment

comments = Comment.objects.all()

def categories():
    categories = ""
    # t = 1

    for i in range(len(comments)):
        comment = comments[i]
        # print(f"comments:\n{comments}\ncomment:\n{comment}\ncomment_text:\n{comment.text}\ncomment_parent:\n{comment.parent}\ncomment_is_child:\n{comment.is_child}\ncomment_object_id:\n{comment.object_id}")
        if comment.is_child == False:
            categories += str(comment) + ") " + comment.text + "\n"
            # t += 1
    # for i in range(len(categories)):
    #     print(categories[i], sep=', ', end=' ')
    return categories

def children(parent_id):
    children = ""
    children_id = []
    # t = 1

    for i in range(len(comments)):
        comment = comments[i]
        # print(comment.parent, parent_id, sep='\n')
        if comment.is_child == True and str(comment.parent) == str(parent_id):
            children += str(comment) + ") " + comment.text + "\n"
            children_id.append(comment.object_id)
            # t += 1
    return children

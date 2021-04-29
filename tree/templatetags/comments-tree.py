from django.template import Library
from django.utils.html import mark_safe


register = Library()


@register.filter
def comments_filter(comments_list):
    res = """
             <ul style="list-style-type:none;">
                <div class="col-md-12 mt-2">
                    {}
                </div>
             </ul>
          """
    i = ''

    for comment in comments_list:
        i += """
             <li>
                <div class="col-md-12 mb-2 mt-2 p-0">
                    <hr>

                    <p>{text} | id={id}</p>
                    <a href="javascript:void(0)" class="replyQ" question-id="{id}" question-parent={parent_id}>Add question</a>
                    <a href="javascript:void(0)" class="replyA" answer-id="{id}" answer-parent={parent_id}>Add answer</a>

                    <form action="" method="POST" class="question-form form-group" id="question-form-{id}" style="display:none;">
                        <textarea type="text" class="form-control" name="question-text"></textarea><br>
                        <input type="submit" class="btn btn-primary submit-reply-question" question-id="{id}" question-submit-reply="{parent_id}" value="Add question"></input>
                    </form>

                    <form action="" method="POST" class="answer-form form-group" id="answer-form-{id}" style="display:none;">
                        <textarea type="text" class="form-control" name="answer-text"></textarea><br>
                        <input type="submit" class="btn btn-primary submit-reply-answer" answer-id="{id}" answer-submit-reply="{parent_id}" value="Add answer"></input>
                    </form>

                </div>
             </li>
             """.format(id=comment['id'], timestamp=comment['timestamp'], text=comment['text'], parent_id=comment['parent_id'])
        if comment.get('children'):
            i += comments_filter(comment['children'])
    return mark_safe(res.format(i))

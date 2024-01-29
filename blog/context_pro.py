from blog.models import Category, Tag, InstagramPost, Ad, Post


def get_all(request):
    if request.path == "/" or "category" in request.path or "tag" in request.path or "filter" in request.path or "post" in request.path:
        context = {
            'categories':Category.objects.all(),
            'tags':Tag.objects.all(),
            "instagram_post":InstagramPost.objects.last(),
            "ad_object":Ad.objects.last(),
        }
        print(context["ad_object"].link)

        return context
    else:
        return {}

# def set_all_rect_count(request):
#     data = Post.objects.all()
#     for obj in data:
#         obj.reaction_count = obj.get_all_reaction_count
#         obj.save()
#         print("done")

# set_all_rect_count()
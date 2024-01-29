from blog.models import Post



def set_reaction(request,post,react):
    request.session.modified = True
    try:
        reacted_posts = request.session["react_list"]
    except:
        reacted_posts = request.session["react_list"] = []
   
    if post.id in reacted_posts:
        return "Siz bu maqolaga reaksiya bildirgansiz ! "
    else:
        if react == "good":
            post.good += 1
            post.reaction_count += 1 
            post.save()
        elif react == "like":
            post.like += 1
            post.reaction_count += 1 
            post.save()
        elif react == "great":
            post.great += 1
            post.reaction_count += 1 
            post.save()
        elif react == "fire":
            post.fire += 1
            post.reaction_count += 1 
            post.save()
        elif react == "legend":
            post.legend += 1
            post.reaction_count += 1 
            post.save()
        elif react == "neutral":
            post.neutral += 1
            post.reaction_count += 1 
            post.save()
        elif react == "dislike":
            post.dislike += 1
            post.reaction_count += 1 
            post.save()
        reacted_posts.append(post.id)
        return "Reaksiya qabul qilindi !"
            


def filter_by_reactions(data):
    pass

def comments_counter(request,post_id):
    post = Post.objects.get(pk=post_id)
    return post.comments.all().count()



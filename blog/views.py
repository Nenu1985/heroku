from attr.filters import exclude
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, CreateView
from .forms import EmailPostFrom, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector
from .forms import EmailPostFrom, CommentForm, SearchForm
from django.utils.text import slugify


# Create your views here.


# view list of post with paginator
# http://127.0.0.1:8000/blog/
def post_list(request, tag_slug=None):
    # using custom manager published
    object_list = Post.published.all()  # millions posts
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)  # 3 posts in a page
    page = request.GET.get('page')  # str object
    try:
        posts = paginator.page(page)  # Page object
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html',
                  {
                      'posts': posts,  # {Page} = <Page 1 of 3>
                      'page': page,  # {str} = '2'
                      'tag': tag,
                  })


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:  # GET
        comment_form = CommentForm()

    # Retrieving posts by similarity p. 152
    # List of similar posts
    # FLAT: The values_list() QuerySet returns tuples with the
    # values for the given fields. We pass flat=True to it to get a flat
    # list like [1, 2, 3, ...]
    post_tags_ids = post.tags.values_list('id', flat=True)

    similar_posts = Post.published.filter(tags__in=post_tags_ids) \
        .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
                        .order_by('-same_tags', '-publish')[:4]

    return render(
        request,
        'blog/post/detail.html',
        {'post': post,
         'comments': comments,
         'new_comment': new_comment,
         'comment_form': comment_form,
         'similar_posts': similar_posts,
         },
    )


# http://127.0.0.1:8000/blog/
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3

    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    # Retrieve post by id:
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostFrom(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email. Get url of post (post_detail view)
            post_url = request.build_absolute_uri(post.get_absolute_url())

            subject = f'{cd["name"]} ({cd["email"]})' \
                f'recommends your reading {post.title}'
            message = f'Read "{post.title}" at {post_url} \n\n{cd["name"]}' \
                f' \'s comments: {cd["comments"]}'

            # subject = '{} ({}) recommends you reading " ' \
            #           '{}"'.format(cd['name'], cd['email'], post.title)
            # message = 'Read "{}" at {}\n\n{}\'s comments:' \
            #           '{}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostFrom()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent},
                  )

# Searching. Don't work with DB that not Postgres!!!
def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.annotate(
                search=SearchVector('title', 'body'),).filter(search=query)
    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})


class PostCreateView(CreateView):
    model = Post
    fields = ['tags', 'title', 'body']
    # exclude('slug', 'author',)
    template_name = 'blog/post/create.html'

    def form_valid(self, form):
        author = self.request.user

        slug = slugify(form.cleaned_data['title'])
        # form.cleaned_data['slug'] = slug
        # author.blog_posts.add(form.instance)

        # form.cleaned_data['status'] = 'published'
        post = form.save(commit=False)
        post.author = author
        post.slug = slug
        post.status = 'published'
        post.save()
        return redirect(post.get_absolute_url())
        # form.save()

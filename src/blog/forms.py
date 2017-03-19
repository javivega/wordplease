from django import forms

from blog.models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["title", "post_intro", "post_body", "post_img", "post_category", "post_published"]

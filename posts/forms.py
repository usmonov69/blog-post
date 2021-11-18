from django import forms
from .models import Comment, Post


class CommentForm(forms.ModelForm):
	content  = forms.CharField(label='' ,widget=forms.Textarea(attrs={
		'class' : 'form-control',
		'placeholder':'Type your comment',
		'id': 'usercommet',
		'rows': '4'
		}))
	class Meta:
		model = Comment
		fields = ('content',)


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'overview', 'author', 'thumbnail', 
			'categories', 'featured', 'previous_post', 'next_post')
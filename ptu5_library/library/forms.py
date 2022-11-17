from django import forms
from django.utils.timezone import datetime, timedelta
from . models import BookReview

class BookReviewForm(forms.ModelForm):
    def is_valid(self) -> bool:
        valid = super().is_valid()
        if valid:
            reader = self.cleaned_data.get("reader")
            recent_posts = BookReview.objects.filter(
                reader=reader, 
                created_at__gte=(datetime.now()-timedelta(hours=1))
            )
            if recent_posts:
                return False
        return valid

    class Meta:
        model = BookReview
        fields = ('content', 'book', 'reader', )
        widgets = {
            'book': forms.HiddenInput(),
            'reader': forms.HiddenInput(),
        }
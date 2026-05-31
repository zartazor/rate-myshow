from django import forms

from .models import Rating


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["score", "review_text", "spoiler"]
        widgets = {
            "score": forms.NumberInput(attrs={"min": 1, "max": 10, "step": 0.5}),
        }

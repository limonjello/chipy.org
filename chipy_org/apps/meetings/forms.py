from django.forms import ModelForm
from meetings.models import Topic, Presentor, RSVP

class TopicForm(ModelForm):
    required = ('title',
                'meeting',
                'description',
    )

    def __init__(self, request, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        self.fields['meeting'].required = True
        self.fields['description'].required = True

        self.request = request
    
    class Meta:
        model = Topic
        fields = ('title',
                   'meeting',
                   'length',
                   'description',
                   'slides_link',
               )

    def save(self, commit=True):
        instance = super(TopicForm, self).save(commit)
        if self.request and not instance.presentor:
            instance.presentor, created = Presentor.objects.get_or_create(
                user = self.request.user,
                name = self.request.user.get_full_name(),
                email = self.request.user.email,
                release = True,
            )

        if commit:
            instance.save()
        return instance

class RSVPForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(RSVPForm, self).__init__(*args, **kwargs)
        self.request = request

    class Meta:
        model = RSVP
        fields = ('response','user','name','meeting','email')

    def clean_user(self):
        if not self.cleaned_data['user'] and self.request.user.is_authenticated():
            return self.request.user
        

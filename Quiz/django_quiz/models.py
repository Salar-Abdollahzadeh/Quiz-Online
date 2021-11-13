from django.db import models

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Question(BaseModel):
    difficulty_choices = [('H', 'hard'),
                          ('M', 'medium'),
                          ('E', 'easy')]

    title = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=1, choices=difficulty_choices)

    cat = models.ForeignKey(to='Category', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.cat} - {self.title[:20]}  - {self.difficulty}'

    correct_answer_count = models.PositiveSmallIntegerField(default=0)
    wrong_answer_count = models.PositiveSmallIntegerField(default=0)
    not_answered_count = models.PositiveSmallIntegerField(default=0)

    @property
    def correct_answer_count_property(self):
        return Answer.objects.filter(question=self, choice__is_correct=True).count()

    @property
    def wrong_answer_count_property(self):
        return Answer.objects.filter(question=self, choice__is_correct=False).count()

    @property
    def not_answered_count_property(self):
        return Answer.objects.filter(question=self, choice=None).count()


class Choice(BaseModel):
    question = models.ForeignKey(to='Question', on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    number = models.PositiveSmallIntegerField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Answer(BaseModel):
    question = models.ForeignKey(to='Question', on_delete=models.CASCADE)
    choice = models.ForeignKey(to='Choice', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.question.id} - {self.choice}'

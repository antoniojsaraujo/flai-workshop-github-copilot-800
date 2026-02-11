from django.db import models
from django.contrib.auth.models import User
from bson import ObjectId


class UserProfile(models.Model):
    """Extended user profile for OctoFit Tracker"""
    _id = models.CharField(max_length=24, primary_key=True, default=lambda: str(ObjectId()))
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField(null=True, blank=True)
    fitness_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        default='beginner'
    )
    total_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        ordering = ['-total_points']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Team(models.Model):
    """Team model for group competitions"""
    _id = models.CharField(max_length=24, primary_key=True, default=lambda: str(ObjectId()))
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(UserProfile, related_name='teams')
    captain = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        related_name='captained_teams'
    )
    total_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teams'
        ordering = ['-total_points']

    def __str__(self):
        return self.name


class Activity(models.Model):
    """Activity logging model for tracking workouts"""
    _id = models.CharField(max_length=24, primary_key=True, default=lambda: str(ObjectId()))
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(
        max_length=50,
        choices=[
            ('running', 'Running'),
            ('walking', 'Walking'),
            ('cycling', 'Cycling'),
            ('swimming', 'Swimming'),
            ('strength_training', 'Strength Training'),
            ('yoga', 'Yoga'),
            ('sports', 'Sports'),
            ('other', 'Other'),
        ]
    )
    duration = models.IntegerField(help_text='Duration in minutes')
    distance = models.FloatField(null=True, blank=True, help_text='Distance in kilometers')
    calories = models.IntegerField(null=True, blank=True)
    points = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    activity_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'activities'
        ordering = ['-activity_date']
        verbose_name_plural = 'Activities'

    def __str__(self):
        return f"{self.user} - {self.activity_type} - {self.activity_date}"

    def save(self, *args, **kwargs):
        """Calculate points based on activity type and duration"""
        if not self.points:
            # Simple point calculation: 10 points per 10 minutes
            self.points = (self.duration // 10) * 10
            
            # Bonus points for certain activity types
            if self.activity_type == 'running':
                self.points = int(self.points * 1.5)
            elif self.activity_type == 'strength_training':
                self.points = int(self.points * 1.3)
        
        super().save(*args, **kwargs)
        
        # Update user's total points
        self.user.total_points = sum(
            activity.points for activity in self.user.activities.all()
        )
        self.user.save()


class Leaderboard(models.Model):
    """Leaderboard model for tracking rankings"""
    _id = models.CharField(max_length=24, primary_key=True, default=lambda: str(ObjectId()))
    period = models.CharField(
        max_length=20,
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('all_time', 'All Time'),
        ]
    )
    leaderboard_type = models.CharField(
        max_length=20,
        choices=[
            ('individual', 'Individual'),
            ('team', 'Team'),
        ]
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    rankings = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leaderboard'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.period} {self.leaderboard_type} - {self.start_date}"


class Workout(models.Model):
    """Personalized workout suggestions"""
    _id = models.CharField(max_length=24, primary_key=True, default=lambda: str(ObjectId()))
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ]
    )
    activity_type = models.CharField(
        max_length=50,
        choices=[
            ('running', 'Running'),
            ('walking', 'Walking'),
            ('cycling', 'Cycling'),
            ('swimming', 'Swimming'),
            ('strength_training', 'Strength Training'),
            ('yoga', 'Yoga'),
            ('sports', 'Sports'),
            ('mixed', 'Mixed'),
        ]
    )
    duration = models.IntegerField(help_text='Estimated duration in minutes')
    exercises = models.JSONField(default=list, help_text='List of exercises in the workout')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'workouts'
        ordering = ['difficulty_level', 'title']

    def __str__(self):
        return f"{self.title} ({self.difficulty_level})"

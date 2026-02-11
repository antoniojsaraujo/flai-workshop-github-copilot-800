from django.contrib import admin
from .models import UserProfile, Team, Activity, Leaderboard, Workout


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for UserProfile model"""
    list_display = ['_id', 'first_name', 'last_name', 'email', 'fitness_level', 'total_points', 'created_at']
    list_filter = ['fitness_level', 'created_at']
    search_fields = ['first_name', 'last_name', 'email']
    readonly_fields = ['_id', 'total_points', 'created_at', 'updated_at']
    ordering = ['-total_points']
    
    fieldsets = (
        ('User Information', {
            'fields': ('_id', 'user', 'first_name', 'last_name', 'email')
        }),
        ('Profile Details', {
            'fields': ('age', 'fitness_level', 'total_points')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin interface for Team model"""
    list_display = ['_id', 'name', 'captain', 'member_count', 'total_points', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['_id', 'total_points', 'created_at', 'updated_at']
    filter_horizontal = ['members']
    ordering = ['-total_points']
    
    fieldsets = (
        ('Team Information', {
            'fields': ('_id', 'name', 'description', 'captain')
        }),
        ('Members', {
            'fields': ('members',)
        }),
        ('Statistics', {
            'fields': ('total_points',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def member_count(self, obj):
        """Display the number of team members"""
        return obj.members.count()
    member_count.short_description = 'Members'


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin interface for Activity model"""
    list_display = ['_id', 'user', 'activity_type', 'duration', 'distance', 'points', 'activity_date']
    list_filter = ['activity_type', 'activity_date', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'activity_type', 'notes']
    readonly_fields = ['_id', 'points', 'created_at']
    date_hierarchy = 'activity_date'
    ordering = ['-activity_date']
    
    fieldsets = (
        ('Activity Information', {
            'fields': ('_id', 'user', 'activity_type', 'activity_date')
        }),
        ('Activity Details', {
            'fields': ('duration', 'distance', 'calories', 'points', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """Admin interface for Leaderboard model"""
    list_display = ['_id', 'period', 'leaderboard_type', 'start_date', 'end_date', 'created_at']
    list_filter = ['period', 'leaderboard_type', 'start_date']
    search_fields = ['period', 'leaderboard_type']
    readonly_fields = ['_id', 'created_at', 'updated_at']
    date_hierarchy = 'start_date'
    ordering = ['-start_date']
    
    fieldsets = (
        ('Leaderboard Information', {
            'fields': ('_id', 'period', 'leaderboard_type')
        }),
        ('Date Range', {
            'fields': ('start_date', 'end_date')
        }),
        ('Rankings', {
            'fields': ('rankings',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    """Admin interface for Workout model"""
    list_display = ['_id', 'title', 'difficulty_level', 'activity_type', 'duration', 'created_at']
    list_filter = ['difficulty_level', 'activity_type', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['_id', 'created_at', 'updated_at']
    ordering = ['difficulty_level', 'title']
    
    fieldsets = (
        ('Workout Information', {
            'fields': ('_id', 'title', 'description')
        }),
        ('Workout Details', {
            'fields': ('difficulty_level', 'activity_type', 'duration', 'exercises')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

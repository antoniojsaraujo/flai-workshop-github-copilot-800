from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from .models import UserProfile, Team, Activity, Leaderboard, Workout
from .serializers import (
    UserProfileSerializer,
    TeamSerializer,
    ActivitySerializer,
    LeaderboardSerializer,
    WorkoutSerializer
)


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for UserProfile model"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    @action(detail=True, methods=['get'])
    def activities(self, request, pk=None):
        """Get all activities for a specific user"""
        user = self.get_object()
        activities = Activity.objects.filter(user=user)
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def teams(self, request, pk=None):
        """Get all teams for a specific user"""
        user = self.get_object()
        teams = user.teams.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get statistics for a specific user"""
        user = self.get_object()
        activities = Activity.objects.filter(user=user)
        
        stats = {
            'total_activities': activities.count(),
            'total_points': user.total_points,
            'total_duration': activities.aggregate(Sum('duration'))['duration__sum'] or 0,
            'total_distance': activities.aggregate(Sum('distance'))['distance__sum'] or 0,
            'total_calories': activities.aggregate(Sum('calories'))['calories__sum'] or 0,
            'activities_by_type': {}
        }
        
        # Count activities by type
        activity_types = activities.values('activity_type').annotate(count=Count('_id'))
        for item in activity_types:
            stats['activities_by_type'][item['activity_type']] = item['count']
        
        return Response(stats)


class TeamViewSet(viewsets.ModelViewSet):
    """ViewSet for Team model"""
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        """Add a member to a team"""
        team = self.get_object()
        user_id = request.data.get('user_id')
        
        try:
            user = UserProfile.objects.get(_id=user_id)
            team.members.add(user)
            
            # Update team points
            self._update_team_points(team)
            
            return Response({
                'message': f'{user} added to {team.name}',
                'member_count': team.members.count()
            })
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def remove_member(self, request, pk=None):
        """Remove a member from a team"""
        team = self.get_object()
        user_id = request.data.get('user_id')
        
        try:
            user = UserProfile.objects.get(_id=user_id)
            team.members.remove(user)
            
            # Update team points
            self._update_team_points(team)
            
            return Response({
                'message': f'{user} removed from {team.name}',
                'member_count': team.members.count()
            })
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get statistics for a specific team"""
        team = self.get_object()
        members = team.members.all()
        
        # Get all activities from team members
        activities = Activity.objects.filter(user__in=members)
        
        stats = {
            'member_count': members.count(),
            'total_points': team.total_points,
            'total_activities': activities.count(),
            'total_duration': activities.aggregate(Sum('duration'))['duration__sum'] or 0,
            'total_distance': activities.aggregate(Sum('distance'))['distance__sum'] or 0,
            'average_points_per_member': team.total_points / members.count() if members.count() > 0 else 0,
        }
        
        return Response(stats)

    def _update_team_points(self, team):
        """Helper method to update team's total points"""
        team.total_points = sum(member.total_points for member in team.members.all())
        team.save()


class ActivityViewSet(viewsets.ModelViewSet):
    """ViewSet for Activity model"""
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def get_queryset(self):
        """Filter activities by query parameters"""
        queryset = Activity.objects.all()
        
        # Filter by user
        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            queryset = queryset.filter(user___id=user_id)
        
        # Filter by activity type
        activity_type = self.request.query_params.get('activity_type', None)
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date:
            queryset = queryset.filter(activity_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(activity_date__lte=end_date)
        
        return queryset

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent activities (last 7 days)"""
        seven_days_ago = datetime.now() - timedelta(days=7)
        activities = Activity.objects.filter(activity_date__gte=seven_days_ago)
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)


class LeaderboardViewSet(viewsets.ModelViewSet):
    """ViewSet for Leaderboard model"""
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer

    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current leaderboard rankings"""
        period = request.query_params.get('period', 'all_time')
        leaderboard_type = request.query_params.get('type', 'individual')
        
        if leaderboard_type == 'individual':
            users = UserProfile.objects.all().order_by('-total_points')[:10]
            rankings = [
                {
                    'rank': idx + 1,
                    'id': str(user._id),
                    'name': f"{user.first_name} {user.last_name}",
                    'points': user.total_points,
                }
                for idx, user in enumerate(users)
            ]
        else:  # team leaderboard
            teams = Team.objects.all().order_by('-total_points')[:10]
            rankings = [
                {
                    'rank': idx + 1,
                    'id': str(team._id),
                    'name': team.name,
                    'points': team.total_points,
                    'member_count': team.members.count(),
                }
                for idx, team in enumerate(teams)
            ]
        
        return Response({
            'period': period,
            'type': leaderboard_type,
            'rankings': rankings,
            'updated_at': datetime.now().isoformat()
        })


class WorkoutViewSet(viewsets.ModelViewSet):
    """ViewSet for Workout model"""
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer

    def get_queryset(self):
        """Filter workouts by query parameters"""
        queryset = Workout.objects.all()
        
        # Filter by difficulty level
        difficulty = self.request.query_params.get('difficulty', None)
        if difficulty:
            queryset = queryset.filter(difficulty_level=difficulty)
        
        # Filter by activity type
        activity_type = self.request.query_params.get('activity_type', None)
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
        
        return queryset

    @action(detail=False, methods=['get'])
    def recommendations(self, request):
        """Get workout recommendations based on user's fitness level"""
        user_id = request.query_params.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = UserProfile.objects.get(_id=user_id)
            workouts = Workout.objects.filter(difficulty_level=user.fitness_level)
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

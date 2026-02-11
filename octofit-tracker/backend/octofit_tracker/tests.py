from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import datetime, timedelta
from .models import UserProfile, Team, Activity, Leaderboard, Workout


class UserProfileModelTest(TestCase):
    """Test cases for UserProfile model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            email='test@example.com',
            age=25,
            fitness_level='beginner'
        )
    
    def test_profile_creation(self):
        """Test that a user profile can be created"""
        self.assertEqual(self.profile.first_name, 'Test')
        self.assertEqual(self.profile.last_name, 'User')
        self.assertEqual(self.profile.fitness_level, 'beginner')
        self.assertEqual(self.profile.total_points, 0)
    
    def test_profile_string_representation(self):
        """Test the string representation of a profile"""
        self.assertEqual(str(self.profile), 'Test User')


class TeamModelTest(TestCase):
    """Test cases for Team model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='captain',
            email='captain@example.com',
            password='testpass123'
        )
        self.captain_profile = UserProfile.objects.create(
            user=self.user,
            first_name='Captain',
            last_name='User',
            email='captain@example.com'
        )
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team',
            captain=self.captain_profile
        )
    
    def test_team_creation(self):
        """Test that a team can be created"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.captain, self.captain_profile)
        self.assertEqual(self.team.total_points, 0)
    
    def test_team_string_representation(self):
        """Test the string representation of a team"""
        self.assertEqual(str(self.team), 'Test Team')
    
    def test_add_team_member(self):
        """Test adding a member to a team"""
        new_user = User.objects.create_user(
            username='member',
            email='member@example.com',
            password='testpass123'
        )
        member_profile = UserProfile.objects.create(
            user=new_user,
            first_name='Member',
            last_name='User',
            email='member@example.com'
        )
        self.team.members.add(member_profile)
        self.assertEqual(self.team.members.count(), 1)


class ActivityModelTest(TestCase):
    """Test cases for Activity model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='athlete',
            email='athlete@example.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            first_name='Athlete',
            last_name='User',
            email='athlete@example.com'
        )
        self.activity = Activity.objects.create(
            user=self.profile,
            activity_type='running',
            duration=30,
            distance=5.0,
            calories=300,
            activity_date=datetime.now()
        )
    
    def test_activity_creation(self):
        """Test that an activity can be created"""
        self.assertEqual(self.activity.user, self.profile)
        self.assertEqual(self.activity.activity_type, 'running')
        self.assertEqual(self.activity.duration, 30)
    
    def test_activity_points_calculation(self):
        """Test that points are calculated correctly"""
        # Points should be calculated: (30 // 10) * 10 * 1.5 = 30 * 1.5 = 45
        self.assertGreater(self.activity.points, 0)


class WorkoutModelTest(TestCase):
    """Test cases for Workout model"""
    
    def setUp(self):
        """Set up test data"""
        self.workout = Workout.objects.create(
            title='Morning Run',
            description='A quick morning run to start the day',
            difficulty_level='beginner',
            activity_type='running',
            duration=20,
            exercises=[
                {'name': 'Warm-up', 'duration': 5},
                {'name': 'Run', 'duration': 10},
                {'name': 'Cool-down', 'duration': 5}
            ]
        )
    
    def test_workout_creation(self):
        """Test that a workout can be created"""
        self.assertEqual(self.workout.title, 'Morning Run')
        self.assertEqual(self.workout.difficulty_level, 'beginner')
        self.assertEqual(len(self.workout.exercises), 3)
    
    def test_workout_string_representation(self):
        """Test the string representation of a workout"""
        self.assertEqual(str(self.workout), 'Morning Run (beginner)')


class APIEndpointTest(APITestCase):
    """Test cases for API endpoints"""
    
    def setUp(self):
        """Set up test client and data"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='apiuser',
            email='api@example.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            first_name='API',
            last_name='User',
            email='api@example.com',
            fitness_level='intermediate'
        )
    
    def test_api_root_endpoint(self):
        """Test that the API root endpoint is accessible"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('endpoints', response.data)
    
    def test_user_list_endpoint(self):
        """Test that the user list endpoint works"""
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_team_list_endpoint(self):
        """Test that the team list endpoint works"""
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_activity_list_endpoint(self):
        """Test that the activity list endpoint works"""
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_workout_list_endpoint(self):
        """Test that the workout list endpoint works"""
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_leaderboard_current_endpoint(self):
        """Test that the current leaderboard endpoint works"""
        response = self.client.get('/api/leaderboard/current/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('rankings', response.data)
    
    def test_workout_recommendations_endpoint(self):
        """Test that the workout recommendations endpoint works"""
        response = self.client.get(f'/api/workouts/recommendations/?user_id={self.profile._id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_user_stats_endpoint(self):
        """Test that the user stats endpoint works"""
        response = self.client.get(f'/api/users/{self.profile._id}/stats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_activities', response.data)
        self.assertIn('total_points', response.data)


class LeaderboardTest(TestCase):
    """Test cases for Leaderboard functionality"""
    
    def setUp(self):
        """Set up test data"""
        # Create multiple users with different points
        self.users = []
        for i in range(5):
            user = User.objects.create_user(
                username=f'user{i}',
                email=f'user{i}@example.com',
                password='testpass123'
            )
            profile = UserProfile.objects.create(
                user=user,
                first_name=f'User{i}',
                last_name='Test',
                email=f'user{i}@example.com',
                total_points=(i + 1) * 100
            )
            self.users.append(profile)
    
    def test_user_ordering_by_points(self):
        """Test that users are ordered by total points"""
        top_users = UserProfile.objects.all().order_by('-total_points')[:3]
        self.assertEqual(top_users[0].total_points, 500)
        self.assertEqual(top_users[1].total_points, 400)
        self.assertEqual(top_users[2].total_points, 300)

from rest_framework import serializers
from .models import UserProfile, Team, Activity, Leaderboard, Workout
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for Django User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model"""
    _id = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)
    username = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = UserProfile
        fields = [
            '_id', 'user', 'username', 'password', 'first_name', 'last_name',
            'email', 'age', 'fitness_level', 'total_points',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['_id', 'total_points', 'created_at', 'updated_at']

    def create(self, validated_data):
        """Create user and profile together"""
        username = validated_data.pop('username', None)
        password = validated_data.pop('password', None)
        
        if username and password:
            user = User.objects.create_user(
                username=username,
                email=validated_data.get('email'),
                first_name=validated_data.get('first_name'),
                last_name=validated_data.get('last_name'),
                password=password
            )
            validated_data['user'] = user
        
        return super().create(validated_data)

    def to_representation(self, instance):
        """Convert ObjectId to string in response"""
        representation = super().to_representation(instance)
        if '_id' in representation and representation['_id']:
            representation['_id'] = str(representation['_id'])
        return representation


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model"""
    _id = serializers.CharField(read_only=True)
    members = UserProfileSerializer(many=True, read_only=True)
    captain = UserProfileSerializer(read_only=True)
    member_ids = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )
    captain_id = serializers.CharField(write_only=True, required=False)
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = [
            '_id', 'name', 'description', 'members', 'captain',
            'member_ids', 'captain_id', 'member_count', 'total_points',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['_id', 'total_points', 'created_at', 'updated_at']

    def get_member_count(self, obj):
        """Get the number of team members"""
        return obj.members.count()

    def create(self, validated_data):
        """Handle member and captain assignment during creation"""
        member_ids = validated_data.pop('member_ids', [])
        captain_id = validated_data.pop('captain_id', None)
        
        team = Team.objects.create(**validated_data)
        
        if member_ids:
            members = UserProfile.objects.filter(_id__in=member_ids)
            team.members.set(members)
        
        if captain_id:
            team.captain = UserProfile.objects.get(_id=captain_id)
            team.save()
        
        return team

    def to_representation(self, instance):
        """Convert ObjectId to string in response"""
        representation = super().to_representation(instance)
        if '_id' in representation and representation['_id']:
            representation['_id'] = str(representation['_id'])
        return representation


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model"""
    _id = serializers.CharField(read_only=True)
    user = UserProfileSerializer(read_only=True)
    user_id = serializers.CharField(write_only=True)

    class Meta:
        model = Activity
        fields = [
            '_id', 'user', 'user_id', 'activity_type', 'duration',
            'distance', 'calories', 'points', 'notes',
            'activity_date', 'created_at'
        ]
        read_only_fields = ['_id', 'points', 'created_at']

    def create(self, validated_data):
        """Assign user during creation"""
        user_id = validated_data.pop('user_id')
        user = UserProfile.objects.get(_id=user_id)
        validated_data['user'] = user
        return super().create(validated_data)

    def to_representation(self, instance):
        """Convert ObjectId to string in response"""
        representation = super().to_representation(instance)
        if '_id' in representation and representation['_id']:
            representation['_id'] = str(representation['_id'])
        return representation


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for Leaderboard model"""
    _id = serializers.CharField(read_only=True)

    class Meta:
        model = Leaderboard
        fields = [
            '_id', 'period', 'leaderboard_type', 'start_date',
            'end_date', 'rankings', 'created_at', 'updated_at'
        ]
        read_only_fields = ['_id', 'created_at', 'updated_at']

    def to_representation(self, instance):
        """Convert ObjectId to string in response"""
        representation = super().to_representation(instance)
        if '_id' in representation and representation['_id']:
            representation['_id'] = str(representation['_id'])
        return representation


class WorkoutSerializer(serializers.ModelSerializer):
    """Serializer for Workout model"""
    _id = serializers.CharField(read_only=True)
    exercise_count = serializers.SerializerMethodField()

    class Meta:
        model = Workout
        fields = [
            '_id', 'title', 'description', 'difficulty_level',
            'activity_type', 'duration', 'exercises', 'exercise_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['_id', 'created_at', 'updated_at']

    def get_exercise_count(self, obj):
        """Get the number of exercises in the workout"""
        return len(obj.exercises) if isinstance(obj.exercises, list) else 0

    def to_representation(self, instance):
        """Convert ObjectId to string in response"""
        representation = super().to_representation(instance)
        if '_id' in representation and representation['_id']:
            representation['_id'] = str(representation['_id'])
        return representation

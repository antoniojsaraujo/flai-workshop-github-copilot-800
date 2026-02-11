from django.core.management.base import BaseCommand
from pymongo import MongoClient
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        self.stdout.write('Clearing existing data...')
        # Clear existing collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create unique index on email
        db.users.create_index('email', unique=True)
        self.stdout.write(self.style.SUCCESS('Created unique index on email field'))

        # Marvel superheroes data
        marvel_heroes = [
            {
                'name': 'Iron Man',
                'email': 'tony.stark@avengers.com',
                'team': 'Team Marvel',
                'avatar': 'ironman.png',
                'fitness_level': 'advanced'
            },
            {
                'name': 'Captain America',
                'email': 'steve.rogers@avengers.com',
                'team': 'Team Marvel',
                'avatar': 'captainamerica.png',
                'fitness_level': 'expert'
            },
            {
                'name': 'Black Widow',
                'email': 'natasha.romanoff@avengers.com',
                'team': 'Team Marvel',
                'avatar': 'blackwidow.png',
                'fitness_level': 'expert'
            },
            {
                'name': 'Thor',
                'email': 'thor@asgard.com',
                'team': 'Team Marvel',
                'avatar': 'thor.png',
                'fitness_level': 'expert'
            },
            {
                'name': 'Hulk',
                'email': 'bruce.banner@avengers.com',
                'team': 'Team Marvel',
                'avatar': 'hulk.png',
                'fitness_level': 'expert'
            }
        ]

        # DC superheroes data
        dc_heroes = [
            {
                'name': 'Batman',
                'email': 'bruce.wayne@justiceleague.com',
                'team': 'Team DC',
                'avatar': 'batman.png',
                'fitness_level': 'expert'
            },
            {
                'name': 'Superman',
                'email': 'clark.kent@justiceleague.com',
                'team': 'Team DC',
                'avatar': 'superman.png',
                'fitness_level': 'expert'
            },
            {
                'name': 'Wonder Woman',
                'email': 'diana.prince@justiceleague.com',
                'team': 'Team DC',
                'avatar': 'wonderwoman.png',
                'fitness_level': 'expert'
            },
            {
                'name': 'Flash',
                'email': 'barry.allen@justiceleague.com',
                'team': 'Team DC',
                'avatar': 'flash.png',
                'fitness_level': 'expert'
            },
            {
                'name': 'Aquaman',
                'email': 'arthur.curry@justiceleague.com',
                'team': 'Team DC',
                'avatar': 'aquaman.png',
                'fitness_level': 'advanced'
            }
        ]

        # Insert users
        self.stdout.write('Creating users...')
        all_users = marvel_heroes + dc_heroes
        users_result = db.users.insert_many(all_users)
        user_ids = users_result.inserted_ids
        self.stdout.write(self.style.SUCCESS(f'Created {len(user_ids)} users'))

        # Create teams
        self.stdout.write('Creating teams...')
        teams = [
            {
                'name': 'Team Marvel',
                'description': 'Earth\'s Mightiest Heroes',
                'members': [str(uid) for uid, user in zip(user_ids[:5], all_users[:5])],
                'created_at': datetime.now()
            },
            {
                'name': 'Team DC',
                'description': 'Justice League Heroes',
                'members': [str(uid) for uid, user in zip(user_ids[5:], all_users[5:])],
                'created_at': datetime.now()
            }
        ]
        teams_result = db.teams.insert_many(teams)
        self.stdout.write(self.style.SUCCESS(f'Created {len(teams_result.inserted_ids)} teams'))

        # Create activities
        self.stdout.write('Creating activities...')
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weightlifting', 'Yoga', 'Boxing']
        activities = []
        
        for i, user_id in enumerate(user_ids):
            user = all_users[i]
            # Each user gets 5-10 activities
            num_activities = random.randint(5, 10)
            for j in range(num_activities):
                days_ago = random.randint(0, 30)
                activity_date = datetime.now() - timedelta(days=days_ago)
                activity_type = random.choice(activity_types)
                
                activities.append({
                    'user_id': str(user_id),
                    'user_name': user['name'],
                    'team': user['team'],
                    'activity_type': activity_type,
                    'duration': random.randint(15, 120),  # minutes
                    'calories': random.randint(100, 800),
                    'distance': round(random.uniform(1.0, 15.0), 2) if activity_type in ['Running', 'Cycling', 'Swimming'] else 0,
                    'date': activity_date,
                    'notes': f'{activity_type} session for hero training'
                })
        
        activities_result = db.activities.insert_many(activities)
        self.stdout.write(self.style.SUCCESS(f'Created {len(activities_result.inserted_ids)} activities'))

        # Create leaderboard
        self.stdout.write('Creating leaderboard...')
        leaderboard = []
        for i, user_id in enumerate(user_ids):
            user = all_users[i]
            # Calculate total points from activities
            user_activities = [a for a in activities if a['user_id'] == str(user_id)]
            total_calories = sum(a['calories'] for a in user_activities)
            total_duration = sum(a['duration'] for a in user_activities)
            points = total_calories + (total_duration * 2)
            
            leaderboard.append({
                'user_id': str(user_id),
                'user_name': user['name'],
                'team': user['team'],
                'points': points,
                'activities_count': len(user_activities),
                'total_calories': total_calories,
                'total_duration': total_duration,
                'rank': 0,  # Will be calculated
                'updated_at': datetime.now()
            })
        
        # Sort by points and assign ranks
        leaderboard.sort(key=lambda x: x['points'], reverse=True)
        for rank, entry in enumerate(leaderboard, 1):
            entry['rank'] = rank
        
        leaderboard_result = db.leaderboard.insert_many(leaderboard)
        self.stdout.write(self.style.SUCCESS(f'Created {len(leaderboard_result.inserted_ids)} leaderboard entries'))

        # Create workouts
        self.stdout.write('Creating workout suggestions...')
        workouts = [
            {
                'name': 'Super Soldier Training',
                'description': 'Intensive workout for peak human performance',
                'difficulty': 'advanced',
                'duration': 60,
                'exercises': [
                    {'name': 'Push-ups', 'reps': 50, 'sets': 3},
                    {'name': 'Pull-ups', 'reps': 20, 'sets': 3},
                    {'name': 'Squats', 'reps': 50, 'sets': 3},
                    {'name': 'Plank', 'duration': '2 minutes', 'sets': 3}
                ],
                'target_muscles': ['chest', 'back', 'legs', 'core'],
                'recommended_for': ['advanced', 'expert']
            },
            {
                'name': 'Speedster Cardio',
                'description': 'High-intensity cardio for maximum speed',
                'difficulty': 'intermediate',
                'duration': 45,
                'exercises': [
                    {'name': 'Sprint Intervals', 'duration': '30 seconds', 'sets': 10},
                    {'name': 'Jump Rope', 'duration': '5 minutes', 'sets': 3},
                    {'name': 'Burpees', 'reps': 20, 'sets': 3},
                ],
                'target_muscles': ['legs', 'cardiovascular'],
                'recommended_for': ['intermediate', 'advanced', 'expert']
            },
            {
                'name': 'Warrior Strength',
                'description': 'Build strength like an Amazonian warrior',
                'difficulty': 'advanced',
                'duration': 75,
                'exercises': [
                    {'name': 'Deadlifts', 'reps': 10, 'sets': 4, 'weight': 'progressive'},
                    {'name': 'Bench Press', 'reps': 10, 'sets': 4, 'weight': 'progressive'},
                    {'name': 'Overhead Press', 'reps': 10, 'sets': 3, 'weight': 'progressive'},
                    {'name': 'Barbell Rows', 'reps': 10, 'sets': 4, 'weight': 'progressive'}
                ],
                'target_muscles': ['full body', 'strength'],
                'recommended_for': ['advanced', 'expert']
            },
            {
                'name': 'Flexibility Flow',
                'description': 'Yoga and stretching for flexibility and balance',
                'difficulty': 'beginner',
                'duration': 30,
                'exercises': [
                    {'name': 'Sun Salutation', 'reps': 5},
                    {'name': 'Warrior Pose', 'duration': '1 minute', 'sets': 2},
                    {'name': 'Tree Pose', 'duration': '1 minute', 'sets': 2},
                    {'name': 'Child Pose', 'duration': '2 minutes'}
                ],
                'target_muscles': ['flexibility', 'balance', 'core'],
                'recommended_for': ['beginner', 'intermediate', 'advanced', 'expert']
            },
            {
                'name': 'Combat Training',
                'description': 'Mixed martial arts and boxing workout',
                'difficulty': 'intermediate',
                'duration': 60,
                'exercises': [
                    {'name': 'Heavy Bag', 'duration': '3 minutes', 'sets': 5},
                    {'name': 'Shadow Boxing', 'duration': '3 minutes', 'sets': 3},
                    {'name': 'Kicks Practice', 'reps': 20, 'sets': 3},
                    {'name': 'Core Work', 'duration': '10 minutes'}
                ],
                'target_muscles': ['full body', 'cardio', 'coordination'],
                'recommended_for': ['intermediate', 'advanced', 'expert']
            }
        ]
        
        workouts_result = db.workouts.insert_many(workouts)
        self.stdout.write(self.style.SUCCESS(f'Created {len(workouts_result.inserted_ids)} workout suggestions'))

        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(self.style.SUCCESS(f'Users: {len(user_ids)}'))
        self.stdout.write(self.style.SUCCESS(f'Teams: {len(teams_result.inserted_ids)}'))
        self.stdout.write(self.style.SUCCESS(f'Activities: {len(activities_result.inserted_ids)}'))
        self.stdout.write(self.style.SUCCESS(f'Leaderboard: {len(leaderboard_result.inserted_ids)}'))
        self.stdout.write(self.style.SUCCESS(f'Workouts: {len(workouts_result.inserted_ids)}'))

        client.close()

from django.core.management.base import BaseCommand
from django.conf import settings
from pymongo import MongoClient
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activity, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Clear existing data using MongoDB commands
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]
        db.users.drop()
        db.teams.drop()
        db.activity.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Save users individually to ensure they are properly saved
        users = [
            User(email='thundergod@mhigh.edu', name='Thor', age=30),
            User(email='metalgeek@mhigh.edu', name='Tony Stark', age=45),
            User(email='zerocool@mhigh.edu', name='Steve Rogers', age=100),
            User(email='crashoverride@mhigh.edu', name='Bruce Banner', age=40),
            User(email='sleeptoken@mhigh.edu', name='Natasha Romanoff', age=35),
        ]
        for user in users:
            user.save()

        # Create teams
        team1 = Team(name='Blue Team')
        team2 = Team(name='Gold Team')
        team1.save()
        team2.save()

        # Update activities to reference saved users
        activities = [
            Activity(user=users[0], activity_type='Cycling', duration=60),
            Activity(user=users[1], activity_type='Crossfit', duration=120),
            Activity(user=users[2], activity_type='Running', duration=90),
            Activity(user=users[3], activity_type='Strength', duration=30),
            Activity(user=users[4], activity_type='Swimming', duration=75),
        ]
        # Save activities individually to ensure related objects are saved
        for activity in activities:
            activity.save()

        # Create leaderboard entries
        leaderboard_entries = [
            Leaderboard(team=team1, points=100),
            Leaderboard(team=team2, points=90),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)

        # Create workouts
        workouts = [
            Workout(name='Cycling Training', description='Training for a road cycling event', duration=60),
            Workout(name='Crossfit', description='Training for a crossfit competition', duration=120),
            Workout(name='Running Training', description='Training for a marathon', duration=90),
            Workout(name='Strength Training', description='Training for strength', duration=30),
            Workout(name='Swimming Training', description='Training for a swimming competition', duration=75),
        ]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))

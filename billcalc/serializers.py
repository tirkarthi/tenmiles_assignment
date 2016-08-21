from rest_framework import serializers
from .models import *


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('id', 'name', 'company_info', 'email')


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'start_date', 'cost_per_hour', 'client')

    def validate(self, attrs):
        '''
        Validate that the date is within the current date
        '''
        import datetime

        if attrs['start_date'] > datetime.date.today():
            raise serializers.ValidationError(
                "Date should be less than or equal the current date")

        return attrs


class TimeSheetSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeSheet
        fields = ('id', 'date', 'time_spent', 'project')

    def validate(self, attrs):
        '''
        Validate that the date is within the current date and project start date
        '''
        import datetime

        if attrs['date'] > datetime.date.today():
            raise serializers.ValidationError(
                "Date should be less than or equal the current date")

        if attrs['date'] < attrs['project'].start_date:
            raise serializers.ValidationError(
                "Date should be greater than or equal to project start date")

        return attrs

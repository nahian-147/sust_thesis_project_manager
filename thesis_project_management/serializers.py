from rest_framework import serializers
from .models import Team, TeamProgress, Arrangement, TeamParticipation


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"

    def validate(self, attrs):
        pass


class TeamProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamProgress
        fields = "__all__"

    def validate(self, attrs):
        pass


class ArrangementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arrangement
        fields = "__all__"

    def validate(self, attrs):
        pass


class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamParticipation
        fields = "__all__"

    def validate(self, attrs):
        pass

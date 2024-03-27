from rest_framework import serializers
from social_network.models import FriendRequest


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status']
        read_only_fields = ('from_user', 'status',)

    def create(self, validated_data):
        # Ensure users cannot send a request to themselves
        if validated_data['from_user'] == validated_data['to_user']:
            raise serializers.ValidationError("You cannot send a friend request to yourself.")
        return super().create(validated_data)

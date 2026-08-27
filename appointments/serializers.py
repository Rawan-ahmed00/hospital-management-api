from rest_framework import serializers
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = '__all__'

    def validate(self, data):
        doctor = data.get('doctor')
        date = data.get('date')
        time = data.get('time')

        appointment_id = self.instance.id if self.instance else None

        existing_appointment = Appointment.objects.filter(
            doctor=doctor,
            date=date,
            time=time
        ).exclude(
            id=appointment_id
        ).exists()

        if existing_appointment:
            raise serializers.ValidationError(
                'This doctor already has an appointment at this date and time.'
            )

        return data
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from measurement.models import Sensor, Measurement
from measurement.serializers import SensorDetailSerializer, MeasurementSerializer, SensorSerializer


class SensorView(ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class MeasurementView(CreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def post(self, request, *args, **kwargs):
        if request.data.get('sensor') is None or request.data.get('temperature') is None:
            return Response({'error': "need to receive 'sensor' and 'temperature'"})
        try:
            sensor = Sensor.objects.get(id=request.data.get('sensor'))
            m = Measurement.objects.create(temperature=request.data.get('temperature'),
                                           sensor=sensor,
                                           photo=request.data.get('photo'))
            return Response({'sensor': m.sensor.id, 'temperature': m.temperature, 'created_at': m.created_at})
        except ObjectDoesNotExist:
            return Response({'error': 'indicated sensor is absent in database'})


class SensorDetailView(RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer

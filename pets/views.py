from rest_framework.views import APIView, Response, Request
from django.forms.models import model_to_dict
from .models import Pet
from .serializers import PetSerializer
from django.shortcuts import get_object_or_404

class PetsView(APIView):
    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, 201)

    def get(self, request: Request) -> Response:
        pets = Pet.objects.all()

        pet_serializer = PetSerializer(pets, many=True)
        
        return Response(pet_serializer.data)

class PetsViewId(APIView):
    def patch(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)

        serializer = PetSerializer(pet, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)

    def get(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)

        pet_serializer = PetSerializer(pet)

        return Response(pet_serializer.data)

    def delete(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)

        pet.delete()

        return Response(status=204)
from rest_framework.views import APIView, Request, Response, status
from rest_framework.pagination import PageNumberPagination
from .serializers import PetsSerializer
from .models import Pet
from groups.models import Group
from traits.models import Trait


class PetView(APIView, PageNumberPagination):
    def post(self, req: Request):
        serializer = PetsSerializer(data=req.data)

        serializer.is_valid(raise_exception=True)

        group_data = serializer.validated_data.pop("group")
        trait_data = serializer.validated_data.pop("traits")
        pet_data = serializer.validated_data

        find_group = Group.objects.filter(
            scientific_name__icontains=group_data["scientific_name"]
        ).first()

        if not find_group:
            find_group = Group.objects.create(**group_data)

        pet_data = Pet.objects.create(**pet_data, group=find_group)

        for trait in trait_data:
            find_trait = Trait.objects.filter(name__icontains=trait["name"]).first()

            if not find_trait:
                find_trait = Trait.objects.create(**trait)

            pet_data.traits.add(find_trait)

        serializer = PetsSerializer(pet_data)

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, req: Request):
        pet_data = Pet.objects.all()

        result_page = self.paginate_queryset(pet_data, req)

        serializer = PetsSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

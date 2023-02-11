from rest_framework.views import APIView, Request, Response, status
from rest_framework.pagination import PageNumberPagination
from .serializers import PetsSerializer
from .models import Pet
from groups.models import Group
from traits.models import Trait
from django.shortcuts import get_object_or_404


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
        trait_param = req.query_params.get("trait")

        if trait_param:
            pets = Pet.objects.filter(traits__name=trait_param).all()

            result_page = self.paginate_queryset(pets, req)

            serializer = PetsSerializer(pets, many=True)

            return self.get_paginated_response(serializer.data)

        pet_data = Pet.objects.all()

        result_page = self.paginate_queryset(pet_data, req)

        serializer = PetsSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


class PetInfoParamView(APIView):
    def get(self, req: Request, pet_id):
        pet_data = get_object_or_404(Pet, pk=pet_id)

        serializer = PetsSerializer(pet_data)

        return Response(serializer.data)

    def delete(self, req: Request, pet_id):
        pet_data = get_object_or_404(Pet, pk=pet_id)

        pet_data.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, req: Request, pet_id):
        pet = get_object_or_404(Pet, pk=pet_id)
        serializer = PetsSerializer(data=req.data, partial=True)

        serializer.is_valid(raise_exception=True)

        group_data = serializer.validated_data.pop("group", None)
        trait_data = serializer.validated_data.pop("traits", None)
        pet_data = serializer.validated_data

        if group_data:
            try:
                find_group = Group.objects.get(
                    scientific_name__iexact=group_data["scientific_name"]
                )
                pet.group = find_group
            except Group.DoesNotExist:
                new_group = Group.objects.create(**group_data)
                pet.group = new_group

        if trait_data:
            list_trait = []

            for trait in trait_data:
                find_trait = Trait.objects.filter(name__iexact=trait["name"]).first()

                if find_trait:
                    list_trait.append(find_trait)
                else:
                    new_trait = Trait.objects.create(**trait)
                    list_trait.append(new_trait)

            pet.traits.set(list_trait)

        for key, value in pet_data.items():
            setattr(pet, key, value)

        pet.save()

        serializer = PetsSerializer(pet)

        return Response(serializer.data)

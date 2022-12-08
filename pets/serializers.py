from rest_framework import serializers
from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer
from .models import SexPet, Pet
from groups.models import Group
from traits.models import Trait

class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices=SexPet.choices, default=SexPet.NOT_INFORMED)
    traits_count = serializers.SerializerMethodField()

    group = GroupSerializer()
    traits = TraitSerializer(many=True)

    def get_traits_count(self, instance):
        traits = instance.traits.all()
        return len(traits)

    def create(self, validated_data: dict) -> Pet:
        group_data  = validated_data.pop("group")
        traits_data = validated_data.pop("traits")
        
        group, _ = Group.objects.get_or_create(**group_data)

        pet = Pet.objects.create(**validated_data, group=group)

        for trait in traits_data:
            x, _ = Trait.objects.get_or_create(**trait)
            x.pet.add(pet)     

        return pet

    def update(self, instance: Pet, validated_data: dict):
        group_data  = validated_data.pop("group", None)
        traits_data = validated_data.pop("traits", None)

        if group_data:
            group, _ = Group.objects.get_or_create(**group_data)
            instance.group = group

        if traits_data:
            trait_list = []
            for trait in traits_data:
                x, _ = Trait.objects.get_or_create(**trait)
                trait_list.append(x)
            instance.traits.set(trait_list)

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance
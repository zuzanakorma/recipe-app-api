"""Serializers for recipe APIs"""

from rest_framework import serializers
from core.models import Recipe, Tag



class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags"""
    class Meta():
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes"""
    tags = TagSerializer(many=True, required=False)
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
        read_only_fields = ['id']

    # code refactoring
    def _get_or_create_tags(self, tags, recipe):
        """handle getting or creating tags as needed"""
        # context is use with serializers
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)

    # nested serializers are by default read_only, need to overwrite- custom create
    def create(self, validated_data):
        """Create a recipe."""
        # remove tags from validated data, if exist, else []
        tags = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)
        return recipe


    def update(self, instance, validated_data):
        """Update recipe"""
        tags = validated_data.pop('tags', None)
        if tags is not None:
            # clear tags and create again(new)
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']




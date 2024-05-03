from account.serializers import UserSerializer
from django.utils import timezone
from django.utils.timesince import timesince
from rest_framework import serializers

from .models import OfferProduct, QuoteAttachment, QuoteOffer, QuoteProduct, QuoteRequest


class QuoteAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteAttachment
        fields = "__all__"


class QuoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(allow_null=True, required=False)
    attachments = QuoteAttachmentSerializer(many=True, read_only=True)
    created_since = serializers.SerializerMethodField()
    due_date_display = serializers.SerializerMethodField(read_only=True)
    due_time_display = serializers.SerializerMethodField(read_only=True)

    products = serializers.SerializerMethodField(read_only=True)
    offers = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = QuoteRequest
        fields = "__all__"

    def get_attachments(self, obj):
        attachments = obj.quoteattachment_set.all()
        serializer = QuoteAttachmentSerializer(attachments, many=True)
        return serializer.data

    def get_created_since(self, obj):
        return timesince(obj.created, timezone.now())

    def get_due_date_display(self, obj):
        return obj.due_date.date()

    def get_due_time_display(self, obj):
        due_time = obj.due_date.time()
        formatted_time = due_time.strftime("%I:%M %p")
        return formatted_time

    def get_products(self, obj):
        qs = obj.quoteproduct_set.all()
        serializer = QuoteProductSerializer(qs, many=True)
        return serializer.data

    def get_offers(self, obj):
        qs = obj.quoteoffer_set.all()
        serializer = QuoteOfferSerializer(qs, many=True)
        return serializer.data


class QuoteProductSerializer(serializers.ModelSerializer):
    unit_display = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = QuoteProduct
        fields = "__all__"

    def get_unit_display(self, obj):
        return obj.get_unit_display()


class OfferProductSerializer(serializers.ModelSerializer):
    unit_display = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OfferProduct
        fields = "__all__"

    def get_unit_display(self, obj):
        return obj.get_unit_display()


class QuoteOfferSerializer(serializers.ModelSerializer):
    user = UserSerializer(allow_null=True, required=False)
    created_since = serializers.SerializerMethodField(read_only=True)
    status_display = serializers.SerializerMethodField(read_only=True)

    products = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = QuoteOffer
        fields = "__all__"

    def get_created_since(self, obj):
        return timesince(obj.created, timezone.now())

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_products(self, obj):
        qs = obj.offerproduct_set.all()
        serializer = OfferProductSerializer(qs, many=True)
        return serializer.data

from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer, \
    StringRelatedField, PrimaryKeyRelatedField, HyperlinkedRelatedField, \
    HyperlinkedIdentityField, SerializerMethodField

from .models import Album, Track, Singer

class SingerSerializer(ModelSerializer):
    class Meta:
        model = Singer
        fields = ['first_name', 'last_name']


class TrackUpdateDetailSerializer(ModelSerializer):
    singers = SingerSerializer(many=True)

    class Meta:
        model = Track
        fields = ['name', 'active', 'singers']

    def update(self, instance, validated_data):
        if validated_data.get('singers'):
            singers_list = validated_data.pop('singers')
            singer_object_list = []
            for elem in singers_list:
                singer, _ = Singer.objects.get_or_create(**elem)
                print(_)
                singer_object_list.append(singer)
            instance.singers.set(singer_object_list)

        instance.active = validated_data.get('active', instance.active)
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        return instance



class TrackModelListSerializer(ModelSerializer):
    singers = SingerSerializer(many=True)

    class Meta:
        model = Track
        fields = ['name', 'active', 'singers']

    def create(self, validated_data):
        singers_list = validated_data.pop('singers')

        singer_object_list = []
        for elem in singers_list:
            singer, _ = Singer.objects.get_or_create(**elem)
            singer_object_list.append(singer)

        track, _ = Track.objects.get_or_create(**validated_data)
        track.singers.set(singer_object_list)

        return track


class TrackListSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Track
        fields = ['name', 'url']


class TrackDetailSerializer(ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'



class TrackViewsetSerializer(ModelSerializer):
    class Meta:
        model = Track
        fields = ['name', 'album', 'active', 'singers']


class TrackSerializer(ModelSerializer):
    class Meta:
        model = Track
        fields = ['name', 'active', 'singers']


class AlbumListSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Album
        fields = ['name', 'url']
        # extra_kwargs = {
        #     'url': {'view_name': 'album-detail', 'lookup_url_kwarg': 'question_id'},
        # }

    def to_representation(self, instance):
        # print(instance)
        # print(type(instance))
        ret = super().to_representation(instance)
        ret['mohammad'] = 'ashkan'
        return ret

    def to_internal_value(self, data):
        data = data['time']['data']
        data_ret = super().to_internal_value(data)

        return data_ret


class AlbumDetailSerializer(ModelSerializer):
    track_set = TrackSerializer(many=True, read_only=True)
    field1 = SerializerMethodField(method_name='compute_field1')

    # tracks = StringRelatedField(source='track_set', many=True, read_only=True)
    # tracks = PrimaryKeyRelatedField(source='track_set', many=True, read_only=True)
    # tracks2 = HyperlinkedRelatedField(source='track_set', many=True, read_only=True,
    #                                  view_name='track-detail')
    # tracks1= HyperlinkedIdentityField(source='track_set', many=True, view_name='track-detail')

    class Meta:
        model = Album
        fields = ['name', 'is_active', 'track_set', 'field1']

    def compute_field1(self, obj):
        return obj.id

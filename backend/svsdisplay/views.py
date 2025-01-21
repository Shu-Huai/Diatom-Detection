# svsdisplay/views.py
from .models import DiatomSlice, DiatomPatch
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def get_images(request):
    slices = DiatomSlice.objects.all()
    patches = DiatomPatch.objects.all()

    slice_data = [{'id': slice.id, 'image': slice.image.url} for slice in slices]
    patch_data = [{'id': patch.id, 'image': patch.image.url} for patch in patches]

    response = {'diatom_slices': slice_data, 'diatom_patches': patch_data}
    print("Response JSON:", response)  # 打印返回的 JSON
    return Response(response, status=200)

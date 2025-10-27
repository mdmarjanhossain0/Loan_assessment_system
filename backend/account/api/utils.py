import os
from django.conf import settings
from django.core.files.storage import default_storage, FileSystemStorage

from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def save_file(file, file_path, file_name) :
			url = os.path.join(settings.MEDIA_ROOT , str(file_path))
			storage = FileSystemStorage(location=url)
			print(storage.location)
			if storage.exists(url) :
				print("Exist")
			else :
				print("Not Exist")
				os.makedirs(url)
			with storage.open(file_name, 'wb+') as destination:
				for chunk in image.chunks():
					destination.write(chunk)
				destination.close()
			return "/media/" + file_path + file_name
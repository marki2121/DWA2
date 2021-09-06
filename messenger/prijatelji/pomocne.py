from prijatelji.models import ZahtijevPrijateljstva

def get_friend_request_or_false(posiljatelj, primatelj):
    try:
        return ZahtijevPrijateljstva.objects.get(posiljatelj=posiljatelj, primatelj=primatelj, is_active=True)
    except ZahtijevPrijateljstva.DoesNotExist:
        return False

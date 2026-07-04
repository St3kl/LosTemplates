from django.core.cache import cache


DOWNLOAD_COOLDOWN = 10  # seconds


class DownloadSecurity:

    @staticmethod
    def can_download(user):

        key = f"download:{user.id}"

        if cache.get(key):
            return False

        cache.set(
            key,
            True,
            timeout=DOWNLOAD_COOLDOWN,
        )

        return True
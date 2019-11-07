"""
Hooks for customizing login with social providers
https://django-allauth.readthedocs.io/en/latest/advanced.html
"""
from allauth.account.signals import user_logged_in
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.dispatch import receiver
from civictechprojects.models import ProjectFile, FileCategory
from democracylab.models import Contributor
from django.contrib.auth.models import User
from django.utils import timezone
import requests


def _get_avatar_url(sociallogin):
    if sociallogin.account.provider.startswith('linkedin'):
        return _get_linkedin_avatar_url(sociallogin)
    else:
        return sociallogin.account.get_avatar_url()

def _get_linkedin_avatar_url(sociallogin):
    response = requests.get(
        'https://api.linkedin.com/v2/me?projection=(profilePicture(displayImage~:playableStreams))',
        headers={'Authorization': f'Bearer {sociallogin.token}'}
    )
    body = response.json()
    return body.get('profilePicture').get('displayImage~').get(
        'elements')[-1].get('identifiers')[0].get('identifier')

def _update_user_avatar_url(sociallogin):
    owner = sociallogin.user.contributor
    user_avatar_url = _get_avatar_url(sociallogin)
    if user_avatar_url:
        file_json = {
            'publicUrl': user_avatar_url,
            'file_user': owner,
            'file_category': FileCategory.THUMBNAIL.value,
            'visibility': 'PUBLIC',
            'fileName': f'{owner.first_name}{owner.last_name}_thumbnail.{sociallogin.account.provider} avatar',
            'key': f'{sociallogin.account.provider}/{owner.username}'
        }
        ProjectFile.replace_single_file(owner, FileCategory.THUMBNAIL, file_json)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def new_user(self, request, sociallogin):
        email = sociallogin.account.get_provider().extract_common_fields(
                                                   sociallogin.account.extra_data).get('email').lower()

        # This account may belong to an existing user
        user = User.objects.filter(username=email).first()
        if user:
            # Preserve current password (sociallogin assigns an unusable password)
            if user.has_usable_password():
                sociallogin.account.extra_data.update(password=user.password)
            return Contributor.objects.get_by_natural_key(user.username)
        else:
            return Contributor(email_verified=True, last_login=timezone.now())

    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a
        social provider, but before the login is actually processed.

        You can use this hook to intervene, e.g. abort the login by
        raising an ImmediateHttpResponse
        """
        # standardizing fields across different providers
        data = sociallogin.account.get_provider().extract_common_fields(
            sociallogin.account.extra_data)

        full_name = data.get('name')
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        sociallogin.user.first_name = first_name or full_name.split()[0]
        sociallogin.user.last_name = last_name or ' '.join(full_name.split()[1:])

        sociallogin.user.username = sociallogin.user.email.lower()

        existing_password = sociallogin.account.extra_data.get('password')
        if existing_password:
            sociallogin.user.password = existing_password

        if sociallogin.is_existing:
            sociallogin.user.save()  # Update only the user
            return

        # Upsert the User and the SocialAccount
        sociallogin.connect(request, sociallogin.user)

    @receiver(user_logged_in)
    def set_avatar_upon_login(sender, sociallogin, **kwargs):
        _update_user_avatar_url(sociallogin)
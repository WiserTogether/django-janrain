from base64 import b64encode
from hashlib import sha1

from django.contrib.auth.models import User

from janrain.constants import PROVIDER_LINKEDIN
from janrain.models import JanrainUser


class JanrainBackend(object):
    supports_anonymous_user = False

    def authenticate(self, profile):
        """
        Authenticate users based on their e-mail address.  Email addresses are
        unique in our system, and we only ever want a verified e-mail address.
        """

        email = profile.get('verifiedEmail', None)
        provider = profile.get('providerName', '').lower()

        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return self.create_user(profile)
            else:
                return user
        elif provider == PROVIDER_LINKEDIN:
            # If the provider the user is signing in with is LinkedIn, we have
            # to work around a bit since LinkedIn does not currently provide
            # email addresses via their API.  To do this, we check to see if a
            # JanrainUser object exists and if it does, return the associated
            # Django User object with it.  Otherwise, we'll create the Django
            # User object with the available profile information.
            try:
                # For LinkedIn, preferredUsername and identifier are the
                # fields that we are most likely able to count on for a match.
                # Please see the Janrain Profile Data API for more info:
                # https://rpxnow.com/docs#profile_data
                janrain_data = {'provider': provider}

                if 'preferredUsername' in profile:
                    janrain_data['username'] = profile.get('preferredUsername')

                # Identifier is listed as a guaranteed field, but it never
                # hurts to double check these things.
                if 'identifier' in profile:
                    janrain_data['identifier'] = profile.get('identifier')

                janrain_user = JanrainUser.objects.get(**janrain_data)
            except JanrainUser.DoesNotExist:
                return self.create_user(profile)
            else:
                return janrain_user.user

        return None

    def create_user(self, profile):
        """
        Creates a new Django User with the profile data returned from the
        chosen provider.
        """

        # django.contrib.auth.models.User.username is required and
        # has a max_length of 30 so to ensure that we don't go over
        # 30 characters we base64 encode the sha1 of the identifier
        # returned from janrain.
        hashed_username = b64encode(
            sha1(profile['identifier']).digest()
        )

        first_name, last_name = self.get_name_from_profile(profile)

        user = User(
            username=hashed_username,
            password='',
            first_name=first_name,
            last_name=last_name,
            email=self.get_email(profile)
        )

        user.set_unusable_password()
        user.is_staff = False
        user.is_superuser = False

        # TODO:  We are hooking into this for now, but will want to
        #        change this in the future once we have a full
        #        registration state machine working.  For the time
        #        being, any new user coming in through a provider we've
        #        configured in Janrain will have is_active set to
        #        False, which will trigger the registration form to
        #        appear so that the user can verify and/or fill in any
        #        information.
        user.is_active = False
        user.save()

        return user

    def get_user(self, uid):
        try:
            return User.objects.get(pk=uid)
        except User.DoesNotExist:
            return None

    def get_name_from_profile(self, p):
        nt = p.get('name')

        if type(nt) == dict:
            fname = nt.get('givenName')
            lname = nt.get('familyName')

            if fname and lname:
                return (fname, lname)
        dn = p.get('displayName')

        if len(dn) > 1 and dn.find(' ') != -1:
            (fname, lname) = dn.split(' ', 1)
            return (fname, lname)
        elif dn == None:
            return ('', '')
        else:
            return (dn, '')

    def get_email(self, p):
        return p.get('verifiedEmail') or p.get('email') or ''

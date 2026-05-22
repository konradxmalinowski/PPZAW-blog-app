import pytest
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.fixture
def active_user(db):
    return User.objects.create_user(
        username='activeuser', password='StrongPass123!', email='active@test.com', is_active=True
    )


class TestRegisterView:
    def test_register_page_loads(self, client):
        response = client.get(reverse('accounts:register'))
        assert response.status_code == 200

    def test_register_creates_inactive_user(self, client, db):
        client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'email': 'new@test.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        user = User.objects.filter(username='newuser').first()
        assert user is not None
        assert user.is_active is False

    def test_register_redirects_to_verify_sent(self, client, db):
        response = client.post(reverse('accounts:register'), {
            'username': 'newuser2',
            'email': 'new2@test.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        assert response.status_code == 302
        assert '/verify-email/sent/' in response.url


class TestLoginView:
    def test_login_page_loads(self, client):
        response = client.get(reverse('accounts:login'))
        assert response.status_code == 200

    def test_login_success_active_user(self, client, active_user):
        response = client.post(reverse('accounts:login'), {
            'username': 'activeuser',
            'password': 'StrongPass123!',
        })
        assert response.status_code == 302

    def test_login_fails_wrong_password(self, client, active_user):
        response = client.post(reverse('accounts:login'), {
            'username': 'activeuser',
            'password': 'wrongpass',
        })
        assert response.status_code == 200

    def test_login_fails_inactive_user(self, client, db):
        User.objects.create_user(username='inactive', password='pass123', is_active=False)
        response = client.post(reverse('accounts:login'), {
            'username': 'inactive',
            'password': 'pass123',
        })
        assert response.status_code == 200


class TestProfileView:
    def test_profile_requires_auth(self, client):
        response = client.get(reverse('accounts:profile'))
        assert response.status_code == 302
        assert '/login/' in response.url

    def test_profile_loads_for_authenticated_user(self, client, active_user):
        client.force_login(active_user)
        response = client.get(reverse('accounts:profile'))
        assert response.status_code == 200


class TestPasswordReset:
    def test_password_reset_page_loads(self, client):
        response = client.get(reverse('accounts:password_reset'))
        assert response.status_code == 200


class TestEmailVerification:
    def test_verify_email_sent_page_loads(self, client):
        response = client.get(reverse('accounts:verify_email_sent'))
        assert response.status_code == 200

    def test_invalid_token_redirects_to_login(self, client, db):
        import uuid
        fake_token = uuid.uuid4()
        response = client.get(reverse('accounts:verify_email', args=[fake_token]))
        assert response.status_code == 302
        assert '/login/' in response.url

    def test_valid_token_activates_user(self, client, db):
        from apps.accounts.models import EmailVerificationToken
        user = User.objects.create_user(
            username='inactivetest', password='pass123', email='inactive@test.com', is_active=False
        )
        token = EmailVerificationToken.objects.create(user=user)
        response = client.get(reverse('accounts:verify_email', args=[token.token]))
        user.refresh_from_db()
        assert user.is_active is True
        assert response.status_code == 302


class TestBackupCodes:
    def test_generate_backup_codes(self, db, active_user):
        from apps.accounts.models import TwoFactorBackupCode
        codes = TwoFactorBackupCode.generate_for_user(active_user)
        assert len(codes) == 8
        assert TwoFactorBackupCode.objects.filter(user=active_user).count() == 8

    def test_verify_and_consume_backup_code(self, db, active_user):
        from apps.accounts.models import TwoFactorBackupCode
        codes = TwoFactorBackupCode.generate_for_user(active_user)
        result = TwoFactorBackupCode.verify_and_consume(active_user, codes[0])
        assert result is True
        result_again = TwoFactorBackupCode.verify_and_consume(active_user, codes[0])
        assert result_again is False

    def test_wrong_backup_code_rejected(self, db, active_user):
        from apps.accounts.models import TwoFactorBackupCode
        TwoFactorBackupCode.generate_for_user(active_user)
        result = TwoFactorBackupCode.verify_and_consume(active_user, 'WRONGCODE')
        assert result is False

from saas_base.test import SaasTestCase
from saas_domain.models import Domain

TEST_DATA = {
    "hostname": "example.com",
    "provider": "null",
}


class TestDomainAPIWithOwner(SaasTestCase):
    user_id = SaasTestCase.OWNER_USER_ID

    def test_list_domains(self):
        self.force_login()

        resp = self.client.get('/m/domains/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), [])

        Domain.objects.create(tenant=self.tenant, hostname="example.com")
        resp = self.client.get('/m/domains/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 1)
        self.assertEqual(resp.json()[0]['hostname'], 'example.com')

    def test_create_domain(self):
        self.force_login()
        resp = self.client.post('/m/domains/', data=TEST_DATA)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()["hostname"], "example.com")
        self.assertEqual(resp.json()["verified"], False)

    def test_create_domain_with_invalid_provider(self):
        self.force_login()
        payload = {
            "hostname": "example.com",
            "provider": "invalid",
        }
        resp = self.client.post('/m/domains/', data=payload)
        self.assertEqual(resp.status_code, 400)


class TestDomainAPIWithGuestUser(SaasTestCase):
    user_id = SaasTestCase.GUEST_USER_ID

    def test_list_domains_with_read_permission(self):
        self.add_user_perms('tenant.read')
        self.force_login()

        resp = self.client.get('/m/domains/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), [])

        Domain.objects.create(tenant=self.tenant, hostname="example.com")
        resp = self.client.get('/m/domains/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 1)
        self.assertEqual(resp.json()[0]['hostname'], 'example.com')

    def test_list_domains_without_permission(self):
        self.force_login()
        resp = self.client.get('/m/domains/')
        self.assertEqual(resp.status_code, 403)

    def test_create_domain_with_admin_permission(self):
        self.add_user_perms('tenant.admin')
        self.force_login()
        resp = self.client.post('/m/domains/', data=TEST_DATA)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()["hostname"], "example.com")
        self.assertEqual(resp.json()["verified"], False)

    def test_create_domain_with_read_permission(self):
        resp = self.client.post('/m/domains/', data=TEST_DATA)
        self.assertEqual(resp.status_code, 403)

    def test_retrieve_domain_with_read_permission(self):
        self.add_user_perms('tenant.read')
        self.force_login()

        domain = Domain.objects.create(
            tenant=self.tenant,
            hostname="example.com",
            provider="null",
        )
        resp = self.client.get(f'/m/domains/{domain.pk}/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["verified"], False)

        resp = self.client.get(f'/m/domains/{domain.pk}/?verify=true')
        self.assertEqual(resp.json()["verified"], True)

    def test_enable_and_refresh_domain(self):
        self.add_user_perms('tenant.admin')
        self.force_login()
        domain = Domain.objects.create(
            tenant=self.tenant,
            hostname="example.com",
            provider="null",
        )

        # enable domain
        resp = self.client.post(f'/m/domains/{domain.pk}/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["instrument"]['ownership_status'], 'pending')

    def test_delete_domain_with_admin_permission(self):
        self.add_user_perms('tenant.admin')
        self.force_login()

        domain = Domain.objects.create(tenant=self.tenant, hostname="example.com")
        resp = self.client.delete(f'/m/domains/{domain.pk}/')
        self.assertEqual(resp.status_code, 204)

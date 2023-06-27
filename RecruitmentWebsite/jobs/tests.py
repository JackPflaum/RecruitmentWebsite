from django.test import TestCase
from django.urls import reverse, resolve
from .views import home, job_details, job_positions
from .models import JobPositions


class HomeTests(TestCase):
    """Tests for home view"""

    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        """the purpose is to verify that the root URL correctly mapped to the 'home' view"""
        view = resolve('/')
        self.assertEqual(view.func, home)
    

class NavigationBarTests(TestCase):
    """Tests for the top navigation bar"""

    # def test_navigation_links(self):
    #     response = self.client.get('/')
    #     self.assertContains(response, '<a href="{}">Home</a>')


class JobPositionsTests(TestCase):
    """Tests for job_positions view"""

    def setUp(self):
        """create JobPositions instance for test cases"""
        JobPositions.objects.create(job_title='Carpenter', company='Wood Inc', location='Perth', closing_date='2040-06-14')
        JobPositions.objects.create(job_title='Accountant', company='Munroes', location='Perth', closing_date='2040-06-14')
        JobPositions.objects.create(job_title='Electrician', company='Elextric', location='Fremantle', closing_date='2040-06-14')

    def test_job_positions_view_success_status(self):
        url = reverse('job_positions')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_job_positions_url_resolves_job_positions_view(self):
        """checking if the url pattern is resolving the 'job_positions' view"""
        view = resolve('/job_positions/')
        self.assertEqual(view.func, job_positions)

    def test_job_positions_search_box_good(self):
        """check job_positions search box returns the JobPositions objects that contains the users search term"""
        keyword_search = 'Perth'
        url = reverse('job_positions')
        response = self.client.get(url, {'search': keyword_search})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, keyword_search)

        # check correct number of 'jobs' are returned
        jobs_page = response.context['jobs'] # 'Page' object because of pagination
        jobs_count = jobs_page.paginator.count # get count of all jobs across all pages
        expected_count = 2 # two objects contain 'Perth' keyword out of 3
        self.assertEqual(jobs_count, expected_count)

    def test_job_positions_search_box_bad(self):
        """check job_positions search box returns 'No search results' when no JobPositions object matches user search term"""
        keyword_search = 'bad_keyword'
        url = reverse('job_positions')
        response = self.client.get(url, {'search': keyword_search})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No search results')
    
    def test_job_link_to_job_details_page(self):
        """check job links take user to job_details page"""
        job_details_url = reverse('job_details', kwargs={'id': 1}) # get url of Job Details page for first job
        job_positions_url = reverse('job_positions')
        response = self.client.get(job_positions_url)
        self.assertContains(response, job_details_url) # assert job link is present in the response HTML


class JobDetailsTest(TestCase):
    """Tests for job_details view"""

    def setUp(self):
        """create JobPositions instance for test cases"""
        JobPositions.objects.create(job_title='Carpenter', company='Wood Inc', location='Perth', closing_date='2040-06-14')
    
    def test_job_details_view_success_status(self):
        """returning status code 200 for an existing JobPositions object"""
        url = reverse('job_details', kwargs={'id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_job_details_view_not_found_status_code(self):
        """returning status code 404 for a JobPositions object that doesn't exist"""
        url = reverse('job_details', kwargs={'id': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_job_details_url_resolves_job_details_view(self):
        """checking if the url pattern is correctly resolving the 'job_details' view"""
        view = resolve('/job_details/1')
        self.assertEqual(view.func, job_details)
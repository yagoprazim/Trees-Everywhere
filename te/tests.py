from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from te.models import Account, Tree, PlantedTree

User = get_user_model()

class TreeTests(TestCase):
    def setUp(self):
        self.account1 = Account.objects.create(name='account1', active=True)
        self.account2 = Account.objects.create(name='account2', active=True)
        
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.user3 = User.objects.create_user(username='user3', password='password3')
        
        self.account1.users.add(self.user1, self.user2)
        self.account2.users.add(self.user3)
        
        self.tree1 = Tree.objects.create(name='tree1', scientific_name='sn1')
        self.tree2 = Tree.objects.create(name='tree2', scientific_name='sn2')
        self.tree3 = Tree.objects.create(name='tree3', scientific_name='sn3')
        
        self.planted_tree1 = PlantedTree.objects.create(tree=self.tree1, age=1, account=self.account1, user=self.user1, latitude=1.1, longitude=1.4)
        self.planted_tree2 = PlantedTree.objects.create(tree=self.tree2, age=2, account=self.account1, user=self.user2, latitude=2.1, longitude=2.4)
        self.planted_tree3 = PlantedTree.objects.create(tree=self.tree3, age=3, account=self.account2, user=self.user3, latitude=3.1, longitude=3.4)
        
        self.client = Client()
    
    # Check user's own trees are displayed
    def test_user_trees_template(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get(reverse('user-trees'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'tree1')
        self.assertNotContains(response, 'tree2')
        self.assertNotContains(response, 'tree3')

    # Check 403 for accessing another user's tree
    def test_forbidden_access_to_other_users_tree(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get(reverse('user-tree-detail', args=[self.planted_tree3.pk]))
        self.assertEqual(response.status_code, 403)

    # Check all trees from user accounts are displayed
    def test_user_accounts_all_trees_template(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get(reverse('user-accounts-trees'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'tree1')
        self.assertContains(response, 'tree2')
        self.assertNotContains(response, 'tree3')

    # Check single tree can be planted successfully
    def test_plant_tree(self):
        self.client.login(username='user1', password='password1')
        new_tree = Tree.objects.create(name='tree4', scientific_name='sn4')
        initial_count = PlantedTree.objects.count()

        self.client.post(reverse('user-trees-plant'), {
            'form-INITIAL_FORMS': 0,
            'form-TOTAL_FORMS': 1,
            'form-0-tree': new_tree.id,
            'form-0-age': 1,
            'form-0-account': self.account1.id,
            'form-0-latitude': 0.0,
            'form-0-longitude': 0.0,
        })

        self.assertEqual(PlantedTree.objects.count(), initial_count + 1)
        planted_tree = PlantedTree.objects.last()
        self.assertEqual(planted_tree.user, self.user1)
        self.assertEqual(planted_tree.tree, new_tree)

    # Check multiple trees can be planted successfully
    def test_plant_trees(self):
        self.client.login(username='user1', password='password1')
        tree4 = Tree.objects.create(name='tree4', scientific_name='sn5')
        tree5 = Tree.objects.create(name='tree5', scientific_name='sn6')
        initial_count = PlantedTree.objects.count()

        data = {
            'form-INITIAL_FORMS': 0,
            'form-TOTAL_FORMS': 2,
             # First user data
            'form-0-tree': tree4.id,
            'form-0-age': 1,
            'form-0-account': self.account1.id,
            'form-0-latitude': 0.0,
            'form-0-longitude': 0.0,
            # Second user data
            'form-1-tree': tree5.id,
            'form-1-age': 2,
            'form-1-account': self.account1.id,
            'form-1-latitude': 0.0,
            'form-1-longitude': 0.0
        }

        self.client.post(reverse('user-trees-plant'), data)
        self.assertEqual(PlantedTree.objects.count(), initial_count + 2)
        new_trees = PlantedTree.objects.filter(user=self.user1)
        self.assertTrue(new_trees.filter(tree=tree4).exists())
        self.assertTrue(new_trees.filter(tree=tree5).exists())

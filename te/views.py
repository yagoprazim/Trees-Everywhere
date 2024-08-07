from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, TemplateView, DetailView
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from te.models import Profile, Account, PlantedTree
from te.forms import LoginForm, ProfileForm, PlantedTreeFormSet
from te.seriallizers import PlantedTreeSeriallizer

class HomeView(TemplateView):
    template_name = 'index.html'

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            
            if user:
                login(request, user)
                next_url = request.GET.get('next', 'user-trees')
                return redirect(next_url)   
            else:
                messages.error(request,"Incorrect informations, try again.")  
        return render(request, 'login.html', {'form': form})

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        form = ProfileForm(instance=profile)
        return render(request, 'user-profile.html', {'profile': profile, 'form': form})

    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user-profile')
        return render(request, 'user-profile.html', {'profile': profile, 'form': form})
  
class PlantTreesView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get_formset_filter(self, request, data=None):
        formset = PlantedTreeFormSet(data)
        for form in formset:
            form.fields['account'].queryset = Account.objects.filter(users=request.user, active=True)
        return formset

    def get(self, request):
        formset = self.get_formset_filter(request)
        return render(request, 'user-trees-plant.html', {'formset': formset})

    def post(self, request):
        formset = self.get_formset_filter(request, data=request.POST)
        if formset.is_valid():
            data = [{
                "user": self.request.user,
                "tree": form.cleaned_data["tree"],
                "age": form.cleaned_data["age"],
                "account": form.cleaned_data["account"],
                "latitude": form.cleaned_data["latitude"],
                "longitude": form.cleaned_data["longitude"]
                }
                for form in formset if form.cleaned_data
            ]

            if len(data) == 1:
                self.request.user.plant_tree(data[0])
                return redirect('user-trees') 
            elif len(data) > 1:
                self.request.user.plant_trees(data)  
                return redirect('user-trees') 
            else:
                messages.error(request, "Please, fill out at least one complete form!")

        return render(request, 'user-trees-plant.html', {'formset': formset})

class UserTreesView(LoginRequiredMixin, ListView):
    model = PlantedTree
    template_name = 'trees-list.html'
    context_object_name = 'planted_trees'
    login_url = reverse_lazy('login')
    paginate_by = 10
    extra_context = {'page_title': 'All My Trees Planted'}

    def get_queryset(self):
        user_accounts = Account.objects.filter(users=self.request.user)
        return PlantedTree.objects.filter(account__in=user_accounts, user=self.request.user)

class UserAccountsAllTreesView(LoginRequiredMixin, ListView):
    model = PlantedTree
    template_name = 'trees-list.html'
    context_object_name = 'planted_trees'
    login_url = reverse_lazy('login')
    paginate_by = 10
    extra_context = {'page_title': 'All Trees Planted From My Accounts'}

    def get_queryset(self):
        user_accounts = Account.objects.filter(users=self.request.user)
        return PlantedTree.objects.filter(account__in=user_accounts)

class PlantedTreeDetailView(LoginRequiredMixin, DetailView):
    model = PlantedTree
    template_name = 'tree-detail.html'
    context_object_name = 'tree'
    login_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        tree = super().get_object(queryset)
        user = self.request.user

        if tree.user != user:
                raise PermissionDenied("You do not have permission to view this tree.")
        return tree

    def get(self, request, pk):
        tree = self.get_object()
        source = request.GET.get('source', reverse('user-trees'))
        return render(request, 'tree-detail.html', {
            'tree': tree,
            'back_url': source
        })

class UserTreesJsonView(ListAPIView):
    model = PlantedTree
    serializer_class = PlantedTreeSeriallizer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.plantedtree_set.all()


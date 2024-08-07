from django.urls import path
from te.views import HomeView, LoginView, PlantedTreeDetailView, ProfileView, UserTreesView, PlantTreesView, UserAccountsAllTreesView, UserTreesJsonView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/profile/', ProfileView.as_view(), name='user-profile'),
    path('user/trees/', UserTreesView.as_view(), name='user-trees'),
    path('user/trees/<int:pk>/details/', PlantedTreeDetailView.as_view(), name='user-tree-detail'),
    path('user/trees/plant/', PlantTreesView.as_view(), name='user-trees-plant'),
    path('user/accounts/all-trees/', UserAccountsAllTreesView.as_view(), name='user-accounts-trees'),
]

urlpatterns += [
    path('user/trees/json/', UserTreesJsonView.as_view(), name='user-trees-json'),
]
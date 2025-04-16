from django.urls import path

from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    #path("", BlogArticleListView.as_view(), name="articles_list"),
]
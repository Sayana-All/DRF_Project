from django.urls import path

from materials.apps import MaterialsConfig

app_name = MaterialsConfig.name

urlpatterns = [
    #path("", BlogArticleListView.as_view(), name="articles_list"),
]
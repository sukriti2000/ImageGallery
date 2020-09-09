from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
	path("",views.index,name="index"),
	path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
	path("Form_page",views.Form_page,name="Form_page"),
	path("Form",views.Form,name="Form"),
	path("Search",views.Search,name="Search"),
	path("api",views.api,name="api"),
	path("profile_pic/<int:user_id>",views.profile_pic,name="profile_pic"),
	path("add_like/<int:image_id>",views.add_like,name="add_like"),
	path("collection",views.collection,name="collection"),
	path("add_collection/<int:image_id>",views.add_collection,name="add_collection"),
	path("remove_collection/<int:image_id>",views.remove_collection,name="remove_collection"),
	path("edit_flip/<int:image_id>",views.edit_flip,name="edit_flip"),
	
	path("edit_contrast/<int:image_id>",views.edit_contrast,name="edit_contrast"),
	
	path("edit_bw/<int:image_id>",views.edit_bw,name="edit_bw"),
	
	path("edit_median/<int:image_id>",views.edit_median,name="edit_median"),
	
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

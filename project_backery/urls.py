"""project_backery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from backeryapp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('login/', views.login),
    path('signup/', views.signup),
    path('profile/',views.profile),
    path('profile_edit/<id>/',views.profile_edit),
    path('logout', views.logout),
    path('forgot_verifiy/',views.forgot_verifiy),
    path('check_username/', views.check_username, name='check_username'),
    path('pass_change/<id>/', views.pass_change),
    path('dashboard/',views.dashboard),
    path('admin_login/',views.admin_login),
    path('off_delete/<id>/',views.off_delete),
    path('add_category/',views.add_category), 
    path('del_category/<id>/',views.del_category),  
    path('add_recipe/',views.add_recipe),
    path('our_products/',views.our_products),
    path('product_edit/<id>/',views.product_edit),
    path('delete_recipe/<id>/', views.delete_recipe),
    path('add_our_banner/',views.add_our_banner),
    path('delete_photo/<id>/',views.delete_photo),
    path('user/',views.user),  
    path('recipe/',views.recipe),
    path('list_recipe/<category>/', views.list_recipe),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/',views.cart),
    path('order_success/',views.order_success),
    path('order/',views.order),
    path('admin_order/',views.admin_order),
    path('view_order/<id>/',views.view_order),
    path('history_view_order/<id>/',views.history_view_order),
    path('admin_history/',views.admin_history), 
    path('remove_cart/<id>/',views.remove_cart), 
    path('review/',views.user_review),  
    path('success_rev/',views.success_rev),  
    path('remove_reviews/<id>/',views.remove_reviews), 
    path('compaint/',views.compaint),  
    path('success_comment/',views.success_comment),  
    path('remove_compaint/<id>/',views.remove_compaint),  
    path('admin_review/',views.admin_review), 
    path('admin_remove_reviews/<id>/',views.admin_remove_reviews), 
    path('admin_remove_compaint/<id>/',views.admin_remove_compaint),  
    path('user_history', views.user_history),
    path('booking/',views.booking),
    path('celebration/',views.celebration),
    path('print/<id>/',views.print)
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



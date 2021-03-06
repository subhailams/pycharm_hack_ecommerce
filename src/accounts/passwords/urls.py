from django.conf.urls import url
from django.contrib.auth import views as auth_views


urlpatterns  = [
        url(r'^password/change/$', 
                auth_views.PasswordChangeView.as_view(), 
                name='password_change'),
        url(r'^password/change/done/$',
                auth_views.PasswordChangeDoneView.as_view(), 
                name='password_change_done'),
        # url(r'^password-reset/$', views.PasswordResetView.as_view(),
        # name='password-reset'),
        url(r'^password/reset/$', 
                auth_views.PasswordResetView.as_view(template_name = "registeration/password_reset_form.html", email_template_name = 'registeration/password_reset_email.html'), 
                name='password_reset'),
        url(r'^password/reset/done/$', 
                auth_views.PasswordResetDoneView.as_view(template_name = "registeration/password_reset_done.html"), 
                name='password_reset_done'),
        url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
                auth_views.PasswordResetConfirmView.as_view(template_name = "registeration/password_reset_confirm.html"), 
                name='password_reset_confirm'),
        url(r'^password/reset/complete/$', 
                auth_views.PasswordResetCompleteView.as_view(template_name = "registeration/password_reset_complete.html"), 
                name='password_reset_complete'),
]

    #         auth_views.PasswordChangeDoneView.as_view(), 
    #         name='password_change_done'),
    # url(r'^password/reset/$', 
    #         auth_views.PasswordResetView.as_view(template_name = "registeration/password_reset_form.html"), 
    #         name='password_reset'),
    # url(r'^password/reset/done/$', 
    #         auth_views.PasswordResetDoneView.as_view(template_name = "registeration/password_reset_done.html"), 
    #         name='password_reset_done'),
    # url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
    #         auth_views.PasswordResetConfirmView.as_view(template_name = "registeration/password_reset_confirm.html"), 
    #         name='password_reset_confirm'),
    # url(r'^password/reset/complete/$', 
    #         auth_views.PasswordResetCompleteView.as_view(template_name = "registeration/password_reset_complete.html"), 
    #         name='password_reset_complete'),
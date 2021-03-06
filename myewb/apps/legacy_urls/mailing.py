from django.conf.urls.defaults import *

urlpatterns = patterns('siteutils.shortcuts',
    url(r'^AvailableLists', 'redirect_to_reverse', {'url': 'communities_index',
                                    'permanent': True}),
    url(r'^EditList/(?P<group_id>\d+)', 'redirect_to', {'url': '/groups/id/%(group_id)s/',
                                    'permanent': True}),
    url(r'^ListInfo/(?P<group_id>\d+)', 'redirect_to', {'url': '/groups/id/%(group_id)s/',
                                    'permanent': True}),
    url(r'^ListMember', 'redirect_to_reverse', {'url': 'profiles_index',
                                    'permanent': True}),
    url(r'^ListMgmt/(?P<group_id>\d+)', 'redirect_to', {'url': '/groups/id/%(group_id)s/',
                                    'permanent': True}),
    url(r'^Mailing', 'redirect_to_reverse', {'url': 'communities_index',
                                    'permanent': True}),
    url(r'^MyLists', 'redirect_to_reverse', {'url': 'communities_index',
                                    'permanent': True}),
    url(r'^NewList', 'redirect_to_reverse', {'url': 'new_community',
                                    'permanent': True}),
    url(r'^SendEmail(?P<group_id>\d+)', 'redirect_to', {'url': '/groups/id/%(group_id)s/',
                                    'permanent': True}),
    url(r'^Unsubscription', 'redirect_to_reverse', {'url': 'network_unsubscribe',
                                    'permanent': True}),
    url(r'^MainListSignup', 'redirect_to_reverse', {'url': 'home',
                                    'permanent': True}),
    url(r'^MassDelete', 'redirect_to_reverse', {'url': 'mass_delete',
                                    'permanent': True}),
    url(r'^MailableLists', 'redirect_to_reverse', {'url': 'communities_index',
                                    'permanent': True}),
    url(r'^Projects', 'redirect_to_reverse', {'url': 'communities_index',
                                    'permanent': True}),
                            
    )
from django.conf.urls.defaults import *
from mpod.views import *
from django.contrib import admin

admin.autodiscover()

import sys
import os


visible_patterns = patterns('',
    (r'^admin/(.*)', include(admin.site.urls)),
    ('^$', index),
    (r'^index/$', index),
    (r'^references/$', references),
    (r'^credits/$', credits),
    (r'^contact/$', contact),
    (r'^disclaimer/$', disclaimer),
    (r'^contact/thanks/$', contact_success),
    (r'^data/$', 'mpod.data.views.data_intro'),
    (r'^data/intro$', 'mpod.data.views.data_intro'),    
    (r'^data/search/$', 'mpod.data.views.data_search'),
    (r'^data/properties/$', 'mpod.data.views.data_properties'),
    (r'^data/doc$', 'mpod.data.views.data_doc'),
#   (r'^data/references/$', 'mpod.data.views.data_references'),
    (r'^data/references/$', 'mpod.data.views.publi_search'),
    (r'^data/submit/$', 'mpod.data.views.submit_file'),
    (r'^dict$', 'mpod.data.views.dict_intro'),
    (r'^dict/intro$', 'mpod.data.views.dict_intro'),
    (r'^dict/doc$', 'mpod.data.views.dict_doc'),

    # Example:
    # (r'^dj_txrf/', include('dj_txrf.foo.urls')),

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)

invisible_patterns = patterns('',
    (r'^images/(.+[.].+)$',get_image),
    (r'^css/(.+[.]css)$',load_css),
    (r'^datafiles/(.+[.]mpod)$',get_datafile),
    (r'^dictionary/get$',get_dictionary),
    (r'^articles/(\d+)/$','mpod.data.views.view_article'),
    (r'^properties/(\d+)/$','mpod.data.views.view_property'),
    (r'^exparcond/(\d+)/$','mpod.data.views.view_exparcond'),
    (r'^dataitem/(\d+)/$','mpod.data.views.view_data_item'),
    (r'^datafiles/upload/success/$','mpod.data.views.upload_success'),
    (r'^datafiles/upload/submit/$','mpod.data.views.submit_file'),
    # Example:
    # (r'^dj_txrf/', include('dj_txrf.foo.urls')),

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)

urlpatterns = invisible_patterns + visible_patterns

urlpatterns += patterns('',
    url(r'^captcha/', include('captcha.urls')),
)

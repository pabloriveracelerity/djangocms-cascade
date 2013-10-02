from django.forms import widgets
from django.forms.models import modelform_factory
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext_lazy as _
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from cmsplugin_bootstrap.models import BootstrapElement
from cmsplugin_bootstrap.change_form_widgets import ExtraStylesWidget, SingleOptionWidget


class BootstrapPluginBase(CMSPluginBase):
    module = 'Bootstrap'
    model = BootstrapElement
    change_form_template = "cms/plugins/bootstrap/change_form.html"
    render_template = "cms/plugins/bootstrap/generic.html"
    allow_children = True

    def __init__(self, *args, **kwargs):
        super(BootstrapPluginBase, self).__init__(*args, **kwargs)
        change_form_widgets = SortedDict()
        if hasattr(self, 'css_classes') and len(self.css_classes) > 1:
            change_form_widgets['class_name'] = widgets.Select(choices=self.css_classes)
        if hasattr(self, 'extra_classes_widget'):
            change_form_widgets['extra_classes'] = self.extra_classes_widget
        change_form_widgets['extra_styles'] = ExtraStylesWidget()
        self.form = modelform_factory(BootstrapElement, fields=change_form_widgets.keys(), widgets=change_form_widgets)

    def save_model(self, request, obj, form, change):
        obj.tag_type = self.tag_type
        if hasattr(self, 'css_classes') and len(self.css_classes) == 1:
            obj.class_name = self.css_classes[0][0]
        return super(BootstrapPluginBase, self).save_model(request, obj, form, change)


class ButtonWrapperPlugin(BootstrapPluginBase):
    name = _("Button wrapper")
    render_template = "cms/plugins/bootstrap/naked.html"
    child_classes = ['LinkPlugin']
    tag_type = 'naked'
    css_classes = (('btn', 'btn'),)
    extra_classes_widget = SingleOptionWidget(prefix='buttontype',
        choices=(('', 'unstyled'),) + tuple(2 * ('btn-%s' % b,)
            for b in ('primary', 'info', 'success', 'warning', 'danger', 'inverse', 'link')))

plugin_pool.register_plugin(ButtonWrapperPlugin)


class BootstrapRowPlugin(BootstrapPluginBase):
    name = _("Row container")
    child_classes = ['BootstrapColumnPlugin']
    tag_type = 'div'
    css_classes = (('row', 'row'),)

plugin_pool.register_plugin(BootstrapRowPlugin)


class BootstrapColumnPlugin(BootstrapPluginBase):
    name = _("Column container")
    parent_classes = ['BootstrapRowPlugin']
    require_parent = True
    tag_type = 'div'
    css_classes = tuple(2 * ('span%s' % i,) for i in range(1, 13))
    extra_classes_widget = SingleOptionWidget(prefix='offset',
        choices=(('', 'no offset'),) + tuple(2 * ('offset%s' % o,) for o in range(1, 12)))

plugin_pool.register_plugin(BootstrapColumnPlugin)


class BootstrapThumbnailsPlugin(BootstrapPluginBase):
    name = _("Thumbnails")
    child_classes = ['BootstrapThumbImagePlugin']
    tag_type = 'ul'
    css_classes = (('thumbnails', 'thumbnails'),)

plugin_pool.register_plugin(BootstrapThumbnailsPlugin)


class BootstrapThumbImagePlugin(BootstrapPluginBase):
    name = _("Single thumbnail")
    parent_classes = ['BootstrapThumbnailsPlugin']
    require_parent = True
    tag_type = 'li'
    css_classes = (('thumbnail', 'thumbnail'),)

plugin_pool.register_plugin(BootstrapThumbImagePlugin)
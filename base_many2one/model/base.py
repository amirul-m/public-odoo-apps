from lxml import etree
from odoo import fields, models, api


class Base(models.AbstractModel):
    _inherit = "base"

    _no_create_no_open_active = True

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        ret_val = super(Base, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)
        if view_type == 'form' and self._no_create_no_open_active and \
                eval(self.env['ir.config_parameter'].sudo().get_param(
                    'many2one.no_create_no_open', 'False')):
            doc = etree.XML(ret_val['arch'])
            m2o_fields = [k for k, v in ret_val.get('fields').items() if v.get('type') == 'many2one']
            for field in m2o_fields:
                for node in doc.xpath("//field[@name='%s']" % field):
                    options_value = eval(node.attrib.get('options', 'False'))
                    item_insert = {'no_open': True, 'no_create': True}
                    if options_value:
                        item_insert_inversed = dict(
                            filter(lambda item: item[0] not in item_insert.keys(), options_value.items()))
                        if item_insert_inversed:
                            item_insert.update(item_insert_inversed)
                    node.set("options", str(item_insert))

            o2m_fields = [k for k, v in ret_val.get('fields').items() if v.get('type') == 'one2many']
            for field in o2m_fields:
                for view_o2m in ret_val.get('fields').get(field).get('views').values():
                    o2m_doc = etree.XML(view_o2m.get('arch'))
                    m2o_fields = [k for k, v in view_o2m.get('fields').items() if v.get('type') == 'many2one']
                    for field_in_o2m in m2o_fields:
                        for node in o2m_doc.xpath("//field[@name='%s']" % field_in_o2m):
                            options_value = eval(node.attrib.get('options', 'False'))
                            item_insert = {'no_open': True, 'no_create': True}
                            if options_value:
                                item_insert_inverted = dict(
                                    filter(lambda item: item[0] not in item_insert.keys(), options_value.items()))
                                if item_insert_inverted:
                                    item_insert.update(item_insert_inverted)
                            node.set("options", str(item_insert))
                    view_o2m['arch'] = etree.tostring(o2m_doc, encoding='unicode')
            ret_val['arch'] = etree.tostring(doc, encoding='unicode')
        return ret_val

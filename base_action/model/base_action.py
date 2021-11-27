from lxml import etree
from odoo import fields, models


class BaseAction(models.AbstractModel):
    _name = "base.action"
    _description = "Base Action"

    _button_xpath = "/form/header/field[@name='state']"
    _show_button_confirm = True
    _show_button_cancel = True
    _show_button_draft = True

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_draft(self):
        self.write({'state': 'draft'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def fields_view_get(self, view_id=None, view_type="form", toolbar=False, submenu=False):
        res = super(BaseAction, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                      submenu=submenu)
        if view_type == "form" and \
                (self._show_button_confirm or self._show_button_cancel or self._show_button_draft):
            doc = etree.XML(res["arch"])
            if self._show_button_confirm:
                for node in doc.xpath(self._button_xpath):
                    str_element = self.env["ir.qweb"]._render(
                        "base_action.button_confirm_template"
                    )
                    new_node = etree.fromstring(str_element)
                    for new_element in new_node:
                        # add new button before the first button (if exist)
                        node.addprevious(new_element)

            if self._show_button_draft:
                for node in doc.xpath(self._button_xpath):
                    str_element = self.env["ir.qweb"]._render(
                        "base_action.button_draft_template"
                    )
                    new_node = etree.fromstring(str_element)
                    for new_element in new_node:
                        # add new button before the first button (if exist)
                        node.addprevious(new_element)

            if self._show_button_cancel:
                for node in doc.xpath(self._button_xpath):
                    str_element = self.env["ir.qweb"]._render(
                        "base_action.button_cancel_template"
                    )
                    new_node = etree.fromstring(str_element)
                    for new_element in new_node:
                        # add new button before the first button (if exist)
                        node.addprevious(new_element)

            View = self.env["ir.ui.view"]
            if view_id and res.get("base_model", self._name) != self._name:
                View = View.with_context(base_model_name=res["base_model"])
            new_arch, new_fields = View.postprocess_and_fields(doc, self._name)
            res["arch"] = new_arch
        return res

from lxml import etree
from odoo import fields, models


class BaseSetToDraft(models.AbstractModel):
    _name = "base.set.to.draft"
    _description = "Set To Draft"

    _button_xpath = "/form/header/button[1]"
    _button_draft_exist = False

    def set_to_draft(self):
        self.write({'state': 'draft'})

    def fields_view_get(self, view_id=None, view_type="form", toolbar=False, submenu=False):
        res = super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_type == "form" and not self._button_draft_exist and res['fields'].get('state'):
            doc = etree.XML(res["arch"])
            for node in doc.xpath(self._button_xpath):
                str_element = self.env["ir.qweb"]._render(
                    "base_set_to_draft.set_to_draft_template"
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

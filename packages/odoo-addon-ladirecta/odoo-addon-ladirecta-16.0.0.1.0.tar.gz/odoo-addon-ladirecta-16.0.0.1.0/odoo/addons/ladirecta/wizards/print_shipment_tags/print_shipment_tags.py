from odoo import fields, models


class PrintShipmentTagsWizard(models.TransientModel):
    """
    A transient model for the creation of the tags for
    the shipments. The user can only define the Correos
    Shipment Code to select a subgroup of tags to print.
    """

    _name = "print.shipment.tags.wizard"
    _description = "Print Shipment Tags"

    correos_shipment_code_id = fields.Many2one(
        "correos.shipment.code",
        string="Correos Shipment Code",
        required=True,
    )

    def print_shipment_tags(self):
        self.ensure_one()
        partners = (
            self.env["res.partner"]
            .sudo()
            .search([("correos_code_id", "=", self.correos_shipment_code_id.id)])
            .filtered(lambda partner: partner.has_active_printable_contracts())
        )
        return self.env.ref("ladirecta.report_shipment_tag").report_action(partners)

from odoo import fields, models


class Partner(models.Model):

    _inherit = "res.partner"

    correos_code_id = fields.Many2one(
        "correos.shipment.code",
        string="Correos Shipment Code",
    )

    def get_correos_image(self):
        self.ensure_one()
        return self.env.company.correos_image

    def has_active_printable_contracts(self):
        self.ensure_one()
        today = fields.Date.context_today(self)

        active_contracts = self.env["contract.contract"].search(
            [
                ("partner_id", "=", self.id),
                ("contract_line_ids", "!=", False),  # Debe tener líneas de contrato
                (
                    "contract_line_ids.product_id.to_be_printed",
                    "=",
                    True,
                ),  # Debe tener productos que se impriman
                ("contract_line_ids.date_start", "<=", today),
                "|",  # Condiciones OR
                ("contract_line_ids.date_end", ">=", today),
                ("contract_line_ids.date_end", "=", False),
            ]
        )

        return bool(active_contracts)

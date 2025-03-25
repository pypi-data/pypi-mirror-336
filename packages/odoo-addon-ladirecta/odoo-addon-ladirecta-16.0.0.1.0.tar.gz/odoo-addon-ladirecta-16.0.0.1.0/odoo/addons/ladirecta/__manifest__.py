{
    "version": "16.0.0.1.0",
    "name": "La Directa",
    "summary": """
    """,
    "depends": [
        "contacts",
    ],
    "author": """
        Coopdevs Treball SCCL,
    """,
    "category": "Shipments management",
    "website": "https://git.coopdevs.org/talaios/addons/odoo-directa#",
    "license": "AGPL-3",
    "data": [
        "views/correos_shipment_code.xml",
        "views/res_partner.xml",
        "views/product_template.xml",
        "views/res_company.xml",
        "wizards/print_shipment_tags/print_shipment_tags.xml",
        "reports/shipment_tag.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [],
    "application": False,
    "installable": True,
}

from odoo import models, fields
from odoo.exceptions import UserError

def _delivery_type_ondelete_custom_table(recs):
    # Cuando se desinstala el módulo, reasigna delivery_type a un valor válido
    recs.filtered(lambda r: r.delivery_type == 'custom_table').write({'delivery_type': 'fixed'})

class DeliveryRateTable(models.Model):
    _name = 'delivery.rate.table'
    _description = 'Tarifas de envío personalizadas'

    zip_code = fields.Char(string='Código Postal', required=True)
    zone = fields.Char(string='Zona')
    max_weight = fields.Float(string='Peso Máximo (kg)', required=True)
    price = fields.Float(string='Precio', required=True)
    is_amba = fields.Boolean(string='Es AMBA')

class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    delivery_type = fields.Selection(
        selection_add=[('custom_table', 'Tarifas Personalizadas')],
        ondelete={'custom_table': _delivery_type_ondelete_custom_table}
    )

    def rate_shipment(self, order):
        self.ensure_one()
        if self.delivery_type != 'custom_table':
            return super().rate_shipment(order)

        weight = sum(line.product_id.weight * line.product_uom_qty for line in order.order_line)
        zip_code = order.partner_shipping_id.zip or ''
        is_amba = self._is_amba(zip_code)

        tarifa = self.env['delivery.rate.table'].search([
            ('zip_code', '=', zip_code),
            ('max_weight', '>=', weight),
            ('is_amba', '=', is_amba)
        ], order='max_weight ASC', limit=1)

        if not tarifa:
            raise UserError("No se encontró una tarifa para el destino y peso especificado.")

        return {
            'success': True,
            'price': tarifa.price,
            'error_message': False,
            'warning_message': False
        }

    def _is_amba(self, zip_code):
        return zip_code.startswith('C1')  # Ajustá esto según tus criterios para zona AMBA

/** @odoo-module **/
import { patch } from '@web/core/utils/patch';
import * as saleUtils from '@sale/js/sale_utils';

patch(saleUtils, {
    serializeComboItem(comboItem) {
        // Llamamos al método original para conservar el resto de la serialización
        const result = super.serializeComboItem(comboItem);
        // Añadimos la propiedad quantity definida en cada comboItem
        result.quantity = comboItem.quantity;
        result.price = comboItem.price
        return result;
    },
});
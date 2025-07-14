/** @odoo-module **/
import { patch } from '@web/core/utils/patch';
import { ProductComboItem } from '@sale/js/models/product_combo_item';

patch(ProductComboItem.prototype, {
    deepCopy() {
        const copy = super.deepCopy()
        copy.price = this.price
        return copy;
    },
});

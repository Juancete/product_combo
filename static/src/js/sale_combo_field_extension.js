/** @odoo-module **/
console.log('⚡ patch_product_combo.js cargado ⚡');
import * as comboModel from '@sale/js/models/product_combo';

const OriginalProductCombo = comboModel.ProductCombo;

class PatchedProductCombo extends OriginalProductCombo {
    constructor(data) {
        super(data);
        // Aquí ya podrás ver tu log y asignar quantity:
        console.log('🔥 quantity desde JS:', data.quantity);
        this.quantity = data.quantity || 1;
    }
}

comboModel.ProductCombo = PatchedProductCombo;
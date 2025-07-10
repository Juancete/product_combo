/** @odoo-module **/
import { patch } from '@web/core/utils/patch';
import {
    ComboConfiguratorDialog
} from '@sale/js/combo_configurator_dialog/combo_configurator_dialog';

class ComboQuantity {

  constructor(comboId,quantity){
    this.id = comboId;
    this.quantity = quantity;
  }
}

patch(ComboConfiguratorDialog.prototype,{

  setup() {
    super.setup(...arguments);
  },

  /**
   * Sets the quantity of this combo product.
   * @param {Number} comboId id del combo.
   * @param {Number} quantity The new quantity of this combo product.
   */
  async getQuantity(comboId) {
      // Use up-to-date selected PTAVs and custom values to populate the product configurator.
      return this.props.itemsQuantity.find(combo => combo.id === comboId).quantity
      
  },

  /**
   * Sets the quantity of this combo product.
   * @param {Number} comboId id del combo.
   * @param {Number} quantity The new quantity of this combo product.
   */
  async setQuantity(comboId, quantity) {
      // Use up-to-date selected PTAVs and custom values to populate the product configurator.
      console.log("update " + comboId + " cantidad:" + quantity)
      this.props.combos.find(combo => combo.id === comboId).quantity = quantity
      
  }
});
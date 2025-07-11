/** @odoo-module **/
import { patch } from '@web/core/utils/patch';
import {
    ComboConfiguratorDialog
} from '@sale/js/combo_configurator_dialog/combo_configurator_dialog';
import { useState } from '@odoo/owl';

class ComboQuantity {
  constructor(comboId,quantity){
    this.id = comboId;
    this.quantity = quantity;
  }
}

patch(ComboConfiguratorDialog.prototype,{

  setup() {
    super.setup(...arguments);
    this.comboQuantity = useState([]);
    this.props.combos.forEach(element => {
      this.comboQuantity.push(new ComboQuantity(element.id, element.quantity))  
    });
    
  },
  /**
   * Sets the quantity of this combo product.
   * @param {Number} comboId id del combo.
   * @param {Number} quantity The new quantity of this combo product.
   */
  async setQuantity(comboId, quantity) {
      this.comboQuantity.find(comboQuantity=> comboQuantity.id === comboId).quantity = quantity; 
      
  },

  /**
   * Return the selected combo items, in the same order as the combos given as props.
   *
   * @return {ProductComboItem[]} The sorted selected combo items.
   */
  get _selectedComboItems() {
      this.state.selectedComboItems.forEach((item, comboId) => item.quantity = this.comboQuantity.find(comboQuantity=> comboQuantity.id === comboId).quantity )
      return super._selectedComboItems
  }

});
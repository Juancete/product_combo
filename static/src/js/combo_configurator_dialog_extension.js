/** @odoo-module **/
import { patch } from '@web/core/utils/patch';
import {
    ComboConfiguratorDialog
} from '@sale/js/combo_configurator_dialog/combo_configurator_dialog';


patch(ComboConfiguratorDialog.prototype, 'product_combo/ComboConfiguratorDialogExtension', {
  setup() {
    this._super(...arguments);
    for (const combo of this.props.combos) {
      const item = this.state.selectedComboItems.get(combo.id) || combo.selectedComboItem;
      item.quantity = item.quantity || 1;
      this.state.selectedComboItems.set(combo.id, item);
    }
  },
  _onSetComboItemQuantity(comboId, quantity) {
    const item = this.state.selectedComboItems.get(comboId);
    if (quantity > 0) {
      item.quantity = quantity;
      this.state.selectedComboItems.set(comboId, item);
    }
  },
  async confirm(options) {
    const combosConCantidad = this._selectedComboItems.map(item => ({
      ...item,
      quantity: item.quantity,
    }));
    await this.props.save(
      { ...this._comboProductData, combos: combosConCantidad },
      combosConCantidad,
      options
    );
    this.props.close();
  },
});
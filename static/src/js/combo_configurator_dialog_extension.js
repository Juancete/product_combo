/** @odoo-module **/
import { patch } from '@web/core/utils/patch';
import {
    ComboConfiguratorDialog
} from '@sale/js/combo_configurator_dialog/combo_configurator_dialog';


patch(ComboConfiguratorDialog.prototype,{
  setup() {
    super.setup(...arguments);
    console.log('Parche setup OK', this.props.combos);
    // Inicializa quantity sólo en los items que realmente existen
    // this.props.combos.forEach(combo => {
    //     // si ya viene (por algún otro patch) lo respeta, sino lo inicializa a 1
    //     combo.quantity = combo.quantity || 1;
    // });
  },
  /**
   * Al confirmar el diálogo, aquí recibes un array de líneas a añadir.
   * Reemplaza `line.quantity` por `line.quantity * combo.quantity`.
   */
  confirm() {
      const lines = super.confirm(...arguments);
      // props.combos y this.combos están alineados por índice
      return lines.map((line, index) => {
          const combo = this.combos[index];
          return {
              ...line,
              quantity: line.quantity * combo.quantity,
          };
      });
  },
});
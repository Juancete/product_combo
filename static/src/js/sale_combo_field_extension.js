/** @odoo-module **/
import { patch } from '@web/core/utils/patch';
import { SaleOrderLineProductField } from '@sale/js/sale_product_field';
import {  getLinkedSaleOrderLines, serializeComboItem } from '@sale/js/sale_utils';
import { uuid } from "@web/views/utils";
import { rpc } from "@web/core/network/rpc";
import { serializeDateTime } from "@web/core/l10n/dates";
import { ProductCombo} from '@sale/js/models/product_combo';
import {
    ComboConfiguratorDialog
} from '@sale/js/combo_configurator_dialog/combo_configurator_dialog';

patch(SaleOrderLineProductField.prototype, {
  async _openComboConfigurator(edit=false) {
        const saleOrder = this.props.record.model.root.data;
        const comboLineRecord = this.props.record;
        const comboItemLineRecords = getLinkedSaleOrderLines(comboLineRecord);
        const selectedComboItems = await Promise.all(comboItemLineRecords.map(async record => ({
            id: record.data.combo_item_id[0],
            no_variant_ptav_ids: edit ? this._getNoVariantPtavIds(record.data) : [],
            custom_ptavs: edit ? await this._getCustomPtavs(record.data) : [],
        })));
        const { combos, ...remainingData } = await rpc('/sale/combo_configurator/get_data', {
            product_tmpl_id: comboLineRecord.data.product_template_id[0],
            currency_id: comboLineRecord.data.currency_id[0],
            quantity: comboLineRecord.data.product_uom_qty,
            date: serializeDateTime(saleOrder.date_order),
            company_id: saleOrder.company_id[0],
            pricelist_id: saleOrder.pricelist_id[0],
            selected_combo_items: selectedComboItems,
            ...this._getAdditionalRpcParams(),
        });
        this.dialog.add(ComboConfiguratorDialog, {
            combos: combos.map(combo => {
                const newCombo = new ProductCombo(combo)
                newCombo.quantity = combo.quantity
                return newCombo
            }),
            ...remainingData,
            company_id: saleOrder.company_id[0],
            pricelist_id: saleOrder.pricelist_id[0],
            date: serializeDateTime(saleOrder.date_order),
            edit: edit,
            save: async (comboProductData, selectedComboItems) => {
                saleOrder.order_line.leaveEditMode();
                const comboLineValues = {
                    product_uom_qty: comboProductData.quantity,
                    selected_combo_items: JSON.stringify(
                        selectedComboItems.map(serializeComboItem)
                    ),
                };
                if (!edit) {
                    comboLineValues.virtual_id = uuid();
                }
                await comboLineRecord.update(comboLineValues);
                // Ensure that the order lines are sorted according to their sequence.
                await saleOrder.order_line._sort();
            },
            discard: () => saleOrder.order_line.delete(comboLineRecord),
            ...this._getAdditionalDialogProps(),
        });
    },
});
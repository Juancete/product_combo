/** @odoo-module **/

import { ComboConfiguratorDialog } from '@sale/js/combo_configurator_dialog/combo_configurator_dialog';
import { patch } from "@web/core/utils/patch";
import { useState } from "@odoo/owl";

patch(ComboConfiguratorDialog.prototype, {
    /**
     * @override
     * Inicializa el estado del componente.
     */
    setup() {
        this._super();
        // Inicializa un estado para almacenar las cantidades seleccionadas por cada comboItem.
        // Usamos un Map para una gestión más fácil por ID.
        this.state.itemQuantities = useState(new Map());

        // Asegúrate de que las cantidades iniciales de los combos ya seleccionados se carguen.
        // Esto es útil si el diálogo se abre con valores pre-seleccionados.
        for (const [comboId, selectedItem] of this.state.selectedComboItems.entries()) {
            this.state.itemQuantities.set(selectedItem.id, selectedItem.quantity || 1);
        }
    },

    /**
     * @override
     * Este método se llama cuando se selecciona un item de combo.
     * Aquí inicializamos o actualizamos la cantidad para el item seleccionado.
     * @param {number} comboId - ID del combo principal.
     * @param {Object} comboItem - El objeto del item de combo seleccionado.
     */
    selectComboItem(comboId, comboItem) {
        this._super(comboId, comboItem); // Llama al método original para manejar la selección

        // Cuando se selecciona un item, asegúrate de que tenga una cantidad inicial de 1
        // si no tiene una ya definida.
        if (!this.state.itemQuantities.has(comboItem.id)) {
            this.state.itemQuantities.set(comboItem.id, comboItem.quantity || 1);
        }
    },

    /**
     * Nuevo método para actualizar la cantidad de un item de combo específico.
     * Se usará desde la plantilla QWeb cuando el usuario cambie la cantidad.
     * @param {number} comboItemId - El ID del item de combo cuya cantidad se va a actualizar.
     * @param {number} newQuantity - La nueva cantidad.
     */
    setItemQuantity(comboItemId, newQuantity) {
        // Asegurarse de que la cantidad sea al menos 1
        newQuantity = Math.max(1, newQuantity);
        this.state.itemQuantities.set(comboItemId, newQuantity);
        // Opcional: Podrías querer forzar una re-renderización o recalcular totales aquí
        // si el total del combo depende de las cantidades individuales.
    },

    /**
     * @override
     * Sobreescribe este método para incluir la cantidad seleccionada en el objeto que se devuelve.
     * Esto asegura que la plantilla QWeb pueda acceder a `item.quantity`.
     * @param {number} comboId - ID del combo.
     * @param {Object} comboItem - El item de combo original.
     * @returns {Object} El item de combo con la cantidad actual.
     */
    getSelectedOrProvidedComboItem(comboId, comboItem) {
        const item = this._super(comboId, comboItem); // Llama al método original
        // Añade la cantidad del estado al objeto del item de combo
        item.quantity = this.state.itemQuantities.get(item.id) || 1;
        return item;
    },

    /**
     * @override
     * Extiende el método confirm para incluir las cantidades por item
     * en los datos enviados al backend.
     */
    async confirm() {
        // Antes de llamar al confirm original, puedes modificar los datos
        // que se enviarán al servidor para incluir las cantidades por item.
        // La lógica exacta de cómo se envían estos datos dependerá de
        // cómo el backend del componente ComboConfiguratorDialog los espera.
        // Normalmente, la "confirm" en estos diálogos termina llamando a un RPC.

        // Por ejemplo, podrías actualizar `this.state.selectedComboItems`
        // o pasar un nuevo parámetro en el RPC.
        // Dado que getSelectedOrProvidedComboItem ya está añadiendo la cantidad
        // a los ítems seleccionados, el backend debería recibirla si consume ese objeto.

        // Si necesitas un formato específico para el backend, aquí es donde lo ajustarías.
        // Por ejemplo, si el RPC espera un array de { id: comboItemId, quantity: num }
        // const selectedData = Array.from(this.state.selectedComboItems.values()).map(item => ({
        //     id: item.id,
        //     quantity: this.state.itemQuantities.get(item.id) || 1,
        // }));
        // await this.env.services.rpc('/your/custom/route', { combos: selectedData });

        return this._super(); // Llama al método original de confirmación
    },
});
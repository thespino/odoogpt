/** @odoo-module **/

import { registerInstancePatchModel } from '@mail/model/model_core';
import { insert } from '@mail/model/model_field_command';

registerInstancePatchModel('mail.messaging_initializer', 'odogpt/static/src/messaging_initializer_ai.js', {
    /**
     * @override
     */
    _initCommands() {
        this._super();
        this.messaging.update({
            commands: insert({
                help: this.env._t("Ask something to the AI"),
                methodName: 'execute_command_ai',
                name: "ai",
            }),
        });
    },
});

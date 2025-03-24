<!-- Copyright 2022 Karlsruhe Institute of Technology
   -
   - Licensed under the Apache License, Version 2.0 (the "License");
   - you may not use this file except in compliance with the License.
   - You may obtain a copy of the License at
   -
   -     http://www.apache.org/licenses/LICENSE-2.0
   -
   - Unless required by applicable law or agreed to in writing, software
   - distributed under the License is distributed on an "AS IS" BASIS,
   - WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   - See the License for the specific language governing permissions and
   - limitations under the License. -->

<template>
  <div>
    <div v-for="message in messages" :key="message.id">
      <flash-message :message="message.message" :type="message.type"></flash-message>
    </div>
  </div>
</template>

<script>
import FlashMessage from 'scripts/components/lib/base/FlashMessage.vue';

export default {
  components: {
    FlashMessage,
  },
  data() {
    return {
      messages: [],
    };
  },
  methods: {
    addMessage(type, message, request = null) {
      let _message = message;

      if (request !== null) {
        // Do nothing if the error originates from a canceled request.
        if (request.status === 0) {
          return;
        }

        _message = `${message} (${request.status})`;
      }

      this.messages.push({id: kadi.utils.randomAlnum(), message: _message, type});
    },
    flashDanger(message, request = null) {
      this.addMessage('danger', message, request);
    },
    flashInfo(message, request = null) {
      this.addMessage('info', message, request);
    },
    flashSuccess(message, request = null) {
      this.addMessage('success', message, request);
    },
    flashWarning(message, request = null) {
      this.addMessage('warning', message, request);
    },
  },
};
</script>

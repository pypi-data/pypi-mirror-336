<!-- Copyright 2020 Karlsruhe Institute of Technology
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
  <div ref="alert" class="alert fade show" :class="`alert-${type}`">
    <i v-if="icon" class="fa" :class="`fa-${icon}`"></i> {{ message }}
  </div>
</template>

<script>
export default {
  props: {
    message: String,
    type: {
      type: String,
      default: 'info',
    },
  },
  data() {
    return {
      icon: null,
    };
  },
  mounted() {
    if (this.type === 'info') {
      this.icon = 'circle-info';
    } else if (this.type === 'danger') {
      this.icon = 'circle-xmark';
    } else if (this.type === 'warning') {
      this.icon = 'triangle-exclamation';
    } else if (this.type === 'success') {
      this.icon = 'circle-check';
    }

    const timeout = Math.min(Math.max(this.message.length * 75, 2500), 7000);
    window.setTimeout(() => $(this.$refs.alert).alert('close'), timeout);
  },
};
</script>

import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import vSelect from 'vue-select';
import LvButton from 'lightvue/button';
import LvCard from 'lightvue/card';
import LvDropdown from 'lightvue/dropdown';
import LvLoader from 'lightvue/loaders';
import LvBadge from 'lightvue/badge';

createApp(App)
    .component("v-select", vSelect)
    .component('LvButton', LvButton)
    .component('LvCard', LvCard)
    .component('LvDropdown', LvDropdown)
    .component('LvLoader', LvLoader)
    .component('LvBadge', LvBadge)
    .mount('#app')
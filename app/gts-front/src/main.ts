import { createApp } from 'vue';
import { createPinia } from 'pinia';
import './style.css';
import App from './App.vue';
import TransferHeader from './components/TransferHeader.vue';
import TransferModes from './components/TransferModes.vue';
import TransferContent from './components/TransferContent.vue';
import LvButton from 'lightvue/button';
import LvCard from 'lightvue/card';
import LvDialog from 'lightvue/dialog';
import LvDropdown from 'lightvue/dropdown';
import LvLoader from 'lightvue/loaders';
import LvBadge from 'lightvue/badge';
import LvProgressBar from 'lightvue/progress-bar';
import LvSlider from 'lightvue/slider';
import Tooltip from 'lightvue/tooltip';

createApp(App)
    .use(createPinia())
    .component('TransferHeader', TransferHeader)
    .component('TransferModes', TransferModes)
    .component('TransferContent', TransferContent)
    .component('LvButton', LvButton)
    .component('LvCard', LvCard)
    .component('LvDialog', LvDialog)
    .component('LvDropdown', LvDropdown)
    .component('LvLoader', LvLoader)
    .component('LvBadge', LvBadge)
    .component('LvProgressBar', LvProgressBar)
    .component('LvSlider', LvSlider)
    .directive('Tooltip', Tooltip)
    .mount('#app')

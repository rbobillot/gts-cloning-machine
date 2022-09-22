import { defineStore } from "pinia";

export const useFlatpassStore = defineStore("flatpassStore", {
    state: () => {
        return {
            fgtsStatus: { isRunning: false, status: "Not Running" }
        };
    },
    actions: {
        setFgtsStatus(status: any) { // update via socket.io ?
            this.fgtsStatus = status;
        },
    },
    getters: {
        getFgtsStatus(): any {
            return this.fgtsStatus.status;
        },
        isFgtsRunning(): boolean {
            return this.fgtsStatus.isRunning
        },
    }
});
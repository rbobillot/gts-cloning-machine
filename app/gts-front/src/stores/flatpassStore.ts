import { defineStore } from "pinia"

export const useFlatpassStore = defineStore("flatpassStore", {
    state: () => {
        return {
            baseFgtsStatus: { isRunning: false, status: "Not Running" },
            baseNdsStatus: { isConnected: false, status: "Not Connected" }
        };
    },
    actions: {
        setFgtsStatus(status: any) {
            this.baseFgtsStatus = status;
        },
        setNdsStatus(status: any) {
            this.baseNdsStatus = status;
        },
    },
    getters: {
        fgtsStatus(): any {
            return this.baseFgtsStatus;
        },
        ndsStatus(): any {
            return this.baseNdsStatus;
        },
        isFgtsRunnig(): boolean {
            return this.baseFgtsStatus.isRunning;
        },
        isNdsConnected(): boolean {
            return this.baseNdsStatus.isConnected;
        },
    }
});
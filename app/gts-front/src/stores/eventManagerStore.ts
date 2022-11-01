import { Manager, Socket } from "socket.io-client"
import { defineStore } from "pinia"
import { DefaultEventsMap } from "socket.io/dist/typed-events"

const manager = new Manager("http://localhost:8083")

export const useEventManagerStore = defineStore("eventManagerStore", {
    state: () => {
        return {
            frontSocket: manager.socket("/gts-front"),
            serviceSocket: manager.socket("/gts-service"),
        }
    },
    actions: {
        setFrontSocket(socket: Socket) {
            this.frontSocket = socket
        },
        setServiceSocket(socket: Socket) {
            this.serviceSocket = socket
        },
    },
    getters: {
        getFrontSocket(): any {
            return this.frontSocket
        },
        getServiceSocket(): any {
            return this.serviceSocket
        },
    }
});
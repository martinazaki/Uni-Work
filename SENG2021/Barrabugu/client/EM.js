class EM {
    static init() {
        this.events = {}
    }

    static emit(event, data) {
        if (!this.events[event]) {
            return;
        }

        for (let cb of this.events[event]) {
            cb(data)
        }
    }

    static on(event, cb) {
        assert(typeof cb === "function", `${cb} is not a function`)
        if (!this.events[event]) {
            this.events[event] = []
        }

        this.events[event].push(cb)
    }
}
class Filter {

    static init() {
        this.elements = {
            form: document.querySelector("#filter-form"),
            filter: document.querySelector("#filter"),
        }

        this.elements.form.addEventListener('submit', e => {
            e.preventDefault()
            EM.emit('filter-change', new FilterEngine(this.elements.filter.value))
        })

        document.body.addEventListener('keydown', e => {
            if (e.target === document.body && e.key === '/') {
                e.preventDefault()
                this.elements.filter.focus()
            }
        })
    }

}
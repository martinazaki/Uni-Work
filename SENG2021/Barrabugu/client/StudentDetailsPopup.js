class StudentDetailsPopup {

    static init() {

        this.elements = {
            window: document.querySelector("#student-details-popup"),
            name: document.querySelector("#sdp-name"),
            email: document.querySelector("#sdp-email"),
            description: document.querySelector("#sdp-description"),
            close: document.querySelector("#sdp-close"),
        }

        document.body.addEventListener('click', e => {
            if (
                !this.elements.window.classList.contains('display-none')
                && e.target.closest('#student-details-popup') === null
            ) {
                this.elements.window.classList.add('display-none')
            }
        }, true)

        window.addEventListener('scroll', e => {
            this.elements.window.classList.add('display-none')
        }, true)
        window.addEventListener('resize', e => {
            this.elements.window.classList.add('display-none')
        }, true)

        this.elements.close.addEventListener('click', e => {
            this.elements.window.classList.add('display-none')
        })

    }

    static show({ x, y, gridWidth, studentDetails }) {
        this.elements.name.textContent = studentDetails.name
        this.elements.email.textContent = studentDetails.email
        this.elements.description.textContent = studentDetails.description

        // if the element is display: none, getBoundingClientRect returns 0, 0, 0, 0
        this.elements.window.classList.remove('display-none')

        const rect = this.elements.window.getBoundingClientRect()

        if (x + rect.width > window.innerWidth) {
            x -= rect.width + gridWidth - 10
        } else {
            x -= 10
        }

        this.elements.window.style.left = x + 'px'
        this.elements.window.style.top = y + 'px'
    }

}
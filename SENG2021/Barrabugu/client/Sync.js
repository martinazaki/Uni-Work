class Sync {

    static init() {
        EM.on('student-moved', this.onStudentMoved.bind(this))
    }

    static async onStudentMoved({email, from, to, newIndex, oldIndex, onResponse}) {
        // null <=> teamless

        assert(from === null || typeof from === "string")
        assert(to === null || typeof to === "string")

        const res = await fetch('api/student-moved', {
            method: "POST",
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'student-email': email,
                'source': from,
                'destination': to,
                'new-index': newIndex,
                'old-index': oldIndex
            })
        })
        if (onResponse !== undefined) {
            const data = await res.json()
            if (res.status === 200 || data.type === "success") {
                const message = `status: ${res.status} type: ${data.type}`
                assert(res.status === 200, message)
                assert(data.type === "success", message)
            }
            onResponse(data)
        }
    }

}
document.addEventListener('DOMContentLoaded', e => {

    const loginSection = document.querySelector('#login')
    const loginForm = document.querySelector('#form-login')
    const loginEmail = document.querySelector('#login-email')
    const loginPassword = document.querySelector('#login-password')

    const registerSection = document.querySelector('#register')
    const registerForm = document.querySelector('#form-register')
    const registerEmail = document.querySelector('#register-email')
    const registerPassword = document.querySelector('#register-password')
    const registerPasswordConfirm = document.querySelector('#register-password-confirm')

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault()
        let response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: loginEmail.value,
                password: loginPassword.value,
            })
        })
        let body = await response.json()
        if (body.type !== "success") {
            alert(`Error: ${JSON.stringify(body, null, 2)}`)
            return
        }
        document.cookie = `token=${response.token}`
        location.href = body.redirect_to
    })

    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault()
        if (registerPassword.value !== registerPasswordConfirm.value) {
            alert("Password and confirmation don't match")
            return;
        }

        let response = await fetch('/api/auth/register', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                email: registerEmail.value,
                password: registerPassword.value
            })
        })

        let body = await response.json()
        if (body.type !== "success") {
            alert(`Error: ${JSON.stringify(body, null, 2)}`)
            return
        }

        document.cookie = `token=${response.token}`
        location.href = body.redirect_to

    })

    document.querySelector("#show-register").addEventListener("click", e => {
        e.preventDefault()
        loginSection.style.display = 'none'
        registerSection.style.display = 'block'
    })

    document.querySelector("#show-login").addEventListener("click", e => {
        e.preventDefault()
        loginSection.style.display = 'block'
        registerSection.style.display = 'none'
    })

})
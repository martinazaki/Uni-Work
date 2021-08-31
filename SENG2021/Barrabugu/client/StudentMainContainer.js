class StudentMainContainer {

    static init() {
        EM.on('students-organization-recieved', this.onStudentOrgRecieved.bind(this))

        this.elements = {
            teams: document.querySelector("#teams"),
            teamless: document.querySelector("#teamless"),
        }

        this.teamsDomElement = {
            // teamName => domElement
        }

        this.studentsDomElement = {
            // studentEmail => domElement
        }
    }

    static onStudentOrgRecieved(teamsOrg) {

        for (let teamName of Object.keys(teamsOrg.teams)) {
            const elem = this.createTeamElement(teamName,
                teamsOrg.teams[teamName].map(studentEmail =>
                    teamsOrg.details[studentEmail]))

            this.teamsDomElement[teamName] = elem
            this.elements.teams.appendChild(elem)
        }

        for (let studentEmail of Object.values(teamsOrg.teamless)) {
            const elem = this.createStudentElement(teamsOrg.details[studentEmail])

            this.studentsDomElement[studentEmail] = elem
            this.elements.teamless.appendChild(elem)
        }

        this.teamsOrg = teamsOrg
    }

    static createStudentElement(studentDetails) {
        const article = document.createElement('article')
        article.classList.add('student')

        const h4 = document.createElement('h4')
        h4.classList.add('student-name')
        h4.textContent = studentDetails.name
        article.appendChild(h4)

        const email = document.createElement('h5')
        email.classList.add('student-email', 'email-to-copy')
        email.textContent = studentDetails.email
        article.appendChild(email)

        const pDescription = document.createElement('p')
        pDescription.classList.add('student-description')
        pDescription.textContent = studentDetails.description
        article.appendChild(pDescription)

        return article
    }

    static createTeamElement(teamName, studentsDetails) {
        const div = document.createElement('div')
        div.classList.add('team')

        const h3 = document.createElement('h3')
        h3.classList.add('team-title')

        const span = document.createElement('span')
        span.classList.add('team-title-name')
        span.textContent = teamName
        h3.appendChild(span)

        const button = document.createElement('button')
        button.classList.add('team-title-apply')
        button.addEventListener('click', e => {
            alert('apply for team ' + teamName)
        })
        button.textContent = 'Apply'
        h3.appendChild(button)

        div.appendChild(h3)

        const students = document.createElement("div")
        students.classList.add('team-students')
        for (let studentDetails of studentsDetails) {
            students.appendChild(this.createStudentElement(studentDetails))
        }
        div.appendChild(students)

        return div
    }


}
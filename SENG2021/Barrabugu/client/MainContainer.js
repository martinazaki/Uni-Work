class MainContainer {

    static init() {
        EM.on('students-organization-recieved', this.onTeamsOrgRecieved.bind(this))
        EM.on('filter-change', this.onFilterChange.bind(this))
        this.teamsOrg = null;

        this.elements = {
            teams: document.querySelector("#teams"),
            teamless: document.querySelector("#teamless"),

            noResultTeams: document.querySelector(".teams-container .no-result"),
            noResultTeamless: document.querySelector(".teamless-container .no-result"),
        }

        this.elements.noResultTeamless.classList.add('display-none')
        this.elements.noResultTeams.classList.add('display-none')

        this.markers = {
            teams: new Mark(this.elements.teams),
            teamless: new Mark(this.elements.teamless),
        }

        this.teamsDomElement = {
            // teamName => domElement
        }
        this.studentsDomElement = {
            // student email => domElement
        }

        document.body.addEventListener('click', e => {
            if (!e.target.matches(".student span, .student span mark")) {
                return
            }
            const email = e.target.closest('.student').getAttribute('data-email')
            const rect = e.target.closest('ul').getBoundingClientRect()
            StudentDetailsPopup.show({
                x: rect.left + rect.width,
                y: rect.top + 10,
                gridWidth: rect.width,
                studentDetails: this.teamsOrg.details[email]
            })
        })
    }

    static onTeamsOrgRecieved(teamsOrg) {

        this.elements.teams.innerHTML = ''
        this.elements.teamless.innerHTML = ''

        this.studentsDomElement = {}
        this.teamsDomElement = {}

        const sortableOptions = {
            group: 'student',
            animation: 100,
            draggable: '.student',
            forceFallback: true,
            handle: '.drag-handle',
            onChoose: () => {
                document.body.classList.add("cursor-move")
            },
            onUnchoose: () => {
                document.body.classList.remove('cursor-move')
            },
            onEnd: this.onStudentDragEnd.bind(this)
        }

        Sortable.create(this.elements.teamless, sortableOptions)

        for (let studentEmail of Object.values(teamsOrg.teamless)) {
            const elem = this.createStudentElement(teamsOrg.details[studentEmail])
            assert(this.studentsDomElement[studentEmail] === undefined)
            this.studentsDomElement[studentEmail] = elem
            this.elements.teamless.appendChild(elem)
        }

        for (let teamName in (teamsOrg.teams)) {
            const article = document.createElement('article')
            article.classList.add("teams-team")

            const h3 = document.createElement("h4")
            h3.classList.add("teams-team-title")
            h3.textContent = teamName
            article.appendChild(h3)

            const ul = document.createElement('ul')
            ul.classList.add('teams-team-members')
            ul.setAttribute('data-team', teamName)

            Sortable.create(ul, sortableOptions)

            for (let studentEmail of teamsOrg.teams[teamName]) {
                const elem = this.createStudentElement(teamsOrg.details[studentEmail])
                assert(this.studentsDomElement[studentEmail] === undefined)
                this.studentsDomElement[studentEmail] = elem
                ul.appendChild(elem)
            }

            article.appendChild(ul)
            this.teamsDomElement[teamName] = article

            this.elements.teams.appendChild(article)
        }


        // everything is now ready, this becomes the source of truth
        this.teamsOrg = teamsOrg;
    }

    static onFilterChange(filterEngine) {
        assert(this.teamsOrg !== null)

        this.markers.teams.unmark()
        this.markers.teamless.unmark()

        if (filterEngine.words === null) {
            // no search terms, un-hide everything
            for (let studentEmail of Object.values(this.teamsOrg.teamless)) {
                this.studentsDomElement[studentEmail].classList.remove('display-none')
            }
            for (let teamName in this.teamsOrg.teams) {
                this.teamsDomElement[teamName].classList.remove('display-none')
            }

            this.elements.noResultTeamless.classList.add('display-none')
            this.elements.noResultTeams.classList.add('display-none')
            return
        }

        for (let word of filterEngine.words) {
            this.markers.teams.mark(word, {separateWordSearch: false})
            this.markers.teamless.mark(word, {separateWordSearch: false})
        }

        // match teams and teamless independently

        const matches = [/* [domelement, # matches] */]

        // teamless
        for (let studentEmail of this.teamsOrg.teamless) {
            const student = this.teamsOrg.details[studentEmail]

            let nMatches = filterEngine.matches(student.name)
                // + filterEngine.matches(student.email)
                // + filterEngine.matches(student.description)

            if (nMatches > 0) {
                this.studentsDomElement[student.email].classList.remove('display-none')
                matches.push([this.studentsDomElement[student.email], nMatches])
            } else {
                this.studentsDomElement[student.email].classList.add("display-none")
            }
        }

        matches
            .sort((a, b) => b[1] - a[1])
            .forEach(elem => this.elements.teamless.appendChild(elem[0]))

        if (matches.length > 0) {
            this.elements.noResultTeamless.classList.add('display-none')
        } else {
            this.elements.noResultTeamless.classList.remove('display-none')
        }

        matches.length = 0

        // teams. Search team name and student name
        for (let teamName of Object.keys(this.teamsOrg.teams)) {

            let nMatches = filterEngine.matches(teamName) * 4;

            for (let studentEmail of this.teamsOrg.teams[teamName]) {
                const student = this.teamsOrg.details[studentEmail]

                nMatches += filterEngine.matches(student.name)
                    // + filterEngine.matches(student.name)
                    // + filterEngine.matches(student.description)

            }

            if (nMatches > 0) {
                this.teamsDomElement[teamName].classList.remove('display-none')
                matches.push([this.teamsDomElement[teamName], nMatches])
            } else {
                this.teamsDomElement[teamName].classList.add("display-none")
            }
        }

        matches
            .sort((a, b) => b[1] - a[1])
            .forEach(elem => this.elements.teams.appendChild(elem[0]))

        if (matches.length > 0) {
            this.elements.noResultTeams.classList.add('display-none')
        } else {
            this.elements.noResultTeams.classList.remove('display-none')
        }

    }

    static createStudentElement(student) {
        const li = document.createElement('li')
        li.classList.add('student')
        li.setAttribute('data-email', student.email)

        const dragHandle = Svgs.dragHandle.cloneNode(/*deep=*/true)
        dragHandle.classList.add('drag-handle')
        li.appendChild(dragHandle)

        const span = document.createElement('span')
        span.textContent = student.name
        li.appendChild(span)

        return li
    }

    static onStudentDragEnd(e) {
        if (e.from === e.to && e.oldIndex === e.newIndex)
            return

        const studentEmail = e.item.getAttribute('data-email')
        const from = e.from.getAttribute('data-team') // null for teamless
        const to = e.to.getAttribute('data-team') // null for teamless

        // keep teamsOrg state in sync with the dom
        if (from === null) {
            this.teamsOrg.teamless.splice(e.oldIndex, 1)
            if (to === null) {
                // move from teamless to teamless
                this.teamsOrg.teamless.splice(e.newIndex, 0, studentEmail)
            } else {
                // move from teamless to team
                this.teamsOrg.teams[to].splice(e.newIndex, 0, studentEmail)
            }
        } else {
            this.teamsOrg.teams[from].splice(e.oldIndex, 1)
            if (to === null) {
                // move from team to teamless
                this.teamsOrg.teamless.splice(e.newIndex, 0, studentEmail)
            } else {
                // move from team to team
                this.teamsOrg.teams[to].splice(e.newIndex, 0, studentEmail)
            }
        }

        // Handle the "no result" sign in the teamless column
        // use the dom so that we don't have to recompute the filter. :^)
        // if we can NOT find a student that is visible
        if (this.elements.teamless.querySelector('.student:not(.display-none)') === null) {
            // show "no result"
            this.elements.noResultTeamless.classList.remove('display-none')
        } else {
            // hide "no result"
            this.elements.noResultTeamless.classList.add('display-none')
        }


        EM.emit('student-moved', {
            email: studentEmail,
            from: from,
            to: to,
            newIndex: e.newIndex,
            oldIndex: e.oldIndex,

            onResponse: (content) => {
                if (content.type !== "success") {
                    alert(`Error(${content.type}): ${content.text}`)
                    return
                }
                assert(content.type === "success", `${JSON.stringify(content)} invalid`)
            }
        })
    }

}
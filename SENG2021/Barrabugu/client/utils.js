function assert(condition, message="no error message") {
    if (!condition) {
        throw new Error(`[assertion error] ${message}`)
    }
}

class FilterEngine {
    constructor(filter) {
        filter = filter.toLowerCase()
        if (filter === '') {
            this.words = null;
        } else {
            this.splitAccordingToCommas(filter)
        }
    }

    matches(searchable) {
        // careful, words can overlap in matches
        if (this.words === null) return 0;

        searchable = searchable.toLowerCase()

        let matchesCount = 0

        for (let word of this.words) {

            assert(word != '')

            let previousIndex = -1, index
            while ((index = searchable.indexOf(word, previousIndex+1)) > -1) {
                matchesCount++
                previousIndex = index
            }
        }

        return matchesCount
    }

    splitAccordingToCommas(filter) {
        this.words = filter.split(/, ?/)
    }

    splitAccordingToQuotes(filter) {
        this.words = ['']
        let withinQuotes = false;
        for (let char of filter) {
            if (char === '"') {
                if (withinQuotes) {
                    withinQuotes = false;
                } else {
                    withinQuotes = true;
                    if (this.words[this.words.length-1] !== '') {
                        this.words.push('')
                    }
                }
            } else if (char === ' ') {
                if (withinQuotes) {
                    this.words[this.words.length-1] += char
                } else if (this.words[this.words.length-1] !== '') {
                    this.words.push('')
                }
            } else {
                this.words[this.words.length-1] += char
            }
        }
    }
}

// let eng;
// for (let eng of [
//     new FilterEngine('"hello world" foo bar'),
//     new FilterEngine('bar "hello world" foo'),
//     new FilterEngine('foo bar "hello world"')
// ]) {
//     assert(eng.matches("hello world") === 1)
//     assert(eng.matches("hello") === 0)
//     assert(eng.matches("hello world foo") === 2)
//     assert(eng.matches("foo bar") === 2)
//     assert(eng.matches("world bar") === 1)
// }


// assert(new FilterEngine('hello').matches('hello hello') === 2)
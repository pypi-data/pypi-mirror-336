class CustomError extends Error {
    constructor(message, cause) {
        super(`${message}: ${cause}`)
        this.name = 'CustomError'
    }
}

module.exports = CustomError

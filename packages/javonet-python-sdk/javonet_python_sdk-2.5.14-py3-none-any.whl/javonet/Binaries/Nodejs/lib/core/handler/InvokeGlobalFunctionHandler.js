const AbstractHandler = require('./AbstractHandler')

class InvokeGlobalFunctionHandler extends AbstractHandler {
    requiredParametersCount = 1

    constructor() {
        super()
    }

    process(command) {
        try {
            if (command.payload.length < this.requiredParametersCount) {
                throw new Error('Invoke Global Function parameters mismatch')
            }
            const { payload } = command
            const functionName = payload[0]
            const args = payload.slice(1)

            if (typeof global[functionName] === 'function') {
                return Reflect.apply(global[functionName], undefined, args)
            } else {
                let methods = Object.getOwnPropertyNames(global).filter(function(property) {
                    return typeof global[property] === 'function'
                })
                let message = `Method ${functionName} not found in global. Available methods:\n`
                methods.forEach((methodIter) => {
                    message += `${methodIter}\n`
                })
                throw new Error(message)
            }


        } catch (error) {
            throw this.process_stack_trace(error, this.constructor.name)
        }
    }
}

module.exports = new InvokeGlobalFunctionHandler()

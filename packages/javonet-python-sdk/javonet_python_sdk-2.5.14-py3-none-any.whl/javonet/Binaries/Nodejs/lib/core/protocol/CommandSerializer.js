
const Command = require('../../utils/Command');
const TypeSerializer = require('./TypeSerializer');
const RuntimeName = require('../../utils/RuntimeName');

class CommandSerializer {
    serialize(rootCommand, connectionData) {
        const buffers = [];
        // Write runtime name and a zero byte for runtime version.
        buffers.push(Uint8Array.of(rootCommand.runtimeName, 0));

        if (connectionData) {
            buffers.push(connectionData.serializeConnectionData());
        } else {

            buffers.push(Uint8Array.of(0, 0, 0, 0, 0, 0, 0));
        }

        buffers.push(Uint8Array.of(RuntimeName.Nodejs, rootCommand.commandType));

        this.serializeRecursively(rootCommand, buffers);

        return concatenateUint8Arrays(buffers);
    }

    serializeRecursively(command, buffers) {
        for (const item of command.payload) {
            if (item instanceof Command) {
                buffers.push(TypeSerializer.serializeCommand(item));
                this.serializeRecursively(item, buffers);
            } else {
                buffers.push(TypeSerializer.serializePrimitive(item));
            }
        }
    }
}

function concatenateUint8Arrays(arrays) {
    let totalLength = arrays.reduce((sum, arr) => sum + arr.length, 0);
    const result = new Uint8Array(totalLength);

    let offset = 0;
    for (const arr of arrays) {
        result.set(arr, offset);
        offset += arr.length;
    }
    return result;
}

module.exports = CommandSerializer;

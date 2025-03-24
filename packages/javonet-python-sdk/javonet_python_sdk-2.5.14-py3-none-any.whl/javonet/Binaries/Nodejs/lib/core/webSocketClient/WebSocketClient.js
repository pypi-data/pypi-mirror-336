const WebSocket = require('ws')

/**
 * Enum for WebSocket states.
 * @readonly
 * @enum {string}
 */
const WebSocketStateEnum = {
    OPEN: 'open',
    CLOSE: 'close',
    ERROR: 'error',
}

/**
 * WebSocketClient class that handles WebSocket connection, message sending, and automatic disconnection.
 */
class WebSocketClient {
    /**
     * @param {string} url
     * @param {object} options
     */
    constructor(url, options) {
        /**
         * @type {string}
         */
        this.url = url

        /**
         * @type {WebSocket | null}
         */
        this.instance = null

        /**
         * @type {boolean} isConnected indicates whether the WebSocket is connected.
         */
        this.isConnected = false

        /**
         * @type {boolean}
         */
        this.isDisconnectedAfterMessage = options?.isDisconnectedAfterMessage ?? true
    }

    /**
     * Connects to the WebSocket server.
     * @async
     * @returns {Promise<WebSocket>} - A promise that resolves when the connection is established.
     */
    connect() {
        return new Promise((resolve, reject) => {
            const client = new WebSocket(this.url)

            client.on(WebSocketStateEnum.OPEN, () => {
                this.instance = client;
                resolve(client);
            })

            // eslint-disable-next-line no-unused-vars
            client.on(WebSocketStateEnum.ERROR, (error) => {
                reject(error)
            })

            client.on(WebSocketStateEnum.CLOSE, () => {
                reject(new Error("Connection closed before receiving message"))
            })
        });
    }

    /**
     * Sends messageArray through websocket connection
     * @async
     * @param {Buffer|ArrayBuffer|Buffer[]} messageArray
     * @returns {Promise<Buffer|ArrayBuffer|Buffer[]>}
     */
    send(messageArray) {
        return new Promise((resolve, reject) => {
            (this.instance ? Promise.resolve(this.instance) : this._connect()).then((client) => {
                client.send(messageArray, (err) => {
                    if (err) {
                        reject(err)
                    }
                })

                client.on('message', (message) => {
                    resolve(message)

                    if (this.isDisconnectedAfterMessage) {
                        this.disconnect()
                    }
                })
            }).catch((error) => {
                reject(error)
            })
        })
    }

    /**
     * Disconnects the WebSocket by terminating the connection.
     */
    disconnect() {
        if (this.instance) {
            this.instance.close()
            this.instance = null
        }
        this.isConnected = false
    }

    /**
     * Connects to the WebSocket server.
     * @private
     * @async
     * @returns {Promise<WebSocket>} - A promise that resolves when the connection is established.
     */
    _connect() {
        return new Promise((resolve, reject) => {
            const client = new WebSocket(this.url)

            client.on(WebSocketStateEnum.OPEN, () => {
                this.isConnected = true
                this.instance = client;
                resolve(client)
            })

            // eslint-disable-next-line no-unused-vars
            client.on(WebSocketStateEnum.ERROR, (error) => {
                reject(error)
            })

            client.on(WebSocketStateEnum.CLOSE, () => {
                reject(new Error("Connection closed before receiving message"))
            })
        })
    }
}

module.exports = WebSocketClient

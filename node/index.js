const net = require('net')
const dgram = require('dgram')
const zmq = require('zeromq')

const message = Buffer.from('ping')
const client = dgram.createSocket('udp4')

client.on('listening', () => {
    const address = client.address();
    console.log(`client listening ${address.address}:${address.port}`);
});

client.on('message', (msg, info) => {
    const sock = zmq.socket("sub")

    sock.connect(`tcp://${info.address}:${info.port}`);
    sock.subscribe("POSE")

    sock.on("message", function(topic, message) {
        console.log(
            "received a message related to:",
            topic,
            "containing message:",
            message)
        })
})  

client.bind(1025, () => {
    client.addMembership('224.0.0.1')
});

client.send(message, 1024, '224.0.0.1', (err) => {
    if (err) {
        console.log('Error while sending', err)
    }
})

const Max = require("max-api")

const dgram = require('dgram')
const zmq = require('zeromq')
const struct = require('python-struct')

Max.addHandler('bang', () => {
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
            if (topic.toString() == 'POSE') {
                const data = struct.unpack('<19d', message)
                Max.outlet({
                    translation: data.slice(0, 3),
                    rotation: data.slice(3,7),
                    velocity: data.slice(7,10),
                    acceleration: data.slice(10,13),
                    angular_velocity: data.slice(13,16),
                    angular_acceleration: data.slice(16,19)
                })
            }
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
})

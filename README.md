# RFXCOM to MQTT bridge
Since I am running my Homeassistant setup in docker on Proxmox in a deep dark cabinet somewhere I needed a solution to get my 433Mhz signals from the center of my house to homeassistant.

I have setup a clean Raspberry Pi to act as a server and at first tried to set it up with Ser2Net and Socat([along these lines](https://community.home-assistant.io/t/hass-io-on-debian-vm-how-to-add-z-wave-usb-stick/80752)) but I was not able to get a stable setup.

So I started thinking about setting up a RF-MQTT bridge, I found some other solutions: With [Node-Red](https://thingsmatic.com/2018/01/07/rfxtrx433e-node-red-mqtt-and-home-assistant/), [perl](http://blog.tensin.org/posts/2017/09/rfxcom-to-mqtt/), [Haskell](https://github.com/dnulnets/rfxcom) and even [Javascript](https://github.com/rfxcom/node-rfxcom). Since I have pretty much no experience with these languages these seemed not a good fit for me. Luckily I found a Pyhton solution written by Anton04: [Anton04/RFXcom-MQTT-bridge
](https://github.com/Anton04/RFXcom-MQTT-bridge) this solution worked! However, the MQTT messages were not really nicely formatted or where they complete(information was missing) so I decided to implement my own solution.


# WORK IN PROGRESS!
It is an ongoing project, not ready for actual use
# Fly Today
[Fly today](https://ryderdamen.com/projects/fly-today) is a google assistant action that lets you know if it's VFR or IFR at an airport of your choice. For those who don't know what this means, it's pilot weather. VFR means it's Visual Flight Rules, so pilots without instrument training can fly. IFR means the weather sucks, so only pilots with specific instrument training can fly.

![Fly Today Logo](assets/banner-01.png)


## About
This project uses the [AVWX Rest API](http://avwx.rest) by [Michael duPont](http://mdupont.com/) as it's source of aviation information. I thought about creating my own API based on the Canadian AWS, but that's way too complicated and time consuming, and this one is pretty amazing.

## Using it
To activate it, you can say something like this to your Google Assistant enabled device:

`````txt
Hey Google, ask Fly Today if the Weather is good at YYZ right now
`````

to which the assistant responds

`````txt
Sure, here's Fly Today.

It's looking like low IFR right now at Lester B. Pearson International, Toronto.
`````



